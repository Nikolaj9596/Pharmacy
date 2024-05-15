from datetime import datetime
from typing import Optional, TypedDict


class CategoryDiseaseCreateData(TypedDict):
    name: str


class CategoryDiseaseData(CategoryDiseaseCreateData):
    id: int


class DiseaseCreateData(TypedDict):
    name: str
    description: Optional[str]
    category_disease: int


class DiseaseData(DiseaseCreateData):
    id: int
    category_disease: CategoryDiseaseData


class DiagnosisCreateData(TypedDict):
    name: str
    description: Optional[str]
    status: str
    client_id: int
    doctor_id: int
    date_closed: Optional[datetime]


class DiagnosisData(DiagnosisCreateData):
    id: int
