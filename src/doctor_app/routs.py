from typing import Annotated, Final, Optional
from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from src.dependencies import Paginator, QueryParams, get_session
from src.doctor_app.schemes import DoctorCreateScheme, DoctorDetailScheme, DoctorScheme
from src.doctor_app.dependencies import doctor_service
from src.doctor_app.services import DoctorService 



doctor_api = APIRouter(prefix='/doctors')
TAG: Final[str] = 'Врач'


@doctor_api.get(
    '/',
    tags=[TAG],
    summary='Получить всех врачей',
    response_model=list[DoctorScheme] | list,
)
async def get_list(
    service: Annotated[DoctorService, Depends(doctor_service)],
    session: Annotated[AsyncSession, Depends(get_session)],
    pagination: Annotated[Paginator, Depends(Paginator)],
    query_params: Annotated[QueryParams, Depends(QueryParams)]
):
    doctors: list[DoctorScheme] | list = await service.get_list(
        session=session, pagination=pagination, query_params=query_params
    )
    return doctors


@doctor_api.get(
    '/{doctor_id}',
    tags=[TAG],
    summary='Получить информацию о враче',
    response_model=DoctorDetailScheme,
)
async def get_retrieve(
    profession_id: int,
    service: Annotated[DoctorService, Depends(doctor_service)],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    doctor: DoctorDetailScheme = await service.get_by_id(
        id=profession_id, session=session
    )
    return doctor 


@doctor_api.post(
    '/',
    tags=[TAG],
    summary='Создать врача',
    response_model=DoctorScheme,
)
async def create(
    service: Annotated[DoctorService, Depends(doctor_service)],
    session: Annotated[AsyncSession, Depends(get_session)],
    data: DoctorCreateScheme,
):
    doctor: DoctorScheme = await service.create(
        session=session, data=data
    )
    return doctor


@doctor_api.patch(
    '/{doctor_id}',
    tags=[TAG],
    summary='Обновление информации о враче',
    response_model=DoctorScheme,
)
async def update(
    doctor_id: int,
    service: Annotated[DoctorService, Depends(doctor_service)],
    session: Annotated[AsyncSession, Depends(get_session)],
    data: DoctorCreateScheme,
):
    doctor: Optional[DoctorScheme] = await service.update(
        id=doctor_id, session=session, data=data
    )
    return doctor

@doctor_api.delete(
    '/{doctor_id}',
    tags=[TAG],
    summary='Удалить врача',
)
async def delete(
    doctor_id: int,
    service: Annotated[DoctorService, Depends(doctor_service)],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    await service.delete(
        id=doctor_id, session=session
    )
    return Response(status_code=204, content=None)
