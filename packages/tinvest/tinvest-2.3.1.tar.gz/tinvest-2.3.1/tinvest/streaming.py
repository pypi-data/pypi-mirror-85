import asyncio
import logging
from datetime import datetime
from typing import Any, Callable, Coroutine, Dict, List, Optional, Tuple, Union

import aiohttp
from pydantic.datetime_parse import parse_datetime  # pylint:disable=E0611

from .constants import STREAMING
from .schemas import (
    CandleResolution,
    CandleStreaming,
    ErrorStreaming,
    EventName,
    InstrumentInfoStreaming,
    OrderbookStreaming,
    ServiceEventName,
)
from .typedefs import AnyDict
from .utils import Func, infinity

__all__ = (
    'Streaming',
    'StreamingApi',
    'StreamingEvents',
    'CandleEvent',
    'OrderbookEvent',
    'InstrumentInfoEvent',
)

logger = logging.getLogger(__name__)


_Handler = Tuple[str, Callable]  # pragma: no mutate


class Streaming:
    schemas: Dict[EventName, Any] = {
        EventName.candle: CandleStreaming,
        EventName.orderbook: OrderbookStreaming,
        EventName.instrument_info: InstrumentInfoStreaming,
        EventName.error: ErrorStreaming,
    }

    def __init__(
        self,
        token: str,
        *,
        session: Optional[aiohttp.ClientSession] = None,
        state: Optional[AnyDict] = None,
        reconnect_timeout: float = 3,
        ws_close_timeout: float = 0,
        receive_timeout: Optional[float] = 5,
        heartbeat: Optional[float] = 3,
    ) -> None:
        """
        ```python
        import tinvest

        events = tinvest.StreamingEvents()

        ...

        async def main():
            await (
                tinvest.Streaming("TOKEN", state={"postgres": ...})
                .add_handlers(events)
                .run()
            )

        if __name__ == "__main__":
            try:
                asyncio.run(main())
            except KeyboardInterrupt:
                pass
        ```
        """
        super().__init__()
        if not token:
            raise ValueError('Token can not be empty')
        self._api: str = STREAMING
        self._token: str = token
        self._session: aiohttp.ClientSession = session or aiohttp.ClientSession()
        self._handlers: List[_Handler] = []
        self._state = state
        self._reconnect_timeout = reconnect_timeout
        self._ws_close_timeout = ws_close_timeout
        self._receive_timeout = receive_timeout
        self._heartbeat = heartbeat

    def add_handlers(
        self, handlers: Union[List[_Handler], 'StreamingEvents']
    ) -> 'Streaming':
        if isinstance(handlers, list):
            self._handlers.extend(handlers)
        else:
            self._handlers.extend(handlers.handlers)

        for _, handler in self._handlers:
            handler.receive_server_time__ = (  # type:ignore
                'server_time' in handler.__code__.co_varnames
            )
        return self

    @infinity
    async def run(self) -> None:
        try:
            async with self._session.ws_connect(
                self._api,
                headers={'Authorization': f'Bearer {self._token}'},
                heartbeat=self._heartbeat,
                timeout=self._ws_close_timeout,
                receive_timeout=self._receive_timeout,
            ) as ws:
                await self._run(ws)
        except asyncio.CancelledError:  # pylint:disable=try-except-raise
            raise
        except asyncio.TimeoutError:
            logger.error('Timeout error. Try to reconnect')
            await asyncio.sleep(self._reconnect_timeout)
        except aiohttp.ClientConnectorError as e:
            logger.error('Connection error: %s. Try to reconnect', e)
            await asyncio.sleep(self._reconnect_timeout)
        funcs = self._get_handlers(ServiceEventName.reconnect)
        await asyncio.gather(*[Func(func)() for func in funcs])

    async def _run(self, ws):
        api = StreamingApi(ws, self._state)
        try:
            funcs = self._get_handlers(ServiceEventName.startup)
            await asyncio.gather(*[Func(func, api)() for func in funcs])

            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    data = msg.json()

                    event_name = data['event']
                    payload = data['payload']
                    server_time = parse_datetime(data['time'])

                    if event_name in self.schemas:
                        data = self.schemas[event_name].parse_obj(payload)
                    else:
                        data = payload

                    await asyncio.gather(
                        *self._call_handlers(event_name, api, data, server_time)
                    )

                elif msg.type == aiohttp.WSMsgType.CLOSED:
                    break
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    break
        except asyncio.CancelledError:
            await self._cleanup(api)
            raise

    def _call_handlers(
        self,
        event_name: EventName,
        api: 'StreamingApi',
        data: Any,
        server_time: datetime,
    ) -> List[Coroutine[Any, Any, None]]:
        funcs = []
        for func in self._get_handlers(event_name):
            kwargs = {}
            if func.receive_server_time__:
                kwargs['server_time'] = server_time

            funcs.append(Func(func, api, data, **kwargs)())

        return funcs

    def _get_handlers(self, event_name):
        return (func for name, func in self._handlers if name == event_name)

    async def _cleanup(self, api) -> None:
        funcs = self._get_handlers(ServiceEventName.cleanup)
        await asyncio.gather(*[Func(func, api)() for func in funcs])
        await self._session.close()


class _BaseEvent:
    def __init__(self, ws):
        self.ws = ws

    async def _send(self, payload):
        await self.ws.send_json(payload)


