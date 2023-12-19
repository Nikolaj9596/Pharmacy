from abc import ABC, abstractmethod
from typing import Optional
from sqlalchemy import text

from sqlalchemy.ext.asyncio import AsyncSession
from src.dependencies import QueryParams
from src.exeptions import BadRequestEx

from src.profession_app.dtos import (
    ProfessionDataCreate,
    ProfessionDataGet,
    ProfessionDataDetailGet,
)


class IProfessionRepository(ABC):
    @abstractmethod
    async def get_by_id(
        self, id: int, session: AsyncSession
    ) -> Optional[ProfessionDataGet]:
        raise NotImplementedError()

    @abstractmethod
    async def get_list(
        self,
        session: AsyncSession,
        limit: int,
        offset: int,
        query_params: QueryParams,
    ) -> list[ProfessionDataDetailGet] | list:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, id: int, session: AsyncSession) -> bool:
        raise NotImplementedError()

    @abstractmethod
    async def create(
        self, data: ProfessionDataCreate, session: AsyncSession
    ) -> ProfessionDataGet:
        raise NotImplementedError()

    @abstractmethod
    async def update(
        self, data: ProfessionDataCreate, session: AsyncSession, id: int
    ) -> ProfessionDataGet:
        raise NotImplementedError()


class ProfessionRepository(IProfessionRepository):
    async def get_by_id(
        self, id: int, session: AsyncSession
    ) -> Optional[ProfessionDataGet]:
        query = text(
            'SELECT p.id, p.name, p.created_at, p.updated_at '
            'FROM profession p  '
            'WHERE p.id=:id '
        )
        result = await session.execute(query, {'id': id})
        row = result.first()
        if not row:
            return None
        id, name, created_at, updated_at = row
        return ProfessionDataGet(
            name=name,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
        )

    async def get_list(
        self,
        limit: int,
        offset: int,
        session: AsyncSession,
        query_params: QueryParams,
    ) -> list[ProfessionDataDetailGet] | list:
        search = ''
        # INFO: Search
        params = {'limit': limit, 'offset': offset}

        if query_params.search:
            search = 'WHERE p.name LIKE :search '
            params['search'] = query_params.search

        query = (
            'SELECT p.id, p.name, p.created_at, p.updated_at, COUNT(d.id) as number_of_specialists '
            'FROM profession p  '
            'LEFT JOIN doctor d ON p.id=d.profession_id '
            f'{search}'
            'GROUP BY p.id, p.name, p.created_at, p.updated_at '
            'LIMIT :limit OFFSET :offset '
        )
        result = await session.execute(text(query), params)
        rows = result.fetchall()
        professions = []

        for row in rows:
            id, name, created_at, updated_at, number_of_specialists = row
            professions.append(
                ProfessionDataDetailGet(
                    name=name,
                    id=id,
                    created_at=created_at,
                    updated_at=updated_at,
                    number_of_specialists=number_of_specialists,
                )
            )
        return professions

    async def delete(self, id: int, session: AsyncSession) -> bool:
        query = text('DELETE FROM profession WHERE id=:id')
        await session.execute(query, {'id': id})
        await session.commit()
        return True

    async def create(
        self, data: ProfessionDataCreate, session: AsyncSession
    ) -> ProfessionDataGet:
        query = text(
            'INSERT INTO profession(name, created_at, updated_at) '
            'VALUES(:name, now(), now()) '
            'RETURNING id, name, created_at, updated_at'
        )
        result = await session.execute(query, dict(data))
        row = result.fetchone()
        if not row:
            raise BadRequestEx(detail='Failed to create a profession')
        await session.commit()
        id, name, created_at, updated_at = row
        return ProfessionDataGet(
            name=name, id=id, created_at=created_at, updated_at=updated_at
        )

    async def update(
        self, id: int, data: ProfessionDataCreate, session: AsyncSession
    ) -> ProfessionDataGet:
        query = text(
            'UPDATE profession SET name=:name, updated_at=now() '
            'WHERE id=:id RETURNING id, name, created_at, updated_at'
        )
        result = await session.execute(query, {'id': id, **data})
        row = result.fetchone()
        if not row:
            raise BadRequestEx(detail='Failed to update a profession')
        raw_id, name, created_at, updated_at = row
        await session.commit()
        return ProfessionDataGet(
            name=name, id=id, created_at=created_at, updated_at=updated_at
        )
