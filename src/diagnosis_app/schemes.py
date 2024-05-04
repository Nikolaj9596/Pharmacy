from datetime import datetime
from typing import Annotated, Optional

from src.models import BaseScheme

from src.types import STR_255


class CategoryDiseaseCreateScheme(BaseScheme):
    name: Annotated[str, STR_255]


class CategoryDiseaseScheme(CategoryDiseaseCreateScheme):
    id: int
    created_at: datetime
    updated_at: datetime


class DiseaseCreateScheme(BaseScheme):
    name: Annotated[str, STR_255]
    description: Optional[str]
    category_disease_id: int


class DiseaseScheme(DiseaseCreateScheme):
    id: int
    created_at: datetime
    updated_at: datetime


class DiagnosisCreateScheme(BaseScheme):
    name: Annotated[str, STR_255]
    description: Optional[str]
    status: str
    client_id: int
    doctor_id: int
    date_closed: Optional[datetime]


class DiagnosisScheme(DiagnosisCreateScheme):
    id: int
    created_at: datetime
    updated_at: datetime
