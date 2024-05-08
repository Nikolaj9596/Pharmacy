from datetime import date, datetime
from typing import TypedDict

class DoctorDataCreate(TypedDict):
    first_name: str
    last_name: str
    middle_name: str
    date_start_work: date
    profession: int
    date_birthday: date
    avatar: str


class DoctorProfession(TypedDict):
    id: int
    name: str

class DoctorData(DoctorDataCreate):
    id: int 
    profession: int

class DoctorDetailData(DoctorData):
    profession: DoctorProfession

class AppointmentDataCreate(TypedDict):
    start_date_appointment: datetime
    end_date_appointment: datetime
    doctor_id: int
    client_id: int

class AppointmentData(AppointmentDataCreate):
    id: int 
    created_at: datetime
    updated_at: datetime
    
class DoctorAppointmentInfo(TypedDict):
    id: int
    first_name: str
    last_name: str
    middle_name: str

class ClientAppointmentInfo(TypedDict):
    id: int
    first_name: str
    last_name: str
    middle_name: str

class AppointmentDetailData(TypedDict):
    id: int 
    created_at: datetime
    updated_at: datetime
    start_date_appointment: datetime
    end_date_appointment: datetime
    doctor: DoctorAppointmentInfo
    client: ClientAppointmentInfo

    
