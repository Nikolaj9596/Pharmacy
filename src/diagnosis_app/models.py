__all__ = ['Diagnosis', 'DiseaseDiagnosis']

from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum

from src.models import Base, str_255


class Diagnosis(Base):
    __tablename__ = 'diagnosis'

    class StatusChoices(Enum):
        ACTIVE = 'active'
        CLOSED = 'closed'

    name: Mapped[str_255]
    description: Mapped[str] = mapped_column(String(1000))
    date_closed: Mapped[datetime] = mapped_column(DateTime(), nullable=True)
    status: Mapped[StatusChoices] = mapped_column(default=StatusChoices.ACTIVE)
    client_id: Mapped[int] = mapped_column(
        ForeignKey('clients.id', ondelete='CASCADE'), index=True
    )
    doctor_id: Mapped[int] = mapped_column(
        ForeignKey('doctors.id', ondelete='CASCADE'), index=True
    )
    diseases: Mapped['DiseaseDiagnosis'] = relationship(
        back_populates='diagnosis', secondary='disease_diagnosis'
    )
    client: Mapped['Client'] = relationship(back_populates='diagnosis')
    doctor: Mapped['Doctor'] = relationship(back_populates='diagnosis')


class DiseaseDiagnosis(Base):
    __tablename__ = 'disease_diagnosis'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    disease_id: Mapped[int] = mapped_column(
        ForeignKey('diseases.id', ondelete='CASCADE'), primary_key=True
    )
    diagnosis_id: Mapped[int] = mapped_column(
        ForeignKey('diagnosis.id', ondelete='CASCADE'), primary_key=True
    )


class CategoryDisease(Base):
    __tablename__ = 'categories_disease'

    name: Mapped[str] = mapped_column(String(255), unique=True)
    diseases: Mapped[list['Disease']] = relationship(
        back_populates='category_disease'
    )


class Disease(Base):
    __tablename__ = 'diseases'

    name: Mapped[str] = mapped_column(String(255), unique=True)
    description: Mapped[str] = mapped_column(String(10000))
    category_disease_id: Mapped[int] = mapped_column(
        ForeignKey('categories_disease.id'), index=True
    )
    category_disease: Mapped['CategoryDisease'] = relationship(
        back_populates='diseases'
    )
    diagnosis: Mapped['DiseaseDiagnosis'] = relationship(
        back_populates='diseases', secondary='disease_diagnosis'
    )
