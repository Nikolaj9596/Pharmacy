__all__ = ["Doctor", "DoctorAppointment"]
from datetime import date, datetime
from typing import Optional

from sqlalchemy import Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base, BaseUser


class Doctor(BaseUser):
    __tablename__ = "doctors"

    __table_args__ = (
        UniqueConstraint(
            "first_name", "last_name", "middle_name", name="uq_doctor_names"
        ),
    )

    date_start_work: Mapped[date] = mapped_column(Date)
    date_birthday: Mapped[date] = mapped_column(Date)
    profession_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("professions.id", ondelete="SET NULL"),
        index=True,
        nullable=True,
    )
    appointments: Mapped["DoctorAppointment"] = relationship(back_populates="doctor")
    diagnosis: Mapped["Diagnosis"] = relationship(back_populates="doctor")
    profession: Mapped["Profession"] = relationship(back_populates="doctors")


class DoctorAppointment(Base):
    __tablename__ = "appointments"

    start_date_appointment: Mapped[datetime]
    end_date_appointment: Mapped[datetime]
    doctor_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("doctors.id", ondelete="SET NULl"), index=True, nullable=True
    )
    client_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("clients.id", ondelete="SET NULl"), index=True, nullable=True
    )
    doctor: Mapped["Doctor"] = relationship(back_populates="appointments")
    client: Mapped["Client"] = relationship(back_populates="appointments")
