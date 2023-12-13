__all__ = ['DoctorAppointment']
from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base


class DoctorAppointment(Base):
    __tablename__ = 'make_anappointment'

    start_date_appointment: Mapped[datetime]
    end_date_appointment: Mapped[datetime]
    doctor_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('doctor.id', ondelete='SET NULl'), index=True, nullable=True
    )
    client_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('client.id', ondelete='SET NULl'), index=True, nullable=True
    )
    doctor: Mapped['Doctor'] = relationship(back_populates='appointments')
    client: Mapped['Client'] = relationship(back_populates='appointments')
