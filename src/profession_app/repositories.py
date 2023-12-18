from abc import ABC, abstractmethod
from typing import Optional
from sqlalchemy import text

from sqlalchemy.ext.asyncio import AsyncSession

from src.profession_app.dtos import ProfessionDataCreate, ProfessionDataGet


class IProfessionRepository(ABC):
    @abstractmethod
    async def get_by_id(
        self, id: int, session: AsyncSession
    ) -> Optional[ProfessionDataGet]:
        raise NotImplementedError()

    @abstractmethod
    async def get_list(self) -> list[ProfessionDataGet] | list:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, id: int) -> bool:
        raise NotImplementedError()

    @abstractmethod
    async def create(self, data: ProfessionDataCreate) -> ProfessionDataGet:
        raise NotImplementedError()

    @abstractmethod
    async def update(
        self, data: ProfessionDataCreate
    ) -> Optional[ProfessionDataGet]:
        raise NotImplementedError()


class ProfessionRepository(IProfessionRepository):
    async def get_by_id(
        self, id: int, session: AsyncSession
    ) -> Optional[ProfessionDataGet]:
        query = text('SELECT * FROM profession p WHERE p.id=:id')
        query = query.bindparams(id=id)
        result = await session.execute(query)
        row = result.first()
        if not row:
            return None
        return ProfessionDataGet(*row)

    async def get_list(self) -> list[ProfessionDataGet] | list:
        raise NotImplementedError()

    async def delete(self, id: int) -> bool:
        raise NotImplementedError()

    async def create(self, data: ProfessionDataCreate) -> ProfessionDataGet:
        raise NotImplementedError()

    async def update(
        self, data: ProfessionDataCreate
    ) -> Optional[ProfessionDataGet]:
        raise NotImplementedError()
