from datetime import datetime
from typing import Annotated, Optional

from src.doctor_app.schemes import UserInfo
from src.models import BaseScheme

from src.types import STR_255


class CategoryDiseaseCreateScheme(BaseScheme):
    name: Annotated[str, STR_255]


class CategoryDiseaseScheme(CategoryDiseaseCreateScheme):
    id: int


class DiseaseCreateScheme(BaseScheme):
    name: Annotated[str, STR_255]
    description: Optional[str]
    category_disease: int


class DiseaseResponseScheme(DiseaseCreateScheme):
    id: int

class DiseaseScheme(DiseaseCreateScheme):
    id: int
    category_disease: CategoryDiseaseScheme

class DiseaseShortScheme(BaseScheme):
    id: int
    name: str

class DiagnosisCreateScheme(BaseScheme):
    name: Annotated[str, STR_255]
    description: Optional[str]
    status: str
    client: int
    doctor: int
    disease: list[int] 

class DiagnosisScheme(DiagnosisCreateScheme):
    id: int
    client: UserInfo
    doctor: UserInfo
    disease: list[DiseaseShortScheme]
