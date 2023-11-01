import os
import pathlib
from dataclasses import dataclass

import alembic.config
import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine


@dataclass
class Directories:
    static: str
    templates: str
    test_data: str


def get_directories() -> Directories:
    root_dir = pathlib.Path(__file__).parent

    return Directories(
        static=str(root_dir / "static"),
        templates=str(root_dir / "templates"),
        test_data=str(root_dir / "test_data"),
    )

def get_database_url() -> str:
    return f"postgresql+psycopg://{os.environ['DATABASE_URL']}"


def create_engine_from_env() -> AsyncEngine:
    SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg://{os.environ['DATABASE_URL']}"

    return create_async_engine(SQLALCHEMY_DATABASE_URL)


def create_alembic_config(this_engine: sqlalchemy.Engine) -> alembic.config.Config:
    config = alembic.config.Config()

    config.set_main_option("script_location", "sammelrepository:migrations")

    config.attributes["engine"] = this_engine

    return config

