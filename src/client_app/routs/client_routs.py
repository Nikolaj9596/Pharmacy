from typing import Annotated, Final, Optional
from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from src.client_app.dependencies import client_service
from src.client_app.schemes import ClientCreateScheme, ClientScheme
from src.client_app.services import ClientService
from src.dependencies import Paginator, QueryParams, get_session


client_api = APIRouter(prefix='/clients')

TAG: Final[str] = 'Поциент'


@client_api.get(
    '/',
    tags=[TAG],
    summary='Получить всех поциетов',
    response_model=list[ClientScheme] | list,
)
async def get_list(
    service: Annotated[ClientService, Depends(client_service)],
    session: Annotated[AsyncSession, Depends(get_session)],
    pagination: Annotated[Paginator, Depends(Paginator)],
    query_params: Annotated[QueryParams, Depends(QueryParams)],
):
    clients: list[ClientScheme] | list = await service.get_list(
        session=session, pagination=pagination, query_params=query_params
    )
    return clients


@client_api.get(
    '/{client_id}',
    tags=[TAG],
    summary='Получить информацию о враче',
    response_model=ClientScheme,
)
async def get_retrieve(
    client_id: int,
    service: Annotated[ClientService, Depends(client_service)],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    client: ClientScheme = await service.get_by_id(
        id=client_id, session=session
    )
    return client


@client_api.post(
    '/', tags=[TAG], summary='Создать врача', response_model=ClientScheme
)
async def create(
    service: Annotated[ClientService, Depends(client_service)],
    session: Annotated[AsyncSession, Depends(get_session)],
    data: ClientCreateScheme,
):
    client: ClientScheme = await service.create(session=session, data=data)
    return client


@client_api.patch(
    '/{client_id}',
    tags=[TAG],
    summary='Обновление информации о враче',
    response_model=ClientScheme,
)
async def update(
    client_id: int,
    service: Annotated[ClientService, Depends(client_service)],
    session: Annotated[AsyncSession, Depends(get_session)],
    data: ClientCreateScheme,
):
    client: Optional[ClientScheme] = await service.update(
        id=client_id, session=session, data=data
    )
    return client


@client_api.delete(
    '/{client_id}',
    tags=[TAG],
    summary='Удалить врача',
)
async def delete(
    client_id: int,
    service: Annotated[ClientService, Depends(client_service)],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    await service.delete(id=client_id, session=session)
    return Response(status_code=204, content=None)
