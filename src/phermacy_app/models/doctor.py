from datetime import date
from sqlalchemy import ForeignKey, String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models import Base

class Doctor(Base):
    __tablename__ = 'doctor'

    profession_id: Mapped[int] = mapped_column(ForeignKey('profession.id'), index=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    middle_name: Mapped[str] = mapped_column(String(50))
    appointments: Mapped['DoctorAppointment'] = relationship(back_populate='doctor')
    profession: Mapped['Profession'] = relationship(back_populate='doctors')
    date_start_work: Mapped[date] = mapped_column(Date)

