import asyncio
import sys
import pathlib

from logging.config import fileConfig

from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context

from app.db._models import *
from app import get_postgres_conf

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

postgres_conf = get_postgres_conf()


config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(
        url=postgres_conf.ASYNC_POSTGRES_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        dialect_opts={"paramstyle": "named"}
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Run migrations in 'online' mode.
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = create_async_engine(
        postgres_conf.ASYNC_POSTGRES_URL,
        echo=True,
        future=True
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
