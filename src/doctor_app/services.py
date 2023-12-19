from typing import Optional
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.dependencies import Paginator, QueryParams
from src.doctor_app.dtos import DoctorData, DoctorDataCreate, DoctorDetailData
from src.doctor_app.repositories import IDoctorRepository
from src.doctor_app.schemes import (
    DoctorCreateScheme,
    DoctorDetailScheme,
    DoctorScheme,
)
from src.exceptions import BadRequestEx, NotFoundEx


class DoctorService:
    def __init__(self, repository: IDoctorRepository):
        self.repository = repository

    async def _check_exists(
        self, id: int, session: AsyncSession
    ) -> DoctorData:
        doctor: Optional[DoctorData] = await self.repository.get_by_id(
            id=id, session=session
        )
        if not doctor:
            raise NotFoundEx(detail=f'Doctor with id: {id} not found')
        return doctor

    async def _check_related_profession_exists(
        self, id: int, session: AsyncSession
    ) -> bool:
        query = text('SELECT p.id FROM profession p WHERE p.id=:id')
        result = await session.execute(query, {'id': id})
        row = result.first()
        if not row:
            raise NotFoundEx(detail=f'Profession with id: {id} not found')
        return True

    async def get_by_id(
        self, id: int, session: AsyncSession
    ) -> DoctorDetailScheme:
        doctor: Optional[
            DoctorDetailData
        ] = await self.repository.get_detail_by_id(id=id, session=session)
        if not doctor:
            raise NotFoundEx(detail=f'Doctor with id: {id} not found')
        return DoctorDetailScheme(**doctor)

    async def get_list(
        self,
        session: AsyncSession,
        pagination: Paginator,
        query_params: QueryParams,
    ) -> list[DoctorScheme] | list:
        doctors: list[DoctorData] | list = await self.repository.get_list(
            session=session,
            limit=pagination.limit,
            offset=pagination.offset,
            query_params=query_params,
        )
        if not doctors:
            return doctors
        return [DoctorScheme(**doctor) for doctor in doctors]

    async def create(
        self, session: AsyncSession, data: DoctorCreateScheme
    ) -> DoctorScheme:
        await self._check_related_profession_exists(
            id=data.profession, session=session
        )
        try:
            doctor: DoctorData = await self.repository.create(
                session=session, data=DoctorDataCreate(**data.model_dump())
            )
        except IntegrityError:
            raise BadRequestEx(
                detail='There is already a doctor with this first_name, last_name, middle_name'
            )
        return DoctorScheme(**doctor)

    async def update(
        self, session: AsyncSession, data: DoctorCreateScheme, id: int
    ) -> DoctorScheme:
        doctor = await self._check_exists(id=id, session=session)
        await self._check_related_profession_exists(
            id=data.profession, session=session
        )
        try:
            doctor = await self.repository.update(
                session=session,
                data=DoctorDataCreate(**data.model_dump()),
                id=id,
            )
        except IntegrityError:
            raise BadRequestEx(
                detail='There is already a doctor with this first_name, last_name, middle_name'
            )
        return DoctorScheme(**doctor)

    async def delete(self, id: int, session: AsyncSession) -> None:
        await self._check_exists(id=id, session=session)
        deleted = await self.repository.delete(session=session, id=id)
        if not deleted:
            raise BadRequestEx(detail='Failed to delete a profession')
        return None
