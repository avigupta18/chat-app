from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from sqlalchemy.engine import url as sa_url
from alembic import context
from realtime.models import Base  # :white_check_mark: Import your metadata here
# Alembic Config object, provides access to alembic.ini values
config = context.config
# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)
# Target metadata (your models’ metadata)
target_metadata = Base.metadata
def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    # Convert async URL to sync
    sync_url = sa_url.make_url(url).set(drivername="postgresql+psycopg2")
    context.configure(
        url=str(sync_url),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()
def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    configuration = config.get_section(config.config_ini_section)
    async_url = configuration["sqlalchemy.url"]
    # Convert async URL → sync URL for Alembic
    sync_url = sa_url.make_url(async_url).set(drivername="postgresql+psycopg2")
    connectable = engine_from_config(
        {**configuration, "sqlalchemy.url": str(sync_url)},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()