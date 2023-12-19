
from datetime import datetime
from pydantic import BaseModel

from src.profession_app.routs import update


class DoctorCreateScheme(BaseModel):
    first_name: str
    last_name: str
    middle_name: str
    date_start_work: datetime
    profession: int

class DoctorScheme(DoctorCreateScheme):
    id: int
    created_at: datetime
    updated_at: datetime

class DoctorProfessionScheme(BaseModel):
    id: int
    name: str

class DoctorDetailScheme(DoctorScheme):
    profession: DoctorProfessionScheme
