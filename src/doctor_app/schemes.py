from datetime import date, datetime
from typing import Annotated
from pydantic import validator
from src.models import BaseScheme
import pydantic

from src.types import POS_INT, STR_50


class UserInfo(BaseScheme):
    first_name: Annotated[str, STR_50]
    last_name: Annotated[str, STR_50]
    middle_name: Annotated[str, STR_50]
    avatar: pydantic.HttpUrl
    date_birthday: date


class DoctorProfessionScheme(BaseScheme):
    id: int
    name: str


class DoctorCreateScheme(UserInfo):
    date_start_work: date
    profession: int


class DoctorScheme(DoctorCreateScheme):
    id: int


class DoctorDetailScheme(DoctorScheme):
    profession: DoctorProfessionScheme


class AppointmentCreateScheme(BaseScheme):
    start_date_appointment: datetime
    end_date_appointment: datetime
    doctor: Annotated[int, POS_INT]
    client: Annotated[int, POS_INT]

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


class AppointmentDoctorInfoScheme(UserInfo):
    id: int
    first_name: str
    last_name: str
    middle_name: str
    avatar: str


class AppointmentClientInfoScheme(UserInfo):
    id: int
    first_name: str
    last_name: str
    middle_name: str
    avatar: str


class AppointmentScheme(AppointmentCreateScheme):
    id: int
    created_at: datetime
    updated_at: datetime
    doctor: AppointmentDoctorInfoScheme
    client: AppointmentClientInfoScheme
