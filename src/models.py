from datetime import datetime
from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import MetaData

class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        default_server=text("TIMEZONE('utc', now())")
    )
    updated_at: Mapped[datetime] = mapped_column(
        default_server=text("TIMEZONE('utc', now())"),
        onupdate=datetime.utcnow,
    )
    metadata = MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    })

    def __repr__(self):
        return f"<{__class__.__name__}: {self.id}>"

    def __str__(self):
        return f"{__class__.__name__}: {self.id}"
