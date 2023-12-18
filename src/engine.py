from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from .config import settings


engine = create_async_engine(
    settings.url,
    pool_size=20,
    pool_pre_ping=True,
    pool_use_lifo=True,
    echo=settings.echo,
)

async_session_factory = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)
