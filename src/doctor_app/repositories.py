from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Optional
from sqlalchemy import text

from sqlalchemy.ext.asyncio.session import AsyncSession

from src.doctor_app.dtos import (
    AppointmentData,
    AppointmentDataCreate,
    AppointmentResponse,
    DoctorData,
    DoctorDataCreate,
    DoctorDetailData,
    DoctorProfession,
)
from src.exceptions import BadRequestEx
from src.dependencies import QueryParams, QueryParamsAppointment


class IDoctorRepository(ABC):
    @abstractmethod
    async def get_by_id(
        self, id: int, session: AsyncSession
    ) -> Optional[DoctorData]:
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


class IDoctorAppointmentRepository(ABC):
    @abstractmethod
    async def get_by_id(
        self, id: int, session: AsyncSession
    ) -> Optional[AppointmentData]:
        raise NotImplementedError()

    @abstractmethod
    async def get_detail_by_id(
        self, id: int, session: AsyncSession
    ) -> Optional[AppointmentData]:
        raise NotImplementedError()

    @abstractmethod
    async def get_list(
        self,
        session: AsyncSession,
        limit: int,
        offset: int,
        query_params: QueryParamsAppointment,
    ) -> list[AppointmentData] | list:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, id: int, session: AsyncSession) -> bool:
        raise NotImplementedError()

    @abstractmethod
    async def create(
        self, data: AppointmentDataCreate, session: AsyncSession
    ) -> AppointmentResponse:
        raise NotImplementedError()

    @abstractmethod
    async def update(
        self, data: AppointmentDataCreate, session: AsyncSession, id: int
    ) -> AppointmentData:
        raise NotImplementedError()


class DoctorRepository(IDoctorRepository):
    async def get_by_id(
        self, id: int, session: AsyncSession
    ) -> Optional[DoctorDetailData]:
        query = text(
            """
                SELECT 
                    d.id, d.first_name, d.last_name,
                    d.middle_name, d.date_start_work, 
                    d.date_birthday, d.avatar,
                    json_build_object('name', p.name, 'id', p.id) as profession
                FROM doctors d
                LEFT JOIN professions p ON d.profession_id=p.id
                WHERE d.id=:id
            """
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
            date_start_work,
            date_birthday,
            avatar,
            profession,
        ) = row
        return DoctorDetailData(
            id=id,
            date_start_work=date_start_work,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            date_birthday=date_birthday,
            avatar=avatar,
            profession=DoctorProfession(profession),
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
        params: dict[str, Any] = {'limit': limit, 'offset': offset}

        if query_params.search:
            search = 'WHERE d.first_name OR d.last_name OR d.middle_name LIKE :search '
            params['search'] = query_params.search

        if query_params.order:
            match query_params.order:
                case 'created_at':
                    order = 'ORDER BY d.created_at ASC '
                case '-created_at':
                    order = 'ORDER BY d.created_at DESC '
                case 'first_name':
                    order = 'ORDER BY d.first_name ASC '
                case 'last_name':
                    order = 'ORDER BY d.last_name ASC '
                case '_':
                    pass

        query = (
            """
            SELECT 
                d.id, d.first_name, d.last_name,
                d.middle_name, d.date_start_work, d.date_birthday, d.avatar,
                json_build_object('name', p.name, 'id', p.id) as profession
            FROM doctors d
            LEFT JOIN professions p
                ON d.profession_id=p.id
            """
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
                date_start_work,
                date_birthday,
                avatar,
                profession,
            ) = row
            doctors.append(
                DoctorData(
                    first_name=first_name,
                    id=id,
                    last_name=last_name,
                    middle_name=middle_name,
                    date_start_work=date_start_work,
                    date_birthday=date_birthday,
                    avatar=avatar,
                    profession=profession,
                )
            )
        return doctors

    async def delete(self, id: int, session: AsyncSession) -> bool:
        query = text('DELETE FROM doctors WHERE id=:id')
        await session.execute(query, {'id': id})
        await session.commit()
        return True

    async def create(
        self, data: DoctorDataCreate, session: AsyncSession
    ) -> DoctorData:
        query = text(
            """
            INSERT INTO doctors(
                first_name, last_name, middle_name,
                created_at, updated_at, date_start_work, profession_id,
                date_birthday, avatar
            )
            VALUES(
                :first_name, :last_name, :middle_name, 
                now(), now(), :date_start_work, :profession,
                :date_birthday, :avatar
            )
            RETURNING 
                id, first_name, last_name, middle_name, 
                date_start_work, profession_id, date_birthday, avatar
            """
        )
        data['avatar'] = str(data['avatar'])
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
            date_start_work,
            profession_id,
            date_birthday,
            avatar,
        ) = row
        return DoctorData(
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            id=id,
            date_start_work=date_start_work,
            profession=profession_id,
            date_birthday=date_birthday,
            avatar=avatar,
        )

    async def update(
        self, id: int, data: DoctorDataCreate, session: AsyncSession
    ) -> DoctorData:
        query = text(
            """
            UPDATE doctors 
                SET first_name=:first_name,
                    last_name=:last_name, 
                    middle_name=:middle_name, 
                    date_start_work=:date_start_work, 
                    updated_at=now(),
                    profession_id=:profession,
                    date_birthday=:date_birthday,
                    avatar=:avatar
            WHERE id=:id 
            RETURNING id, first_name, last_name, middle_name, date_start_work, profession_id, date_birthday, avatar
            """
        )
        data['avatar'] = str(data['avatar'])
        result = await session.execute(query, {'id': id, **data})
        row = result.fetchone()
        if not row:
            raise BadRequestEx(detail='Failed to update a profession')
        (
            _,
            first_name,
            last_name,
            middle_name,
            date_start_work,
            profession_id,
            date_birthday,
            avatar,
        ) = row
        await session.commit()
        return DoctorData(
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            date_start_work=date_start_work,
            id=id,
            profession=profession_id,
            date_birthday=date_birthday,
            avatar=avatar,
        )


