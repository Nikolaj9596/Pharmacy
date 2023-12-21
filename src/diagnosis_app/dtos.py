
from datetime import datetime
from typing import Optional, TypedDict


class CategoryDiseaseCreateData(TypedDict):
    name: str

class CategoryDiseaseData(CategoryDiseaseCreateData):
    id: int
    created_at: datetime
    updated_at: datetime

class DiseaseCreateData(TypedDict):
    name: str
    description: Optional[str]
    category_disease_id: int

class DiseaseData(DiseaseCreateData):
    id: int
    created_at: datetime
    updated_at: datetime

class DiagnosisCreateData(TypedDict):
    name: str
    description: Optional[str]
    status: str
    client_id: int
    doctor_id: int
    date_closed: Optional[datetime]

class DiagnosisData(DiagnosisCreateData):
    id: int
    created_at: datetime
    updated_at: datetime
