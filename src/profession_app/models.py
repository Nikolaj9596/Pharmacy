__all__ = ['Profession']
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models import Base

class ProfessionORM(Base):
    __tablename__ = 'profession'

    name: Mapped[str] = mapped_column(String(255))
    doctors: Mapped['Doctor'] = relationship(back_populates='profession')
