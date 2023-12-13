__all__ = ['Client',]
from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from src.models import Base


class Client(Base):
    __tablename__ = 'client'

    first_name: Mapped[str] = mapped_column(String(255))
    last_name: Mapped[str] = mapped_column(String(255))
    middle_name: Mapped[str] = mapped_column(String(255))
    date_birthday: Mapped[date] = mapped_column(Date())
    address: Mapped[str] = mapped_column(String(255))
    appointments: Mapped['DoctorAppointment'] = relationship(back_populates='client')
    client_diagnosis: Mapped['ClientDiagnosis'] = relationship(back_populates='client')
