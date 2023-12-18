from typing import Annotated, Optional
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.dependencies import get_session
from src.profession_app.dependencies import profession_service

from src.profession_app.schemes import ProfessionScheme
from src.profession_app.services import ProfessionService


profession_api = APIRouter(prefix='/professions')


@profession_api.get(
    '/{profession_id}',
    tags=['Профессия'],
    summary='Получить информацию о профессии',
    response_model=ProfessionScheme,
)
async def get_profession(
    profession_id: int,
    service: Annotated[ProfessionService, Depends(profession_service)],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    profession: Optional[ProfessionScheme] = await service.get_by_id(
        id=profession_id, session=session
    )
    print(f'{profession=}')
    if not profession:
        return JSONResponse(
            status_code=404,
            content={
                'detail': f'Profession with id: {profession_id} not found'
            },
        )
    return JSONResponse(status_code=200, content=profession)
