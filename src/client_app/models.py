from datetime import date

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, relationship

from src.models import BaseUser, str_255


class Client(BaseUser):
    __tablename__ = 'client'

    __table_args__ = (
        UniqueConstraint(
            'first_name',
            'last_name',
            'middle_name',
            name='uq_client_full_name',
        ),
    )
    date_birthday: Mapped[date]
    address: Mapped[str_255]
    appointments: Mapped['DoctorAppointment'] = relationship(
        back_populates='client'
    )
    diagnosis: Mapped['Diagnosis'] = relationship(back_populates='client')
