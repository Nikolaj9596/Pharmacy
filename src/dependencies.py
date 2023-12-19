import contextlib
from typing import Optional
from collections.abc import AsyncIterator

from fastapi.requests import Request
from sqlalchemy.ext.asyncio import AsyncSession

from .engine import async_session_factory


async def get_session(request: Request) -> AsyncIterator[AsyncSession]:
    async with async_session_factory() as session:
        request.state.sqlalchemy_session = session
        yield session


@contextlib.asynccontextmanager
async def create_session() -> AsyncIterator[AsyncSession]:
    async with async_session_factory.begin() as session:
        yield session


class Paginator:
    def __init__(self, limit: int = 10, offset: int = 0):
        self.limit = limit
        self.offset = offset

class QueryParams:
    def __init__(self, search: Optional[str] = None, order: Optional[str] = None):
        self.search = search
        self.order = order 
