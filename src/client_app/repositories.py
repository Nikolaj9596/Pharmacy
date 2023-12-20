
from abc import ABC, abstractmethod
from typing import Any, Optional
from sqlalchemy import text

from sqlalchemy.ext.asyncio.session import AsyncSession

from src.client_app.dtos import ClientCreateData, ClientData
from src.dependencies import QueryParams
from src.exceptions import BadRequestEx


class IClientRepository(ABC):
    @abstractmethod
    async def get_by_id(
        self, id: int, session: AsyncSession
    ) -> Optional[ClientData]:
        raise NotImplementedError()

    @abstractmethod
    async def get_list(
        self,
        session: AsyncSession,
        limit: int,
        offset: int,
        query_params: QueryParams,
    ) -> list[ClientData] | list:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, id: int, session: AsyncSession) -> bool:
        raise NotImplementedError()

    @abstractmethod
    async def create(
        self, data: ClientCreateData, session: AsyncSession
    ) -> ClientData:
        raise NotImplementedError()

    @abstractmethod
    async def update(
        self, data: ClientCreateData, session: AsyncSession, id: int
    ) -> ClientData:
        raise NotImplementedError()

class ClientRepository(IClientRepository):

    async def get_by_id(
        self, id: int, session: AsyncSession
    ) -> Optional[ClientData]:
        query = text(
            'SELECT c.id, c.first_name, c.last_name, c.middle_name, c.date_birthday, address, created_at, updated_at '
            'FROM client c  '
            'WHERE c.id=:id'
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
            date_birthday,
            address,
            created_at,
            updated_at,
        ) = row
        return ClientData(
            id=id,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            date_birthday=date_birthday,
            address=address,
            created_at=created_at,
            updated_at=updated_at,
        )

    async def get_list(
        self,
        session: AsyncSession,
        limit: int,
        offset: int,
        query_params: QueryParams,
    ) -> list[ClientData] | list:
        order = ''
        search = ''
        params: dict[str, Any] = {'limit': limit, 'offset': offset}

        if query_params.search:
            search = 'WHERE c.first_name OR c.last_name OR c.middle_name LIKE :search '
            params['search'] = query_params.search

        if query_params.order:
            match query_params.order:
                case 'last_name':
                    order = 'ORDER BY c.last_name ASC '
                case '-last_name':
                    order = 'ORDER BY c.last_name DESC '
                case 'created_at':
                    order = 'ORDER BY c.created_at ASC '
                case '-created_at':
                    order = 'ORDER BY c.created_at DESC '
                case '_':
                    pass
        query = (
            'SELECT c.id, c.first_name, c.last_name, c.middle_name, c.date_birthday, c.address, c.created_at, c.updated_at '
            'FROM client c  '
            f'{search} '
            f'{order}'
            'LIMIT :limit OFFSET :offset '
        )
        result = await session.execute(text(query), params)
        rows = result.fetchall()
        appointments = []

        for row in rows:
            (
                id,
                first_name,
                last_name,
                middle_name,
                date_birthday,
                address,
                created_at,
                updated_at,
            ) = row
            appointments.append(
                ClientData(
                    id=id,
                    first_name=first_name,
                    last_name=last_name,
                    middle_name=middle_name,
                    date_birthday=date_birthday,
                    address=address,
                    created_at=created_at,
                    updated_at=updated_at,
                )
            )
        return appointments

    async def delete(self, id: int, session: AsyncSession) -> bool:
        query = text('DELETE FROM client WHERE id=:id')
        await session.execute(query, {'id': id})
        await session.commit()
        return True

    async def create(
        self, data: ClientCreateData, session: AsyncSession
    ) -> ClientData:
        query = text(
            'INSERT INTO client(first_name, last_name, middle_name, date_birthday, address, created_at, updated_at) '
            'VALUES(:first_name, :last_name, :middle_name, :date_birthday, :address, now(), now()) '
            'RETURNING id, first_name, last_name, middle_name, date_birthday, address, created_at, updated_at '
        )
        result = await session.execute(query, dict(data))
        row = result.fetchone()
        if not row:
            raise BadRequestEx(detail='Failed to create a client')
        await session.commit()
        (
            id,
            first_name,
            last_name,
            middle_name,
            date_birthday,
            address,
            created_at,
            updated_at,
        ) = row
        return ClientData(
            id=id,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            date_birthday=date_birthday,
            address=address,
            created_at=created_at,
            updated_at=updated_at,
        )

    async def update(
        self, id: int, data: ClientCreateData, session: AsyncSession
    ) -> ClientData:
        query = text(
            'UPDATE client SET first_name=:first_name, last_name=:last_name, middle_name=:middle_name, date_birthday=:date_birthday, address=:address, updated_at=now() '
            'WHERE id=:id RETURNING first_name, last_name, middle_name, date_birthday, address, created_at, updated_at '
        )
        result = await session.execute(query, {'id': id, **data})
        row = result.fetchone()
        if not row:
            raise BadRequestEx(detail='Failed to update a client')
        await session.commit()
        (
            first_name,
            last_name,
            middle_name,
            date_birthday,
            address,
            created_at,
            updated_at,
        ) = row
        return ClientData(
            id=id,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            date_birthday=date_birthday,
            address=address,
            created_at=created_at,
            updated_at=updated_at,
        )
