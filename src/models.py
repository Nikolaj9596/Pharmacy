from datetime import datetime
from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        default_server=text("TIMEZONE('utc', now())")
    )
    updated_at: Mapped[datetime] = mapped_column(
        default_server=text("TIMEZONE('utc', now())"),
        onupdate=datetime.utcnow,
    )

    def __repr__(self):
        return f"<{__class__.__name__}: {self.id}>"

    def __str__(self):
        return f"{__class__.__name__}: {self.id}"
