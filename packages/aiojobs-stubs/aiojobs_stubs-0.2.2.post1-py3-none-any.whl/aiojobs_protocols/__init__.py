from typing import Any, Awaitable, Callable, Dict, Optional, Protocol, TypeVar

_T = TypeVar('_T')
_T_co = TypeVar('_T_co', covariant=True)
_Context = Dict[str, Any]
_ExceptionHandler = Callable[['SchedulerProtocol', _Context], None]


class JobProtocol(Protocol[_T_co]):
    active: bool
    pending: bool
    closed: bool
    async def wait(self, *, timeout: Optional[float] = None) -> _T_co: ...
    async def close(self, *, timeout: Optional[float] = None) -> None: ...


class SchedulerProtocol(Protocol):
    limit: int
    pending_limit: int
    close_timeout: float
    active_count: int
    pending_count: int
    closed: bool
    exception_handler: _ExceptionHandler
    async def spawn(self, coro: Awaitable[_T]) -> JobProtocol[_T]: ...
    async def close(self) -> None: ...
    def call_exception_handler(self, context: _Context) -> None: ...
