__all__ = ['Diagnosis', 'DiseaseDiagnosis']
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base


class Diagnosis(Base):
    __tablename__ = 'diagnosis'

    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(1000))
    diseases: Mapped['DiseaseDiagnosis'] = relationship(
        back_populates='diagnosis', secondary='disease_diagnosis'
    )


class DiseaseDiagnosis(Base):
    __tablename__ = 'disease_diagnosis'

    disease_id: Mapped[int] = mapped_column(
        ForeignKey('disease.id', ondelete='CASCADE'), primary_key=True
    )
    diagnosis_id: Mapped[int] = mapped_column(
        ForeignKey('diagnosis.id', ondelete='CASCADE'), primary_key=True
    )
