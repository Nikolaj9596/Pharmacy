__all__ = ['appointment_api']

from typing import Annotated, Final, Optional
from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from src.dependencies import Paginator, get_session, QueryParamsAppointment
from src.doctor_app.schemes import (
    AppointmentCreateScheme,
    AppointmentScheme,
)
from src.doctor_app.dependencies import (
    appointment_service,
)
from src.doctor_app.services import AppointmentService


appointment_api = APIRouter(prefix='/appointments')

TAG: Final[str] = 'Запись на прием'


@appointment_api.get(
    '/',
    tags=[TAG],
    summary='Получить все записи на прием',
    response_model=list[AppointmentScheme] | list,
)
async def get_list(
    service: Annotated[AppointmentService, Depends(appointment_service)],
    session: Annotated[AsyncSession, Depends(get_session)],
    pagination: Annotated[Paginator, Depends(Paginator)],
    query_params: Annotated[
        QueryParamsAppointment, Depends(QueryParamsAppointment)
    ],
):
    appointments: list[AppointmentScheme] | list = await service.get_list(
        session=session, pagination=pagination, query_params=query_params
    )
    return appointments


@appointment_api.get(
    '/{appointment_id}',
    tags=[TAG],
    summary='Получить информацию о записи на прием',
    response_model=AppointmentScheme,
)
async def get_retrieve(
    appointment_id: int,
    service: Annotated[AppointmentService, Depends(appointment_service)],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    appointment: AppointmentScheme = await service.get_by_id(
        id=appointment_id, session=session
    )
    return appointment


@appointment_api.post(
    '/',
    tags=[TAG],
    summary='Создать запись на прием',
    response_model=AppointmentCreateScheme,
)
async def create(
    service: Annotated[AppointmentService, Depends(appointment_service)],
    session: Annotated[AsyncSession, Depends(get_session)],
    data: AppointmentCreateScheme,
):
    appointment: AppointmentCreateScheme = await service.create(
        session=session, data=data
    )
    return appointment


@appointment_api.patch(
    '/{appointment_id}',
    tags=[TAG],
    summary='Обновление записи на прием',
    response_model=AppointmentScheme,
)
async def update(
    appointment_id: int,
    service: Annotated[AppointmentService, Depends(appointment_service)],
    session: Annotated[AsyncSession, Depends(get_session)],
    data: AppointmentCreateScheme,
):
    appointment: Optional[AppointmentScheme] = await service.update(
        id=appointment_id, session=session, data=data
    )
    return appointment


@appointment_api.delete(
    '/{appointment_id}',
    tags=[TAG],
    summary='Удалить запись на прием',
)
async def delete(
    appointment_id: int,
    service: Annotated[AppointmentService, Depends(appointment_service)],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    await service.delete(id=appointment_id, session=session)
    return Response(status_code=204, content=None)
