from abc import ABC, abstractmethod
from typing import Any, Optional
from sqlalchemy import text

from sqlalchemy.ext.asyncio.session import AsyncSession
from src.dependencies import QueryParams

from src.diagnosis_app.dtos import (
    CategoryDiseaseCreateData,
    CategoryDiseaseData,
    DiagnosisCreateData,
    DiagnosisData,
    DiseaseCreateData,
    DiseaseData,
)
from src.exceptions import BadRequestEx


class ICategoryDiseaseRepository(ABC):
    @abstractmethod
    async def get_by_id(
        self, id: int, session: AsyncSession
    ) -> Optional[CategoryDiseaseData]:
        raise NotImplementedError()

    @abstractmethod
    async def get_list(
        self,
        session: AsyncSession,
        limit: int,
        offset: int,
        query_params: QueryParams,
    ) -> list[CategoryDiseaseData] | list:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, id: int, session: AsyncSession) -> bool:
        raise NotImplementedError()

    @abstractmethod
    async def create(
        self, data: CategoryDiseaseCreateData, session: AsyncSession
    ) -> CategoryDiseaseData:
        raise NotImplementedError()

    @abstractmethod
    async def update(
        self, data: CategoryDiseaseCreateData, session: AsyncSession, id: int
    ) -> CategoryDiseaseData:
        raise NotImplementedError()


class IDiseaseRepository(ABC):
    @abstractmethod
    async def get_by_id(
        self, id: int, session: AsyncSession
    ) -> Optional[DiseaseData]:
        raise NotImplementedError()

    @abstractmethod
    async def get_list(
        self,
        session: AsyncSession,
        limit: int,
        offset: int,
        query_params: QueryParams,
    ) -> list[DiseaseData] | list:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, id: int, session: AsyncSession) -> bool:
        raise NotImplementedError()

    @abstractmethod
    async def create(
        self, data: DiseaseCreateData, session: AsyncSession
    ) -> DiseaseData:
        raise NotImplementedError()

    @abstractmethod
    async def update(
        self, data: DiseaseCreateData, session: AsyncSession, id: int
    ) -> DiseaseData:
        raise NotImplementedError()


class IDiagnosisRepository(ABC):
    @abstractmethod
    async def get_by_id(
        self, id: int, session: AsyncSession
    ) -> Optional[DiagnosisData]:
        raise NotImplementedError()

    @abstractmethod
    async def get_list(
        self,
        session: AsyncSession,
        limit: int,
        offset: int,
        query_params: QueryParams,
    ) -> list[DiagnosisData] | list:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, id: int, session: AsyncSession) -> bool:
        raise NotImplementedError()

    @abstractmethod
    async def create(
        self, data: DiagnosisCreateData, session: AsyncSession
    ) -> DiagnosisData:
        raise NotImplementedError()

    @abstractmethod
    async def update(
        self, data: DiagnosisCreateData, session: AsyncSession, id: int
    ) -> DiagnosisData:
        raise NotImplementedError()


class CategoryDiseaseRepository(ICategoryDiseaseRepository):
    async def get_by_id(
        self, id: int, session: AsyncSession
    ) -> Optional[CategoryDiseaseData]:
        query = text(
            'SELECT cd.name ' 'FROM categories_disease cd  ' 'WHERE cd.id=:id '
        )
        result = await session.execute(query, {'id': id})
        row = result.first()
        if not row:
            return None
        (name,) = row
        return CategoryDiseaseData(id=id, name=name)

    async def get_list(
        self,
        session: AsyncSession,
        limit: int,
        offset: int,
        query_params: QueryParams,
    ) -> list[CategoryDiseaseData] | list:
        order = ''
        params: dict[str, Any] = {'limit': limit, 'offset': offset}

        if query_params.order:
            match query_params.order:
                case 'created_at':
                    order = 'ORDER BY cd.created_at ASC '
                case '-created_at':
                    order = 'ORDER BY cd.created_at DESC '
                case '_':
                    pass

        query = (
            'SELECT cd.id, cd.name '
            'FROM categories_disease cd  '
            f'{order}'
            'LIMIT :limit OFFSET :offset '
        )
        result = await session.execute(text(query), params)
        rows = result.fetchall()
        catalogs = []

        for row in rows:
            (id, name) = row
            catalogs.append(CategoryDiseaseData(id=id, name=name))
        return catalogs

    async def delete(self, id: int, session: AsyncSession) -> bool:
        query = text('DELETE FROM  categories_disease WHERE id=:id')
        await session.execute(query, {'id': id})
        await session.commit()
        return True

    async def create(
        self, data: CategoryDiseaseCreateData, session: AsyncSession
    ) -> CategoryDiseaseData:
        query = text(
            'INSERT INTO categories_disease(name, created_at, updated_at) '
            'VALUES(:name, now(), now()) '
            'RETURNING id, name '
        )
        result = await session.execute(query, dict(data))
        row = result.fetchone()
        if not row:
            raise BadRequestEx(detail='Failed to create a category disease')
        await session.commit()
        (id, name) = row
        return CategoryDiseaseData(id=id, name=name)

    async def update(
        self, id: int, data: CategoryDiseaseCreateData, session: AsyncSession
    ) -> CategoryDiseaseData:
        query = text(
            'UPDATE categories_disease SET updated_at=now(), name=:name '
            'WHERE id=:id RETURNING name '
        )
        result = await session.execute(query, {'id': id, **data})
        row = result.fetchone()
        if not row:
            raise BadRequestEx(detail='Failed to update a category disease')
        (name) = row
        await session.commit()
        return CategoryDiseaseData(id=id, name=name)


