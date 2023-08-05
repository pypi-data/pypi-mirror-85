import asyncio
import functools
import typing
from datetime import timezone

from .typedefs import AnyDict, datetime_or_str

try:
    import contextvars  # Python 3.7+ only.
except ImportError:  # pragma: no cover
    contextvars = None  # type: ignore # pragma: no mutate

__all__ = (
    'set_default_headers',
    'Func',
    'run_in_threadpool',
    'isoformat',
    'infinity',
)


def set_default_headers(data: AnyDict, token: str) -> None:
    headers = data.get('headers', {})
    headers.setdefault('accept', 'application/json')
    headers.setdefault('Authorization', f'Bearer {token}')
    data['headers'] = headers


T = typing.TypeVar('T')  # pragma: no mutate


class Func:
    def __init__(
        self, func: typing.Callable, *args: typing.Any, **kwargs: typing.Any
    ) -> None:
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.is_async = asyncio.iscoroutinefunction(func)

    async def __call__(self) -> None:
        if self.is_async:
            return await self.func(*self.args, **self.kwargs)
        return await run_in_threadpool(self.func, *self.args, **self.kwargs)


async def run_in_threadpool(
    func: typing.Callable[..., T], *args: typing.Any, **kwargs: typing.Any
) -> T:
    loop = asyncio.get_event_loop()
    if contextvars is not None:  # pragma: no cover, no mutate
        # Ensure we run in the same context
        child = functools.partial(func, *args, **kwargs)
        context = contextvars.copy_context()
        func = context.run
        args = (child,)
    elif kwargs:  # pragma: no cover
        # loop.run_in_executor doesn't accept 'kwargs', so bind them in here
        func = functools.partial(func, **kwargs)  # pragma: no mutate
    return await loop.run_in_executor(None, func, *args)


def isoformat(dt: datetime_or_str) -> str:
    if isinstance(dt, str):
        return dt
    return dt.replace(tzinfo=timezone.utc).isoformat()


def infinity(func: typing.Callable[..., typing.Awaitable[None]]):
    @functools.wraps(func)
    async def wrapper(
        *args: typing.Any, **kwargs: typing.Any
    ) -> typing.Awaitable[None]:
        while True:
            await func(*args, **kwargs)

    return wrapper
