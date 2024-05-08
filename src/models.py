from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import MetaData
from sqlalchemy.sql.functions import now
import pydantic


str_50 = Annotated[str, 50]
str_255 = Annotated[str, 50]


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=now())
    updated_at: Mapped[datetime] = mapped_column(
        default=now(),
        onupdate=datetime.utcnow,
    )
    metadata = MetaData(
        naming_convention={
            'ix': 'ix_%(column_0_label)s',
            'uq': 'uq_%(table_name)s_%(column_0_name)s',
            'ck': 'ck_%(table_name)s_%(constraint_name)s',
            'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
            'pk': 'pk_%(table_name)s',
        }
    )
    type_annotation_map = {str_50: String(50), str_255: String(255)}

    def __repr__(self):
        return f'<{__class__.__name__}: {self.id}>'

    def __str__(self):
        return f'{__class__.__name__}: {self.id}'


class BaseUser(Base):
    __abstract__ = True

    first_name: Mapped[str_50]
    last_name: Mapped[str_50]
    middle_name: Mapped[str_50]
    avatar: Mapped[str_255]

class BaseScheme(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
