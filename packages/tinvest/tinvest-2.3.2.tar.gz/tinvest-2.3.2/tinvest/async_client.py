from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Generic, Type, TypeVar

from aiohttp import ClientResponse, ClientSession
from pydantic import BaseModel  # pylint:disable=no-name-in-module

from .base_client import BaseClient
from .schemas import Error
from .utils import set_default_headers

__all__ = (
    'AsyncClient',
    'ResponseWrapper',
)

T = TypeVar('T', bound=BaseModel)  # pragma: no mutate


class ResponseWrapper(Generic[T]):
    S = TypeVar('S', bound=BaseModel)

    def __init__(self, response: ClientResponse, response_model: Type[T]):
        self._response = response
        self._response_model = response_model

    def __getattr__(self, name):
        return getattr(self._response, name)

    async def parse_json(self, **kwargs: Any) -> Any:
        return await self._parse_json(self._response_model, **kwargs)

    async def parse_error(self, **kwargs: Any) -> Error:
        return await self._parse_json(Error, **kwargs)

    async def _parse_json(self, response_model: Type[S], **kwargs: Any) -> S:
        return response_model.parse_obj(await self._response.json(**kwargs))


class AsyncClient(BaseClient[ClientSession]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._session is None:
            self._session = ClientSession()

    @asynccontextmanager
    async def request(
        self, method: str, path: str, response_model: Type[T], **kwargs: Any
    ) -> AsyncIterator[ResponseWrapper]:
        url = self._base_url + path
        set_default_headers(kwargs, self._token)

        async with self.session.request(method, url, **kwargs) as response:
            yield ResponseWrapper[T](response, response_model)

    async def close(self) -> None:
        await self.session.close()
