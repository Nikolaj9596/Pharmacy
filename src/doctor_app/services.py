__all__ = ['AppointmentService', 'DoctorService']

from typing import Optional
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.dependencies import Paginator, QueryParams, QueryParamsAppointment
from src.doctor_app.dtos import (
    AppointmentData,
    AppointmentDataCreate,
    AppointmentResponse,
    DoctorData,
    DoctorDataCreate,
    DoctorDetailData,
)
from src.doctor_app.repositories import (
    IDoctorAppointmentRepository,
    IDoctorRepository,
)
from src.doctor_app.schemes import (
    AppointmentCreateScheme,
    AppointmentScheme,
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
        query = text('SELECT p.id FROM professions p WHERE p.id=:id')
        result = await session.execute(query, {'id': id})
        row = result.first()
        if not row:
            raise NotFoundEx(detail=f'Profession with id: {id} not found')
        return True

    async def get_by_id(
        self, id: int, session: AsyncSession
    ) -> DoctorDetailScheme:
        doctor: Optional[DoctorDetailData] = await self.repository.get_by_id(
            id=id, session=session
        )
        if not doctor:
            raise NotFoundEx(detail=f'Doctor with id: {id} not found')
        return DoctorDetailScheme.model_validate(doctor)

    async def get_list(
        self,
        session: AsyncSession,
        pagination: Paginator,
        query_params: QueryParams,
    ) -> list[DoctorDetailScheme] | list:
        doctors: list[DoctorData] | list = await self.repository.get_list(
            session=session,
            limit=pagination.limit,
            offset=pagination.offset,
            query_params=query_params,
        )
        if not doctors:
            return doctors
        return [
            DoctorDetailScheme.model_validate(doctor) for doctor in doctors
        ]

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
        return DoctorScheme.model_validate(doctor)

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
        return DoctorScheme.model_validate(doctor)

    async def delete(self, id: int, session: AsyncSession) -> None:
        await self._check_exists(id=id, session=session)
        deleted = await self.repository.delete(session=session, id=id)
        if not deleted:
            raise BadRequestEx(detail='Failed to delete a profession')
        return None


class AppointmentService:
    def __init__(self, repository: IDoctorAppointmentRepository):
        self.repository = repository

    async def _check_exists(
        self, id: int, session: AsyncSession
    ) -> AppointmentData:
        doctor: Optional[AppointmentData] = await self.repository.get_by_id(
            id=id, session=session
        )
        if not doctor:
            raise NotFoundEx(detail=f'Appointment with id: {id} not found')
        return doctor

    async def _check_related_doctor_exists(
        self, id: int, session: AsyncSession
    ) -> bool:
        query = text('SELECT d.id FROM doctors d WHERE d.id=:id')
        result = await session.execute(query, {'id': id})
        row = result.first()
        if not row:
            raise NotFoundEx(detail=f'Doctor with id: {id} not found')
        return True

    async def _check_related_client_exists(
        self, id: int, session: AsyncSession
    ) -> bool:
        query = text('SELECT c.id FROM clients c WHERE c.id=:id')
        result = await session.execute(query, {'id': id})
        row = result.first()
        if not row:
            raise NotFoundEx(detail=f'Client with id: {id} not found')
        return True

    async def _check_doctor_is_busy(
        self,
        data: AppointmentCreateScheme,
        session: AsyncSession,
    ) -> bool:
        appointments: list[
            AppointmentData
        ] | list = await self.repository.get_list(
            session=session,
            limit=1,
            offset=0,
            query_params=QueryParamsAppointment(
                start_date=data.start_date_appointment,
                end_date=data.end_date_appointment,
                doctor=data.doctor,
                client=data.client,
            ),
        )
        if appointments:
            return True
        return False

    async def get_by_id(
        self, id: int, session: AsyncSession
    ) -> AppointmentScheme:
        appointment: Optional[
            AppointmentData
        ] = await self.repository.get_detail_by_id(id=id, session=session)
        if not appointment:
            raise NotFoundEx(detail=f'Appointment with id: {id} not found')
        return AppointmentScheme.model_validate(appointment)

    async def get_list(
        self,
        session: AsyncSession,
        pagination: Paginator,
        query_params: QueryParamsAppointment,
    ) -> list[AppointmentScheme] | list:
        appointments: list[
            AppointmentData
        ] | list = await self.repository.get_list(
            session=session,
            limit=pagination.limit,
            offset=pagination.offset,
            query_params=query_params,
        )
        if not appointments:
            return appointments
        return [
            AppointmentScheme.model_validate(appointment)
            for appointment in appointments
        ]

    async def create(
        self, session: AsyncSession, data: AppointmentCreateScheme
    ) -> AppointmentCreateScheme:
        await self._check_related_doctor_exists(
            id=data.doctor, session=session
        )
        await self._check_related_client_exists(
            id=data.client, session=session
        )
        await self._check_doctor_is_busy(session=session, data=data)

        appointment: AppointmentResponse = await self.repository.create(
            session=session, data=AppointmentDataCreate(**data.model_dump())
        )
        return AppointmentCreateScheme.model_validate(dict(appointment))

    async def update(
        self, session: AsyncSession, data: AppointmentCreateScheme, id: int
    ) -> AppointmentScheme:
        await self._check_exists(id=id, session=session)
        await self._check_related_doctor_exists(
            id=data.doctor, session=session
        )
        await self._check_related_client_exists(
            id=data.client, session=session
        )
        await self._check_doctor_is_busy(session=session, data=data)
        appointment = await self.repository.update(
            session=session,
            data=AppointmentDataCreate(**data.model_dump()),
            id=id,
        )
        return AppointmentScheme.model_validate(appointment)

    async def delete(self, id: int, session: AsyncSession) -> None:
        await self._check_exists(id=id, session=session)
        deleted = await self.repository.delete(session=session, id=id)
        if not deleted:
            raise BadRequestEx(detail='Failed to delete a appointment')
        return None
