from datetime import date, datetime
from typing import Annotated
from pydantic import BaseModel, validator

from src.types import POS_INT, STR_50


class UserInfo(BaseModel):
    first_name: Annotated[str, STR_50]
    last_name: Annotated[str, STR_50]
    middle_name: Annotated[str, STR_50]


class DoctorCreateScheme(UserInfo):
    date_start_work: date
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


class AppointmentCreateScheme(BaseModel):
    start_date_appointment: datetime
    end_date_appointment: datetime
    doctor_id: Annotated[int, POS_INT]
    client_id: Annotated[int, POS_INT]

    @validator('start_date_appointment')
    def validate_start_date(cls, value, values):
        if (
            'end_date_appointment' in values
            and value >= values['end_date_appointment']
        ):
            raise ValueError(
                'start_date_appointment must be less than end_date_appointment'
            )
        if value <= datetime.now():
            raise ValueError(
                'start_date_appointment must be greater than the current date'
            )
        return value

    @validator('end_date_appointment')
    def validate_end_date(cls, value, values):
        if (
            'start_date_appointment' in values
            and value <= values['start_date_appointment']
        ):
            raise ValueError(
                'end_date_appointment must be greater than start_date_appointment'
            )

        if value <= datetime.now():
            raise ValueError(
                'end_date_appointment must be greater than the current date'
            )
        return value


class AppointmentScheme(AppointmentCreateScheme):
    id: int
    created_at: datetime
    updated_at: datetime


class AppointmentDoctorInfoScheme(UserInfo):
    id: int


class AppointmentClientInfoScheme(UserInfo):
    id: int


class AppointmentDetailScheme(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    start_date_appointment: datetime
    end_date_appointment: datetime
    doctor: AppointmentDoctorInfoScheme
    client: AppointmentClientInfoScheme
