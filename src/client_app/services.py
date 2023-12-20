from typing import Optional
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.client_app.dtos import ClientCreateData, ClientData
from src.client_app.repositories import IClientRepository
from src.client_app.schemes import ClientCreateScheme, ClientScheme
from src.dependencies import Paginator, QueryParams
from src.exceptions import BadRequestEx, NotFoundEx


class ClientService:
    def __init__(self, repository: IClientRepository):
        self.repository = repository

    async def _check_exists(
        self, id: int, session: AsyncSession
    ) -> ClientData:
        client: Optional[ClientData] = await self.repository.get_by_id(
            id=id, session=session
        )
        if not client:
            raise NotFoundEx(detail=f'Client with id: {id} not found')
        return client

    async def get_by_id(self, id: int, session: AsyncSession) -> ClientScheme:
        client: Optional[ClientData] = await self.repository.get_by_id(
            id=id, session=session
        )
        if not client:
            raise NotFoundEx(detail=f'Client with id: {id} not found')
        return ClientScheme(**client)

    async def get_list(
        self,
        session: AsyncSession,
        pagination: Paginator,
        query_params: QueryParams,
    ) -> list[ClientScheme] | list:
        clients: list[ClientData] | list = await self.repository.get_list(
            session=session,
            limit=pagination.limit,
            offset=pagination.offset,
            query_params=query_params,
        )
        if not clients:
            return clients
        return [ClientScheme(**client) for client in clients]

    async def create(
        self, session: AsyncSession, data: ClientCreateScheme
    ) -> ClientScheme:
        try:
            client: ClientData = await self.repository.create(
                session=session, data=ClientCreateData(**data.model_dump())
            )
        except IntegrityError:
            raise BadRequestEx(
                detail='There is already a client with this first_name, last_name, middle_name'
            )
        return ClientScheme(**client)

    async def update(
        self, session: AsyncSession, data: ClientCreateScheme, id: int
    ) -> ClientScheme:
        await self._check_exists(id=id, session=session)
        try:
            client = await self.repository.update(
                session=session,
                data=ClientCreateData(**data.model_dump()),
                id=id,
            )
        except IntegrityError:
            raise BadRequestEx(
                detail='There is already a client with this first_name, last_name, middle_name'
            )
        return ClientScheme(**client)

    async def delete(self, id: int, session: AsyncSession) -> None:
        await self._check_exists(id=id, session=session)
        deleted = await self.repository.delete(session=session, id=id)
        if not deleted:
            raise BadRequestEx(detail='Failed to delete a client')
        return None

