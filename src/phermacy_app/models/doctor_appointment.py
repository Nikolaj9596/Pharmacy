from datetime import datetime
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models import Base


class DoctorAppointment(Base):
    __tablename__ = 'make_anappointment'

    doctor_id: Mapped[int] = mapped_column(ForeignKey('doctor.id'), index=True)
    doctor: Mapped['Doctor'] = relationship(back_populate='appointments')
    client_id: Mapped[int] = mapped_column(ForeignKey('client.id'), index=True)
    client: Mapped['Client'] = relationship(back_populate='appointments')
    start_date_appointment: Mapped[datetime] = mapped_column(DateTime)
    end_date_appointment: Mapped[datetime] = mapped_column(DateTime)
