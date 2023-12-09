from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models import Base


class Disease(Base):
    __tablename__ = 'disease'

    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String())
    category_disease_id: Mapped[int] = mapped_column(ForeignKey('category_disease.id'), index=True)
    category_disease: Mapped['CategoryDisease'] = relationship(back_populates='diseases')
    diagnosis: Mapped['Diagnosis'] = relationship(back_populates='diseases')
