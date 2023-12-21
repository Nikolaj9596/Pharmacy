from typing import Optional
from sqlalchemy import text
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.dependencies import Paginator, QueryParams
from src.diagnosis_app.dtos import CategoryDiseaseData, DiagnosisCreateData, DiagnosisData, DiseaseCreateData, DiseaseData
from src.diagnosis_app.repositories import (
    ICategoryDiseaseRepository,
    IDiagnosisRepository,
    IDiseaseRepository,
)
from src.diagnosis_app.schemes import (
    CategoryDiseaseCreateScheme,
    CategoryDiseaseScheme,
    DiagnosisCreateScheme,
    DiagnosisScheme,
    DiseaseCreateScheme,
    DiseaseScheme,
)
from src.exceptions import BadRequestEx, NotFoundEx


class CategoryDiseaseService:
    def __init__(self, repository: ICategoryDiseaseRepository):
        self.repository = repository

    async def _check_exists(
        self, id: int, session: AsyncSession
    ) -> CategoryDiseaseData:
        category_disease: Optional[
            CategoryDiseaseData
        ] = await self.repository.get_by_id(id=id, session=session)
        if not category_disease:
            raise NotFoundEx(
                detail=f'Category Disease with id: {id} not found'
            )
        return category_disease

    async def get_by_id(
        self, id: int, session: AsyncSession
    ) -> CategoryDiseaseScheme:
        category: Optional[
            CategoryDiseaseData
        ] = await self.repository.get_by_id(id=id, session=session)
        if not category:
            raise NotFoundEx(detail=f'CategoryDisease with id: {id} not found')
        return CategoryDiseaseScheme(**category)

    async def get_list(
        self,
        session: AsyncSession,
        pagination: Paginator,
        query_params: QueryParams,
    ) -> list[CategoryDiseaseScheme] | list:
        categories: list[
            CategoryDiseaseScheme
        ] | list = await self.repository.get_list(
            session=session,
            limit=pagination.limit,
            offset=pagination.offset,
            query_params=query_params,
        )
        if not categories:
            return categories
        return [CategoryDiseaseScheme(**category) for category in categories]

    async def create(
        self, session: AsyncSession, data: CategoryDiseaseCreateScheme
    ) -> CategoryDiseaseScheme:
        category: CategoryDiseaseData = await self.repository.create(
            session=session, data=CategoryDiseaseData(**data.model_dump())
        )
        return CategoryDiseaseScheme(**category)

    async def update(
        self, session: AsyncSession, data: CategoryDiseaseCreateScheme, id: int
    ) -> CategoryDiseaseScheme:
        await self._check_exists(id=id, session=session)
        category = await self.repository.update(
            session=session,
            data=CategoryDiseaseData(**data.model_dump()),
            id=id,
        )
        return CategoryDiseaseScheme(**category)

    async def delete(self, id: int, session: AsyncSession) -> None:
        await self._check_exists(id=id, session=session)
        deleted = await self.repository.delete(session=session, id=id)
        if not deleted:
            raise BadRequestEx(detail='Failed to delete a category disease')
        return None


class DiseaseService:
    def __init__(self, repository: IDiseaseRepository):
        self.repository = repository

    async def _check_exists(
        self, id: int, session: AsyncSession
    ) -> DiseaseData:
        disease: Optional[DiseaseData] = await self.repository.get_by_id(
            id=id, session=session
        )
        if not disease:
            raise NotFoundEx(detail=f'Disease with id: {id} not found')
        return disease

    async def _check_category_exists(
        self, id: int, session: AsyncSession
    ) -> bool:

        query = text('SELECT cd.id FROM category_disease cd WHERE cd.id=:id')
        result = await session.execute(query, {'id': id})
        row = result.first()
        if not row:
            raise NotFoundEx(detail=f'Category Disease with id: {id} not found')
        return True

    async def get_by_id(self, id: int, session: AsyncSession) -> DiseaseScheme:
        disease: Optional[DiseaseData] = await self.repository.get_by_id(
            id=id, session=session
        )
        if not disease:
            raise NotFoundEx(detail=f'Disease with id: {id} not found')
        return DiseaseScheme(**disease)

    async def get_list(
        self,
        session: AsyncSession,
        pagination: Paginator,
        query_params: QueryParams,
    ) -> list[DiseaseScheme] | list:
        diseases: list[DiseaseData] | list = await self.repository.get_list(
            session=session,
            limit=pagination.limit,
            offset=pagination.offset,
            query_params=query_params,
        )
        if not diseases:
            return diseases
        return [DiseaseScheme(**disease) for disease in diseases]

    async def create(
        self, session: AsyncSession, data: DiseaseCreateScheme
    ) -> DiseaseScheme:
        await self._check_category_exists(id=data.category_disease_id, session=session)
        disease: DiseaseData = await self.repository.create(
            session=session, data=DiseaseCreateData(**data.model_dump())
        )
        return DiseaseScheme(**disease)

    async def update(
        self, session: AsyncSession, data: DiseaseCreateScheme, id: int
    ) -> DiseaseScheme:
        await self._check_exists(id=id, session=session)
        await self._check_category_exists(id=data.category_disease_id, session=session)
        disease = await self.repository.update(
            session=session,
            data=DiseaseCreateData(**data.model_dump()),
            id=id,
        )
        return DiseaseScheme(**disease)

    async def delete(self, id: int, session: AsyncSession) -> None:
        await self._check_exists(id=id, session=session)
        deleted = await self.repository.delete(session=session, id=id)
        if not deleted:
            raise BadRequestEx(detail='Failed to delete a disease')
        return None


