from abc import ABC, abstractmethod
from typing import Optional
from sqlalchemy import text

from sqlalchemy.ext.asyncio.session import AsyncSession

from src.dependencies import QueryParams
from src.doctor_app.dtos import (
    DoctorData,
    DoctorDataCreate,
    DoctorDetailData,
    DoctorProfession,
)
from src.exceptions import BadRequestEx


class IDoctorRepository(ABC):
    @abstractmethod
    async def get_by_id(
        self, id: int, session: AsyncSession
    ) -> Optional[DoctorData]:
        raise NotImplementedError()

    @abstractmethod
    async def get_detail_by_id(
        self, id: int, session: AsyncSession
    ) -> Optional[DoctorDetailData]:
        raise NotImplementedError()

    @abstractmethod
    async def get_list(
        self,
        session: AsyncSession,
        limit: int,
        offset: int,
        query_params: QueryParams,
    ) -> list[DoctorData] | list:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, id: int, session: AsyncSession) -> bool:
        raise NotImplementedError()

    @abstractmethod
    async def create(
        self, data: DoctorDataCreate, session: AsyncSession
    ) -> DoctorData:
        raise NotImplementedError()

    @abstractmethod
    async def update(
        self, data: DoctorDataCreate, session: AsyncSession, id: int
    ) -> DoctorData:
        raise NotImplementedError()


class DoctorRepository(IDoctorRepository):
    async def get_by_id(
        self, id: int, session: AsyncSession
    ) -> Optional[DoctorData]:
        query = text(
            'SELECT d.id, d.first_name, d.last_name, d.middle_name, d.created_at, d.updated_at, d.date_start_work, d.profession_id '
            'FROM doctor d  '
            'WHERE d.id=:id '
        )
        result = await session.execute(query, {'id': id})
        row = result.first()
        if not row:
            return None
        (
            id,
            first_name,
            last_name,
            middle_name,
            created_at,
            updated_at,
            date_start_work,
            profession,
        ) = row
        return DoctorData(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            date_start_work=date_start_work,
            profession=profession,
        )

    async def get_detail_by_id(
        self, id: int, session: AsyncSession
    ) -> Optional[DoctorDetailData]:
        query = text(
            'SELECT d.id, d.first_name, d.last_name, d.middle_name, d.created_at, d.updated_at, d.date_start_work, p.id, p.name '
            'FROM doctor d  '
            'LEFT JOIN profession p ON d.profession_id=p.id '
            'WHERE d.id=:id '
        )
        result = await session.execute(query, {'id': id})
        row = result.first()
        if not row:
            return None
        (
            id,
            first_name,
            last_name,
            middle_name,
            created_at,
            updated_at,
            date_start_work,
            profession_id,
            profession_name,
        ) = row
        return DoctorDetailData(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            date_start_work=date_start_work,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            profession=DoctorProfession(
                id=profession_id, name=profession_name
            ),
        )

    async def get_list(
        self,
        limit: int,
        offset: int,
        session: AsyncSession,
        query_params: QueryParams,
    ) -> list[DoctorData] | list:
        search = ''
        order = ''
        params = {'limit': limit, 'offset': offset}

        if query_params.search:
            search = 'WHERE d.first_name OR d.last_name OR d.middle_name LIKE :search '
            params['search'] = query_params.search

        if query_params.order:
            match query_params.order:
                case 'created_at':
                    order = 'ORDER BY p.created_at ASC '
                case '-created_at':
                    order = 'ORDER BY p.created_at DESC '
                case 'first_name':
                    order = 'ORDER BY p.name ASC '
                case 'last_name':
                    order = 'ORDER BY p.name ASC '
                case '_':
                    pass

        query = (
            'SELECT d.id, d.first_name, d.last_name, d.middle_name, d.created_at, d.updated_at, d.date_start_work, d.profession_id '
            'FROM doctor d  '
            f'{search}'
            f'{order}'
            'LIMIT :limit OFFSET :offset '
        )
        result = await session.execute(text(query), params)
        rows = result.fetchall()
        doctors = []

        for row in rows:
            (
                id,
                first_name,
                last_name,
                middle_name,
                created_at,
                updated_at,
                date_start_work,
                profession,
            ) = row
            doctors.append(
                DoctorData(
                    first_name=first_name,
                    id=id,
                    created_at=created_at,
                    updated_at=updated_at,
                    last_name=last_name,
                    middle_name=middle_name,
                    date_start_work=date_start_work,
                    profession=profession,
                )
            )
        return doctors

    async def delete(self, id: int, session: AsyncSession) -> bool:
        query = text('DELETE FROM doctor WHERE id=:id')
        await session.execute(query, {'id': id})
        await session.commit()
        return True

    async def create(
        self, data: DoctorDataCreate, session: AsyncSession
    ) -> DoctorData:
        query = text(
            'INSERT INTO doctor(first_name, last_name, middle_name, created_at, updated_at, date_start_work, profession_id) '
            'VALUES(:first_name, :last_name, :middle_name, now(), now(), :date_start_work, :profession) '
            'RETURNING id, first_name, last_name, middle_name, created_at, updated_at, date_start_work, profession_id '
        )
        result = await session.execute(query, dict(data))
        row = result.fetchone()
        if not row:
            raise BadRequestEx(detail='Failed to create a profession')
        await session.commit()
        (
            id,
            first_name,
            last_name,
            middle_name,
            created_at,
            updated_at,
            date_start_work,
            profession_id,
        ) = row
        return DoctorData(
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            date_start_work=date_start_work,
            profession=profession_id,
        )

    async def update(
        self, id: int, data: DoctorDataCreate, session: AsyncSession
    ) -> DoctorData:
        query = text(
            'UPDATE doctor SET first_name=:first_name, last_name=:last_name, middle_name=:middle_name, date_start_work=:date_start_work, updated_at=now(), profession_id=:profession '
            'WHERE id=:id RETURNING id, first_name, last_name, middle_name, created_at, updated_at, date_start_work, profession_id'
        )
        result = await session.execute(query, {'id': id, **data})
        row = result.fetchone()
        if not row:
            raise BadRequestEx(detail='Failed to update a profession')
        (
            _,
            first_name,
            last_name,
            middle_name,
            created_at,
            updated_at,
            date_start_work,
            profession_id,
        ) = row
        await session.commit()
        return DoctorData(
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            date_start_work=date_start_work,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            profession=profession_id,
        )
