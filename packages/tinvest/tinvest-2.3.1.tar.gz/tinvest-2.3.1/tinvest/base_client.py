from typing import Generic, Optional, TypeVar

from .constants import PRODUCTION, SANDBOX

__all__ = ('BaseClient',)

T = TypeVar('T')  # pragma: no mutate


class BaseClient(Generic[T]):
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
