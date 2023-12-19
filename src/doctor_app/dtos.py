from datetime import datetime
from typing import TypedDict

class DoctorDataCreate(TypedDict):
    first_name: str
    last_name: str
    middle_name: str
    date_start_work: datetime
    profession: int

class DoctorData(DoctorDataCreate):
    id: int 
    created_at: datetime
    updated_at: datetime

class DoctorProfession(TypedDict):
    id: int
    name: str

class DoctorDetailData(DoctorData):
    profession: DoctorProfession
