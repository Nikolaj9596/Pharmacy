from datetime import datetime
from typing import Optional, TypedDict


class UserData(TypedDict):
    first_name: str
    last_name: str
    middle_name: str
    avatar: str


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
    client: int
    doctor: int
    date_closed: Optional[datetime]
    disease: list[int]


class ShortDiseaseData(TypedDict):
    id: int
    name: str


class DiagnosisResponseData(DiagnosisCreateData):
    id: int

class DiagnosisData(DiagnosisCreateData):
    id: int
    disease: list[ShortDiseaseData]
    client: UserData
    doctor: UserData
