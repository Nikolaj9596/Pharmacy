from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from src.profession_app.dtos import ProfessionDataGet
from src.profession_app.repositories import IProfessionRepository
from src.profession_app.schemes import ProfessionScheme


class ProfessionService:
    def __init__(self, repository: IProfessionRepository):
        self.repository = repository

    async def get_by_id(
        self, id: int, session: AsyncSession
    ) -> Optional[ProfessionScheme]:
        profession: Optional[
            ProfessionDataGet
        ] = await self.repository.get_by_id(id=id, session=session)
        if not profession:
            return None
        return ProfessionScheme(**profession)