class DiagnosisService:
    def __init__(self, repository: IDiagnosisRepository):
        self.repository = repository

    async def _check_exists(
        self, id: int, session: AsyncSession
    ) -> DiagnosisData:
        diagnosis: Optional[DiagnosisData] = await self.repository.get_by_id(
            id=id, session=session
        )
        if not diagnosis:
            raise NotFoundEx(detail=f'Diagnosis with id: {id} not found')
        return diagnosis

    async def _check_client_exists(
        self, id: int, session: AsyncSession
    ) -> bool:

        query = text('SELECT c.id FROM client c WHERE c.id=:id')
        result = await session.execute(query, {'id': id})
        row = result.first()
        if not row:
            raise NotFoundEx(detail=f'Client with id: {id} not found')
        return True

    async def _check_doctor_exists(
        self, id: int, session: AsyncSession
    ) -> bool:

        query = text('SELECT d.id FROM doctor d WHERE d.id=:id')
        result = await session.execute(query, {'id': id})
        row = result.first()
        if not row:
            raise NotFoundEx(detail=f'Doctor with id: {id} not found')
        return True

    async def get_by_id(self, id: int, session: AsyncSession) -> DiagnosisScheme:
        diagnosis: Optional[DiagnosisData] = await self.repository.get_by_id(
            id=id, session=session
        )
        if not diagnosis:
            raise NotFoundEx(detail=f'Disease with id: {id} not found')
        return DiagnosisScheme(**diagnosis)

    async def get_list(
        self,
        session: AsyncSession,
        pagination: Paginator,
        query_params: QueryParams,
    ) -> list[DiagnosisScheme] | list:
        diagnosis: list[DiagnosisData] | list = await self.repository.get_list(
            session=session,
            limit=pagination.limit,
            offset=pagination.offset,
            query_params=query_params,
        )
        if not diagnosis:
            return diagnosis
        return [DiagnosisScheme(**d) for d in diagnosis]

    async def create(
        self, session: AsyncSession, data: DiagnosisCreateScheme 
    ) -> DiagnosisScheme:
        await self._check_client_exists(id=data.client_id, session=session)
        await self._check_doctor_exists(id=data.doctor_id, session=session)
        diagnosis: DiagnosisData = await self.repository.create(
            session=session, data=DiagnosisCreateData(**data.model_dump())
        )
        return DiagnosisScheme(**diagnosis)

    async def update(
        self, session: AsyncSession, data: DiagnosisCreateScheme, id: int
    ) -> DiagnosisScheme:
        await self._check_exists(id=id, session=session)
        await self._check_client_exists(id=data.client_id, session=session)
        await self._check_doctor_exists(id=data.doctor_id, session=session)
        diagnosis = await self.repository.update(
            session=session,
            data=DiagnosisCreateData(**data.model_dump()),
            id=id,
        )
        return DiagnosisScheme(**diagnosis)

    async def delete(self, id: int, session: AsyncSession) -> None:
        await self._check_exists(id=id, session=session)
        deleted = await self.repository.delete(session=session, id=id)
        if not deleted:
            raise BadRequestEx(detail='Failed to delete a diagnosis')
        return None
