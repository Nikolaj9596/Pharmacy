from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models import Base

class Profession(Base):
    __tablename__ = 'professions'

    name: Mapped[str] = mapped_column(String(255))
    doctors: Mapped['Doctor'] = relationship(back_populates='profession')
