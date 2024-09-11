from typing import Annotated, Final
from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.dependencies import Paginator, QueryParams, get_session
from src.diagnosis_app.dependencies import diagnosis_service
from src.diagnosis_app.schemes import DiagnosisCreateScheme, DiagnosisScheme
from src.diagnosis_app.services import DiagnosisService


diagnosis_api = APIRouter(prefix='/diagnosis')

TAG: Final[str] = 'Диагноз'


@diagnosis_api.get(
    '/',
    tags=[TAG],
    summary='Получить все диагнозы',
    response_model=list[DiagnosisScheme] | list,
)
async def get_list(
    service: Annotated[DiagnosisService, Depends(diagnosis_service)],
    session: Annotated[AsyncSession, Depends(get_session)],
    pagination: Annotated[Paginator, Depends(Paginator)],
    query_params: Annotated[QueryParams, Depends(QueryParams)],
):
    return await service.get_list(
        pagination=pagination, query_params=query_params, session=session
    )


@diagnosis_api.get(
    '/{diagnosis_id}',
    tags=[TAG],
    summary='Получить информацию о диагнозе',
    response_model=DiagnosisScheme,
)
async def get_retrieve(
    diagnosis_id: int,
    service: Annotated[DiagnosisService, Depends(diagnosis_service)],
    session: Annotated[AsyncSession, Depends(get_session)],
):

    return await service.get_by_id(id=diagnosis_id, session=session)


@diagnosis_api.post(
    '/',
    tags=[TAG],
    summary='Создать диагноз',
    response_model=DiagnosisCreateScheme,
)
async def create(
    service: Annotated[DiagnosisService, Depends(diagnosis_service)],
    session: Annotated[AsyncSession, Depends(get_session)],
    data: DiagnosisCreateScheme,
):
    return await service.create(session=session, data=data)


@diagnosis_api.patch(
    '/{diagnosis_id}',
    tags=[TAG],
    summary='Обновить диагноз',
    response_model=DiagnosisScheme,
)
async def update(
    diagnosis_id: int,
    service: Annotated[DiagnosisService, Depends(diagnosis_service)],
    session: Annotated[AsyncSession, Depends(get_session)],
    data: DiagnosisScheme,
):
    return await service.update(id=diagnosis_id, session=session, data=data)


@diagnosis_api.delete(
    '/{diagnosis_id}',
    tags=[TAG],
    summary='Удалить диагноз',
)
async def delete(
    diagnosis_id: int,
    service: Annotated[DiagnosisService, Depends(diagnosis_service)],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    await service.delete(id=diagnosis_id, session=session)
    return Response(status_code=204, content=None)
