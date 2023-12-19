from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.dependencies import Paginator, QueryParams, get_session
from src.profession_app.dependencies import profession_service

from src.profession_app.schemes import ProfessionCreateScheme, ProfessionScheme
from src.profession_app.services import ProfessionService


profession_api = APIRouter(prefix='/professions')


@profession_api.get(
    '/',
    tags=['Профессия'],
    summary='Получить все профессии',
    response_model=list[ProfessionScheme] | list,
)
async def get_list(
    service: Annotated[ProfessionService, Depends(profession_service)],
    session: Annotated[AsyncSession, Depends(get_session)],
    pagination: Annotated[Paginator, Depends(Paginator)],
    query_params: Annotated[QueryParams, Depends(QueryParams)]
):
    professions: list[ProfessionScheme] | list = await service.get_list(
        session=session, pagination=pagination, query_params=query_params
    )
    return professions


@profession_api.get(
    '/{profession_id}',
    tags=['Профессия'],
    summary='Получить информацию о профессии',
    response_model=ProfessionScheme,
)
async def get_retrieve(
    profession_id: int,
    service: Annotated[ProfessionService, Depends(profession_service)],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    profession: ProfessionScheme = await service.get_by_id(
        id=profession_id, session=session
    )
    return profession


@profession_api.post(
    '/',
    tags=['Профессия'],
    summary='Создать профессию',
    response_model=ProfessionScheme,
)
async def create(
    service: Annotated[ProfessionService, Depends(profession_service)],
    session: Annotated[AsyncSession, Depends(get_session)],
    data: ProfessionCreateScheme,
):
    professions: ProfessionScheme = await service.create(
        session=session, data=data
    )
    return professions


@profession_api.patch(
    '/{profession_id}',
    tags=['Профессия'],
    summary='Обновление профессии',
    response_model=ProfessionScheme,
)
async def update(
    profession_id: int,
    service: Annotated[ProfessionService, Depends(profession_service)],
    session: Annotated[AsyncSession, Depends(get_session)],
    data: ProfessionCreateScheme,
):
    profession: Optional[ProfessionScheme] = await service.update(
        id=profession_id, session=session, data=data
    )
    return profession

@profession_api.delete(
    '/{profession_id}',
    tags=['Профессия'],
    summary='Удалить профессию',
)
async def delete(
    profession_id: int,
    service: Annotated[ProfessionService, Depends(profession_service)],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    await service.delete(
        id=profession_id, session=session
    )
    return Response(status_code=204, content=None)
