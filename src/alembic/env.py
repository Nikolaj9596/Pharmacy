import asyncio
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from sqlalchemy.ext.asyncio import AsyncEngine
from src.profession_app.models import *
from src.client_app.models import *
from src.diagnosis_app.models import *
from src.doctor_app.models import *

from alembic import context
from src.config import settings
from src.models import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
section = config.config_ini_section
config.set_section_option(section, 'DB_USER', settings.db_user)
config.set_section_option(section, 'DB_HOST', settings.db_host)
config.set_section_option(section, 'DB_PORT', str(settings.db_port))
config.set_section_option(section, 'DB_NAME', settings.db_name)
config.set_section_option(section, 'DB_PASS', settings.db_pass)

target_metadata = [
    Base.metadata,
]   # INFO: import form file with models


if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def run_migrations_online():
    connectable = context.config.attributes.get('connection', None)
    if connectable is None:
        connectable = AsyncEngine(
            engine_from_config(
                context.config.get_section(context.config.config_ini_section),
                prefix='sqlalchemy.',
                poolclass=pool.NullPool,
                future=True,
            )
        )

    if isinstance(connectable, AsyncEngine):
        asyncio.run(run_async_migrations(connectable))
    else:
        do_run_migrations(connectable)


async def run_async_migrations(connectable):
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


run_migrations_online()
