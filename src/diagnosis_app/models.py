__all__ = ["Diagnosis", "DiseaseDiagnosis"]
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base


class Diagnosis(Base):
    __tablename__ = "diagnosis"

    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(1000))
    diseases: Mapped["DiseaseDiagnosis"] = relationship(
        back_populates="diagnosis", secondary="disease_diagnosis"
    )


class DiseaseDiagnosis(Base):
    __tablename__ = "disease_diagnosis"

    disease_id: Mapped[int] = mapped_column(
        ForeignKey("disease.id", ondelete="CASCADE"), primary_key=True
    )
    diagnosis_id: Mapped[int] = mapped_column(
        ForeignKey("diagnosis.id", ondelete="CASCADE"), primary_key=True
    )


class CategoryDisease(Base):
    __tablename__ = "category_disease"

    name: Mapped[str] = mapped_column(String(255))
    diseases: Mapped[list["Disease"]] = relationship(back_populates="category_disease")


class Disease(Base):
    __tablename__ = "disease"

    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String())
    category_disease_id: Mapped[int] = mapped_column(
        ForeignKey("category_disease.id"), index=True
    )
    category_disease: Mapped["CategoryDisease"] = relationship(
        back_populates="diseases"
    )
    diagnosis: Mapped["DiseaseDiagnosis"] = relationship(
        back_populates="diseases", secondary="disease_diagnosis"
    )