class DoctorAppointmentRepository(IDoctorAppointmentRepository):
    async def get_by_id(
        self, id: int, session: AsyncSession
    ) -> Optional[AppointmentResponse]:
        query = text(
            'SELECT m.id, m.start_date_appointment, m.end_date_appointment, m.doctor_id, m.client_id, m.created_at, m.updated_at '
            'FROM appointments m  '
            'WHERE m.id=:id '
        )
        result = await session.execute(query, {'id': id})
        row = result.first()
        if not row:
            return None
        (
            id,
            start_date_appointment,
            end_date_appointment,
            doctor_id,
            client_id,
            created_at,
            updated_at,
        ) = row
        return AppointmentResponse(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            start_date_appointment=start_date_appointment,
            end_date_appointment=end_date_appointment,
            doctor=doctor_id,
            client=client_id,
        )

    async def get_detail_by_id(
        self, id: int, session: AsyncSession
    ) -> Optional[AppointmentData]:
        query = text(
            """
            SELECT 
                m.id, m.start_date_appointment, m.end_date_appointment, 
                json_build_object('first_name', c.first_name, 'id', c.id, 'last_name', c.last_name, 'middle_name', c.middle_name, 'avatar', c.avatar) as client,
                json_build_object('first_name', d.first_name, 'id', d.id, 'last_name', d.last_name, 'middle_name', d.middle_name, 'avatar', c.avatar) as doctor,
                m.created_at, m.updated_at
            FROM appointments m
            INNER JOIN doctors d ON m.doctor_id = d.id
            INNER JOIN clients c ON m.client_id = c.id
            WHERE m.id=:id;
            """
        )
        result = await session.execute(query, {'id': id})
        row = result.first()
        if not row:
            return None
        (
            id,
            start_date_appointment,
            end_date_appointment,
            doctor,
            client,
            created_at,
            updated_at,
        ) = row
        return AppointmentData(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            start_date_appointment=start_date_appointment,
            end_date_appointment=end_date_appointment,
            doctor=doctor,
            client=client,
        )

    async def get_list(
        self,
        session: AsyncSession,
        limit: int,
        offset: int,
        query_params: 'QueryParamsAppointment',
    ) -> list[AppointmentData] | list:
        order = ''
        params: dict[str, Any] = {'limit': limit, 'offset': offset}
        filter = ''

        if query_params.order:
            match query_params.order:
                case 'start_date_appointment':
                    order = 'ORDER BY m.start_date_appointment ASC '
                case '-start_date_appointment':
                    order = 'ORDER BY m.start_date_appointment DESC '
                case 'end_date_appointment':
                    order = 'ORDER BY m.end_date_appointment ASC '
                case '-end_date_appointment':
                    order = 'ORDER BY m.end_date_appointment DESC '
                case '_':
                    pass

        if query_params.start_date and query_params.end_date:
            filter += ' WHERE m.start_date_appointment >= :start_date AND m.end_date_appointment <= :end_date'
            params['start_date'] = datetime.fromisoformat(
                query_params.start_date.strftime('%Y-%m-%dT%H:%M:%S')
            )
            params['end_date'] = datetime.fromisoformat(
                query_params.end_date.strftime('%Y-%m-%dT%H:%M:%S')
            )

        if query_params.doctor and not filter:
            filter += ' WHERE m.doctor_id = :doctor_id '
            params['doctor_id'] = query_params.doctor

        if query_params.doctor and filter:
            filter += ' AND m.doctor_id = :doctor_id '
            params['doctor_id'] = query_params.doctor

        if query_params.doctor and not filter:
            filter += ' WHERE m.client_id = :client_id '
            params['client_id'] = query_params.client

        if query_params.doctor and filter:
            filter += ' AND m.client_id = :client_id '
            params['client_id'] = query_params.client

        query = (
            """
            SELECT 
                m.id, m.start_date_appointment, m.end_date_appointment, 
                json_build_object('first_name', c.first_name, 'id', c.id, 'last_name', c.last_name, 'middle_name', c.middle_name, 'avatar', c.avatar) as client,
                json_build_object('first_name', d.first_name, 'id', d.id, 'last_name', d.last_name, 'middle_name', d.middle_name, 'avatar', c.avatar) as doctor,
                m.created_at, m.updated_at
            FROM appointments m
            INNER JOIN doctors d ON m.doctor_id = d.id
            INNER JOIN clients c ON m.client_id = c.id
            """
            f'{filter} '
            f'{order}'
            'LIMIT :limit OFFSET :offset '
        )
        result = await session.execute(text(query), params)
        rows = result.fetchall()
        appointments = []

        for row in rows:
            (
                id,
                start_date_appointment,
                end_date_appointment,
                doctor,
                client,
                created_at,
                updated_at,
            ) = row
            appointments.append(
                AppointmentData(
                    id=id,
                    created_at=created_at,
                    updated_at=updated_at,
                    start_date_appointment=start_date_appointment,
                    end_date_appointment=end_date_appointment,
                    doctor=doctor,
                    client=client,
                )
            )
        return appointments

    async def delete(self, id: int, session: AsyncSession) -> bool:
        query = text('DELETE FROM  appointments WHERE id=:id')
        await session.execute(query, {'id': id})
        await session.commit()
        return True

    async def create(
        self, data: AppointmentDataCreate, session: AsyncSession
    ) -> AppointmentResponse:
        query = text(
            'INSERT INTO appointments(created_at, updated_at, start_date_appointment, end_date_appointment, doctor_id, client_id) '
            'VALUES(now(), now(), :start_date_appointment, :end_date_appointment, :doctor, :client) '
            'RETURNING id, created_at, updated_at, start_date_appointment, end_date_appointment, doctor_id, client_id '
        )

        data['start_date_appointment'] = datetime.fromisoformat(
            data['start_date_appointment'].strftime('%Y-%m-%dT%H:%M:%S')
        )

        data['end_date_appointment'] = datetime.fromisoformat(
            data['end_date_appointment'].strftime('%Y-%m-%dT%H:%M:%S')
        )
        result = await session.execute(query, dict(data))
        row = result.fetchone()
        if not row:
            raise BadRequestEx(detail='Failed to create a appointment')
        await session.commit()
        (
            id,
            created_at,
            updated_at,
            start_date_appointment,
            end_date_appointment,
            doctor_id,
            client_id,
        ) = row
        return AppointmentResponse(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            start_date_appointment=start_date_appointment,
            end_date_appointment=end_date_appointment,
            doctor=doctor_id,
            client=client_id,
        )

    async def update(
        self, id: int, data: AppointmentDataCreate, session: AsyncSession
    ) -> AppointmentResponse:
        query = text(
            'UPDATE appointments SET  updated_at=now(), start_date_appointment=:start_date_appointment, end_date_appointment=:end_date_appointment, doctor_id=:doctor, client_id=:client '
            'WHERE id=:id RETURNING created_at, updated_at, start_date_appointment, end_date_appointment, doctor_id, client_id '
        )

        data['start_date_appointment'] = datetime.fromisoformat(
            data['start_date_appointment'].strftime('%Y-%m-%dT%H:%M:%S')
        )

        data['end_date_appointment'] = datetime.fromisoformat(
            data['end_date_appointment'].strftime('%Y-%m-%dT%H:%M:%S')
        )
        result = await session.execute(query, {'id': id, **data})
        row = result.fetchone()
        if not row:
            raise BadRequestEx(detail='Failed to update a appointment')
        (
            created_at,
            updated_at,
            start_date_appointment,
            end_date_appointment,
            doctor_id,
            client_id,
        ) = row
        await session.commit()
        return AppointmentResponse(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            start_date_appointment=start_date_appointment,
            end_date_appointment=end_date_appointment,
            doctor=doctor_id,
            client=client_id,
        )
