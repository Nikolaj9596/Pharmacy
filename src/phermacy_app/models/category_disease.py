from sqlalchemy import String
from src.models import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class CategoryDisease(Base):
    __tablename__ = 'category_disease'

    name: Mapped[str] = mapped_column(String(255))
    diseases: Mapped[list['Disease']] = relationship(back_populates='category_disease')
