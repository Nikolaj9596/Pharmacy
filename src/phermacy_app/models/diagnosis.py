from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models import Base


class Diagnosis(Base):
    __tablename__ = 'diagnosis'

    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(1000))
    disease_id: Mapped[int] = mapped_column(ForeignKey('disease.id'), index=True)
    disease: Mapped['Disease'] = relationship(back_populates='diagnosis') 
