from typing import Any, Generic, Type, TypeVar

from pydantic import BaseModel  # pylint:disable=no-name-in-module
from requests import Response, Session, session

from .base_client import BaseClient
from .schemas import Error
from .utils import set_default_headers

__all__ = ('SyncClient', 'ResponseWrapper')

T = TypeVar('T', bound=BaseModel)  # pragma: no mutate


class ResponseWrapper(Generic[T]):
    S = TypeVar('S', bound=BaseModel)

    def __init__(self, response: Response, response_model: Type[T]):
        self._response = response
        self._response_model = response_model

    def __getattr__(self, name):
        return getattr(self._response, name)

    def parse_json(self, **kwargs: Any) -> T:
        return self._parse_json(self._response_model, **kwargs)

    def parse_error(self, **kwargs: Any) -> Error:
        return self._parse_json(Error, **kwargs)

    def _parse_json(self, response_model: Type[S], **kwargs: Any) -> S:
        return response_model.parse_obj(self._response.json(**kwargs))


class SyncClient(BaseClient[Session]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._session is None:
            self._session = session()

    def request(
        self,
        method: str,
        path: str,
        response_model: Type[T],
        raise_for_status: bool = False,
        **kwargs: Any,
    ) -> ResponseWrapper:
        url = self._base_url + path
        set_default_headers(kwargs, self._token)

        response = ResponseWrapper[T](
            self.session.request(method, url, **kwargs), response_model
        )

        if raise_for_status:
            response.raise_for_status()

        return response