class DiseaseRepository(IDiseaseRepository):
    async def get_by_id(
        self, id: int, session: AsyncSession
    ) -> Optional[DiseaseData]:
        query = text(
            """
                SELECT 
                    d.name, d.description, 
                    json_build_object('name', cd.name, 'id', cd.id) as category_disease
                FROM diseases d
                LEFT JOIN categories_disease cd ON d.category_disease_id=cd.id
                WHERE d.id=:id

            """
        )
        result = await session.execute(query, {'id': id})
        row = result.first()
        if not row:
            return None
        (name, description, category_disease) = row
        return DiseaseData(
            id=id,
            name=name,
            description=description,
            category_disease=category_disease,
        )

    async def get_list(
        self,
        session: AsyncSession,
        limit: int,
        offset: int,
        query_params: QueryParams,
    ) -> list[DiseaseData] | list:
        order = ''
        search = ''
        params: dict[str, Any] = {'limit': limit, 'offset': offset}

        if query_params.order:
            match query_params.order:
                case 'created_at':
                    order = 'ORDER BY d.created_at ASC '
                case '-created_at':
                    order = 'ORDER BY d.created_at DESC '
                case '_':
                    pass

        if query_params.search:
            search = 'WHERE d.name LiKE :search '
            params['search'] = search
        query = (
            "SELECT d.id, d.name as new_name, d.description, json_build_object('name', cd.name, 'id', cd.id) as category_disease "
            'FROM diseases d  '
            'LEFT JOIN categories_disease cd ON d.category_disease_id=cd.id '
            f'{search}'
            f'{order}'
            'LIMIT :limit OFFSET :offset '
        )
        result = await session.execute(text(query), params)
        rows = result.fetchall()
        diseases = []

        for row in rows:
            (id, name, description, category_disease) = row
            diseases.append(
                DiseaseData(
                    id=id,
                    name=name,
                    description=description,
                    category_disease=category_disease,
                )
            )
        return diseases

    async def delete(self, id: int, session: AsyncSession) -> bool:
        query = text('DELETE FROM  diseases WHERE id=:id')
        await session.execute(query, {'id': id})
        await session.commit()
        return True

    async def create(
        self, data: DiseaseCreateData, session: AsyncSession
    ) -> dict[str, Any]:
        query = text(
            'INSERT INTO diseases(name, description, category_disease_id, created_at, updated_at) '
            'VALUES(:name, :description, :category_disease, now(), now()) '
            'RETURNING id, name, description, category_disease_id'
        )
        result = await session.execute(query, dict(data))
        row = result.fetchone()
        if not row:
            raise BadRequestEx(detail='Failed to create a disease')
        await session.commit()
        (
            id,
            name,
            description,
            category_disease,
        ) = row
        return dict(
            id=id,
            name=name,
            description=description,
            category_disease=category_disease,
        )

    async def update(
        self, id: int, data: DiseaseCreateData, session: AsyncSession
    ) -> dict[str, Any]:
        query = text(
            'UPDATE diseases SET  updated_at=now(), name=:name, description=:description, category_disease_id=:category_disease '
            'WHERE id=:id RETURNING name, description, category_disease_id '
        )
        result = await session.execute(query, {'id': id, **data})
        row = result.fetchone()
        if not row:
            raise BadRequestEx(detail='Failed to update a disease')
        (
            name,
            description,
            category_disease,
        ) = row
        await session.commit()
        return dict(
            id=id,
            name=name,
            description=description,
            category_disease=category_disease,
        )


