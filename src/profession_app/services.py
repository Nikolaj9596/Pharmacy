from typing import NoReturn, Optional
from sqlalchemy.exc import IntegrityError

from sqlalchemy.ext.asyncio import AsyncSession
from src.dependencies import Paginator, QueryParams
from src.exceptions import BadRequestEx, NotFoundEx
from src.profession_app.dtos import (
    ProfessionDataCreate,
    ProfessionDataDetailGet,
    ProfessionDataGet,
)
from src.profession_app.repositories import IProfessionRepository
from src.profession_app.schemes import (
    ProfessionCreateScheme,
    ProfessionDetailScheme,
    ProfessionScheme,
)


class ProfessionService:
    def __init__(self, repository: IProfessionRepository):
        self.repository = repository

    async def _check_exists(
        self, id: int, session: AsyncSession
    ) -> ProfessionDataGet | NoReturn:
        profession: Optional[
            ProfessionDataGet
        ] = await self.repository.get_by_id(id=id, session=session)
        if not profession:
            raise NotFoundEx(detail=f'Profession with id: {id} not found')
        return profession

    async def get_by_id(
        self, id: int, session: AsyncSession
    ) -> ProfessionScheme:
        profession = await self._check_exists(id=id, session=session)
        return ProfessionScheme(**profession)

    async def get_list(
        self,
        session: AsyncSession,
        pagination: Paginator,
        query_params: QueryParams,
    ) -> list[ProfessionScheme] | list:
        professions: list[
            ProfessionDataDetailGet
        ] | list = await self.repository.get_list(
            session=session, 
            limit=pagination.limit, 
            offset=pagination.offset,
            query_params=query_params
        )
        if not professions:
            return professions
        return [
            ProfessionDetailScheme(**profession) for profession in professions
        ]

    async def create(
        self, session: AsyncSession, data: ProfessionCreateScheme
    ) -> ProfessionScheme:
        try:
            profession: ProfessionDataGet = await self.repository.create(
                session=session, data=ProfessionDataCreate(**data.model_dump())
            )
        except IntegrityError:
            raise BadRequestEx(
                detail='There is already a profession with this name'
            )
        return ProfessionScheme(**profession)

    async def update(
        self, session: AsyncSession, data: ProfessionCreateScheme, id: int
    ) -> ProfessionScheme:
        profession = await self._check_exists(id=id, session=session)

        try:
            profession = await self.repository.update(
                session=session,
                data=ProfessionDataCreate(**data.model_dump()),
                id=id,
            )
        except IntegrityError:
            raise BadRequestEx(
                detail='There is already a profession with this name'
            )
        return ProfessionScheme(**profession)

    async def delete(self, id: int, session: AsyncSession) -> None:
        await self._check_exists(id=id, session=session)
        deleted = await self.repository.delete(session=session, id=id)
        if not deleted:
            raise BadRequestEx(detail='Failed to delete a profession')
        return None
