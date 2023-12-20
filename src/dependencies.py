import contextlib
from datetime import datetime
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
    def __init__(
        self, search: Optional[str] = None, order: Optional[str] = None
    ):
        self.search = search
        self.order = order

class QueryParamsAppointment:
    def __init__(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        doctor: Optional[int] = None,
        client: Optional[int] = None,
        order: Optional[str] = None
    ):
        self.start_date = start_date
        self.end_date = end_date
        self.doctor = doctor
        self.client = client
        self.order = order