class DiagnosisRepository(IDiagnosisRepository):
    async def get_by_id(
        self, id: int, session: AsyncSession
    ) -> Optional[DiagnosisData]:
        query = text(
            'SELECT d.name, d.description, d.date_closed, d.status, d.client_id, d.doctor_id '
            'FROM diagnosis d '
            'WHERE d.id=:id '
        )
        result = await session.execute(query, {'id': id})
        row = result.first()
        if not row:
            return None
        (name, description, date_closed, status, client_id, doctor_id) = row
        return DiagnosisData(
            id=id,
            name=name,
            description=description,
            date_closed=date_closed,
            status=status,
            client_id=client_id,
            doctor_id=doctor_id,
        )

    async def get_list(
        self,
        session: AsyncSession,
        limit: int,
        offset: int,
        query_params: QueryParams,
    ) -> list[DiagnosisData] | list:
        order = ''
        search = ''
        params: dict[str, Any] = {'limit': limit, 'offset': offset}

        if query_params.order:
            match query_params.order:
                case 'created_at':
                    order = 'ORDER BY d.created_at ASC '
                case '-created_at':
                    order = 'ORDER BY d.created_at DESC '
                case '_':
                    pass

        if query_params.search:
            search = 'WHERE d.name LiKE :search '
            params['search'] = search

        query = (
            'SELECT d.id, d.name, d.description, d.date_closed, d.status, d.client_id, d.doctor_id '
            'FROM diagnosis d  '
            f'{search}'
            f'{order}'
            'LIMIT :limit OFFSET :offset '
        )
        result = await session.execute(text(query), params)
        rows = result.fetchall()
        diagnosis = []

        for row in rows:
            (
                id,
                name,
                description,
                date_closed,
                status,
                client_id,
                doctor_id,
            ) = row
            diagnosis.append(
                DiagnosisData(
                    id=id,
                    name=name,
                    description=description,
                    date_closed=date_closed,
                    status=status,
                    client_id=client_id,
                    doctor_id=doctor_id,
                )
            )
        return diagnosis

    async def delete(self, id: int, session: AsyncSession) -> bool:
        query = text('DELETE FROM  diagnosis WHERE id=:id')
        await session.execute(query, {'id': id})
        await session.commit()
        return True

    async def create(
        self, data: DiagnosisCreateData, session: AsyncSession
    ) -> DiagnosisData:
        query = text(
            'INSERT INTO diagnosis(name, description, date_closed, status, client_id, doctor_id, created_at, updated_at) '
            'VALUES(:name, :description, :date_closed, :status, :client_id, :doctor_id, now(), now()) '
            'RETURNING id, name, description, date_closed, status, client_id, doctor_id '
        )
        result = await session.execute(query, dict(data))
        row = result.fetchone()
        if not row:
            raise BadRequestEx(detail='Failed to create a diagnosis')
        await session.commit()
        (
            id,
            name,
            description,
            date_closed,
            status,
            client_id,
            doctor_id,
        ) = row
        return DiagnosisData(
            id=id,
            name=name,
            description=description,
            date_closed=date_closed,
            status=status,
            client_id=client_id,
            doctor_id=doctor_id,
        )

    async def update(
        self, id: int, data: DiagnosisCreateData, session: AsyncSession
    ) -> DiagnosisData:
        query = text(
            'UPDATE diagnosis SET  updated_at=now(), name=:name, description=:description, date_closed=:date_closed, status=:status, client_id=:client_id, doctor_id=:doctor_id '
            'WHERE id=:id RETURNING name, description, date_closed, status, client_id, doctor_id '
        )
        result = await session.execute(query, {'id': id, **data})
        row = result.fetchone()
        if not row:
            raise BadRequestEx(detail='Failed to update a diagnosis')
        (name, description, date_closed, status, client_id, doctor_id) = row
        await session.commit()
        return DiagnosisData(
            id=id,
            name=name,
            description=description,
            date_closed=date_closed,
            status=status,
            client_id=client_id,
            doctor_id=doctor_id,
        )
