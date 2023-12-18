from datetime import date

from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base


class Client(Base):
    __tablename__ = "client"

    first_name: Mapped[str] = mapped_column(String(255))
    last_name: Mapped[str] = mapped_column(String(255))
    middle_name: Mapped[str] = mapped_column(String(255))
    date_birthday: Mapped[date] = mapped_column(Date())
    address: Mapped[str] = mapped_column(String(255))
    appointments: Mapped["DoctorAppointment"] = relationship(back_populates="client")
    client_diagnosis: Mapped["ClientDiagnosis"] = relationship(back_populates="client")


class ClientDiagnosis(Base):
    __tablename__ = "client_diagnosis"

    diagnosis_id: Mapped[int] = mapped_column(
        ForeignKey("diagnosis.id", ondelete="CASCADE"), index=True
    )
    client_id: Mapped[int] = mapped_column(
        ForeignKey("client.id", ondelete="CASCADE"), index=True
    )
    doctor_id: Mapped[int] = mapped_column(
        ForeignKey("doctor.id", ondelete="CASCADE"), index=True
    )

    diagnosis: Mapped["Diagnosis"] = relationship(back_populates="client_diagnosis")
    client: Mapped["Client"] = relationship(back_populates="client_diagnosis")
    doctor: Mapped["Doctor"] = relationship(back_populates="client_diagnosis")
