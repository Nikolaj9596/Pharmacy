from typing import Annotated, Final
from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.dependencies import Paginator, QueryParams, get_session
from src.diagnosis_app.dependencies import disease_service
from src.diagnosis_app.schemes import DiseaseCreateScheme, DiseaseResponseScheme, DiseaseScheme
from src.diagnosis_app.services import DiseaseService



disease_api = APIRouter(prefix='/diseases')

TAG: Final[str] = 'Заболевания'


@disease_api.get(
    '/',
    tags=[TAG],
    summary='Получить все заболевания',
    response_model=list[DiseaseScheme] | list,
)
async def get_list(
    service: Annotated[
        DiseaseService, Depends(disease_service)
    ],
    session: Annotated[AsyncSession, Depends(get_session)],
    pagination: Annotated[Paginator, Depends(Paginator)],
    query_params: Annotated[QueryParams, Depends(QueryParams)],
):
    return await service.get_list(
        pagination=pagination, query_params=query_params, session=session
    )


@disease_api.get(
    '/{disease_id}',
    tags=[TAG],
    summary='Получить заболевание',
    response_model=DiseaseScheme,
)
async def get_retrieve(
    disease_id: int,
    service: Annotated[
        DiseaseService, Depends(disease_service)
    ],
    session: Annotated[AsyncSession, Depends(get_session)],
):

    return await service.get_by_id(id=disease_id, session=session)


@disease_api.post(
    '/',
    tags=[TAG],
    summary='Создать заболевание',
    response_model=DiseaseResponseScheme,
)
async def create(
    service: Annotated[
        DiseaseService, Depends(disease_service)
    ],
    session: Annotated[AsyncSession, Depends(get_session)],
    data: DiseaseCreateScheme,
):
    return await service.create(session=session, data=data)


@disease_api.patch(
    '/{disease_id}',
    tags=[TAG],
    summary='Обновить заболевание',
    response_model=DiseaseResponseScheme,
)
async def update(
    disease_id: int,
    service: Annotated[
        DiseaseService, Depends(disease_service)
    ],
    session: Annotated[AsyncSession, Depends(get_session)],
    data: DiseaseCreateScheme,
):
    return await service.update(id=disease_id, session=session, data=data)


@disease_api.delete(
    '/{disease_id}',
    tags=[TAG],
    summary='Удалить заболевание',
)
async def delete(
    disease_id: int,
    service: Annotated[DiseaseService, Depends(disease_service)],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    await service.delete(id=disease_id, session=session)
    return Response(status_code=204, content=None)
