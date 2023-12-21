from typing import Annotated, Final
from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.dependencies import Paginator, QueryParams, get_session
from src.diagnosis_app.dependencies import category_disease_service

from src.diagnosis_app.schemes import (
    CategoryDiseaseCreateScheme,
    CategoryDiseaseScheme,
)
from src.diagnosis_app.services import CategoryDiseaseService


category_disease_api = APIRouter(prefix='/category_diseases')

TAG: Final[str] = 'Категории заболеваний'


@category_disease_api.get(
    '/',
    tags=[TAG],
    summary='Получить все категории заболеваний',
    response_model=list[CategoryDiseaseScheme] | list,
)
async def get_list(
    service: Annotated[
        CategoryDiseaseService, Depends(category_disease_service)
    ],
    session: Annotated[AsyncSession, Depends(get_session)],
    pagination: Annotated[Paginator, Depends(Paginator)],
    query_params: Annotated[QueryParams, Depends(QueryParams)],
):
    return await service.get_list(
        pagination=pagination, query_params=query_params, session=session
    )


@category_disease_api.get(
    '/{category_id}',
    tags=[TAG],
    summary='Получить категорию заболевании',
    response_model=CategoryDiseaseScheme,
)
async def get_retrieve(
    category_id: int,
    service: Annotated[
        CategoryDiseaseService, Depends(category_disease_service)
    ],
    session: Annotated[AsyncSession, Depends(get_session)],
):

    return await service.get_by_id(id=category_id, session=session)


@category_disease_api.post(
    '/',
    tags=[TAG],
    summary='Создать категорию заболеваний',
    response_model=CategoryDiseaseScheme,
)
async def create(
    service: Annotated[
        CategoryDiseaseService, Depends(category_disease_service)
    ],
    session: Annotated[AsyncSession, Depends(get_session)],
    data: CategoryDiseaseCreateScheme,
):
    return await service.create(session=session, data=data)


@category_disease_api.patch(
    '/{category_id}',
    tags=[TAG],
    summary='Обновить категорию заболеваний',
    response_model=CategoryDiseaseScheme,
)
async def update(
    category_id: int,
    service: Annotated[
        CategoryDiseaseService, Depends(category_disease_service)
    ],
    session: Annotated[AsyncSession, Depends(get_session)],
    data: CategoryDiseaseCreateScheme,
):
    return await service.update(id=category_id, session=session, data=data)


@category_disease_api.delete(
    '/{category_id}',
    tags=[TAG],
    summary='Удалить категорию заболеваний',
)
async def delete(
    category_id: int,
    service: Annotated[CategoryDiseaseService, Depends(category_disease_service)],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    await service.delete(id=category_id, session=session)
    return Response(status_code=204, content=None)
