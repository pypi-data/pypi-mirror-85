from abc import ABC, abstractmethod
from typing import Any, Generic, Optional, Type, TypeVar

from pydantic import BaseModel  # pylint:disable=no-name-in-module

from .constants import PRODUCTION, SANDBOX

__all__ = ('BaseClient',)

T = TypeVar('T')  # pragma: no mutate
S = TypeVar('S')  # pragma: no mutate
M = TypeVar('M', bound=BaseModel)  # pragma: no mutate


class BaseClient(ABC, Generic[T, S]):
    def __init__(
        self, token: str, *, use_sandbox: bool = False, session: Optional[T] = None
    ):
        if not token:
            raise ValueError('Token can not be empty')
        self._base_url: str = PRODUCTION
        if use_sandbox:
            self._base_url = SANDBOX

        self._token: str = token
        self._session = session

    @property
    def session(self) -> T:
        if self._session:
            return self._session
        raise AttributeError

    @abstractmethod
    def request(
        self, method: str, path: str, response_model: Type[M], **kwargs: Any
    ) -> S:
        pass