class CandleEvent(_BaseEvent):
    INTERVALS = tuple(c.value for c in CandleResolution)

    def subscribe(
        self,
        figi: str,
        interval: CandleResolution,
        request_id: Optional[str] = None,
    ):
        return self._send(
            {
                'event': f'{EventName.candle}:subscribe',
                **self._get_payload(figi, interval, request_id),
            }
        )

    def unsubscribe(
        self,
        figi: str,
        interval: CandleResolution,
        request_id: Optional[str] = None,
    ):
        return self._send(
            {
                'event': f'{EventName.candle}:unsubscribe',
                **self._get_payload(figi, interval, request_id),
            }
        )

    def _get_payload(
        self,
        figi: str,
        interval: CandleResolution,
        request_id: Optional[str] = None,
    ):
        if interval not in self.INTERVALS:
            raise ValueError(f'{interval} not in {self.INTERVALS}')

        data = {'figi': figi, 'interval': interval}
        if request_id:
            data['request_id'] = request_id
        return data


class OrderbookEvent(_BaseEvent):
    def subscribe(self, figi: str, depth: int = 2, request_id: Optional[str] = None):
        return self._send(
            {
                'event': f'{EventName.orderbook}:subscribe',
                **self._get_payload(figi, depth, request_id),
            }
        )

    def unsubscribe(self, figi: str, depth: int = 2, request_id: Optional[str] = None):
        return self._send(
            {
                'event': f'{EventName.orderbook}:unsubscribe',
                **self._get_payload(figi, depth, request_id),
            }
        )

    @staticmethod
    def _get_payload(figi: str, depth: int = 2, request_id: Optional[str] = None):
        if not 0 < depth <= 20:
            raise ValueError(f'not 0 < {depth} <= 20')
        data = {'figi': figi, 'depth': depth}
        if request_id:
            data['request_id'] = request_id
        return data


class InstrumentInfoEvent(_BaseEvent):
    def subscribe(self, figi: str, request_id: Optional[str] = None):
        return self._send(
            {
                'event': f'{EventName.instrument_info}:subscribe',
                **self._get_payload(figi, request_id),
            }
        )

    def unsubscribe(self, figi: str, request_id: Optional[str] = None):
        return self._send(
            {
                'event': f'{EventName.instrument_info}:unsubscribe',
                **self._get_payload(figi, request_id),
            }
        )

    @staticmethod
    def _get_payload(figi: str, request_id: Optional[str] = None):
        data = {'figi': figi}
        if request_id:
            data['request_id'] = request_id

        return data


class StreamingEvents:
    """
    ```python
    import tinvest

    events = tinvest.StreamingEvents()
    ```
    """

    def __init__(self) -> None:
        self.handlers: List[_Handler] = []

    def _decorator_wrapper(self, event_name: str):
        def decorator(func):
            self.handlers.append((event_name, func))
            return func

        return decorator

    def startup(self):
        """
        ```python
        @events.startup()
        async def startup(api: tinvest.StreamingApi):
            await api.candle.subscribe("BBG0013HGFT4", tinvest.CandleResolution.min1)
            await api.orderbook.subscribe("BBG0013HGFT4", 5, "123ASD1123")
            await api.instrument_info.subscribe("BBG0013HGFT4")
        ```
        """
        return self._decorator_wrapper(ServiceEventName.startup)

    def candle(self):
        """
        ```python
        @events.candle()
        async def handle_candle(
            api: tinvest.StreamingApi,
            payload: tinvest.CandleStreaming,
            server_time: datetime  # [optional] if you want
        ):
            pass
        ```
        ```python
        @events.candle()
        async def handle_candle(
            api: tinvest.StreamingApi,
            payload: tinvest.CandleStreaming,
        ):
            pass
        ```
        """
        return self._decorator_wrapper(EventName.candle)

    def orderbook(self):
        """
        ```python
        @events.orderbook()
        async def handle_orderbook(
            api: tinvest.StreamingApi, payload: tinvest.OrderbookStreaming
        ):
            pass
        ```
        """
        return self._decorator_wrapper(EventName.orderbook)

    def instrument_info(self):
        """
        ```python
        @events.instrument_info()
        async def handle_instrument_info(
            api: tinvest.StreamingApi, payload: tinvest.InstrumentInfoStreaming
        ):
            pass
        ```
        """
        return self._decorator_wrapper(EventName.instrument_info)

    def error(self):
        """
        ```python
        @events.error()
        async def handle_error(
            api: tinvest.StreamingApi, payload: tinvest.ErrorStreaming
        ):
            pass
        ```
        """
        return self._decorator_wrapper(EventName.error)

    def cleanup(self):
        """
        ```python
        @events.cleanup()
        async def cleanup(api: tinvest.StreamingApi):
            await api.candle.unsubscribe("BBG0013HGFT4", "1min")
            await api.orderbook.unsubscribe("BBG0013HGFT4", 5)
            await api.instrument_info.unsubscribe("BBG0013HGFT4")
        ```
        """
        return self._decorator_wrapper(ServiceEventName.cleanup)

    def reconnect(self):
        """
        ```python
        @events.reconnect()
        def handle_reconnect():
            pass
        ```
        ```python
        @events.reconnect()
        async def handle_reconnect():
            pass
        ```
        """
        return self._decorator_wrapper(ServiceEventName.reconnect)


class StreamingApi:
    def __init__(self, ws, state: Optional[AnyDict] = None) -> None:
        self.candle = CandleEvent(ws)
        self.orderbook = OrderbookEvent(ws)
        self.instrument_info = InstrumentInfoEvent(ws)
        self._state = state

    def __getitem__(self, key: str) -> Any:
        if self._state and key in self._state:
            return self._state[key]
        raise KeyError
