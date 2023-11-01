from __future__ import annotations


from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.database import Database, GetAdministratorFilter
from src.models.models import AdministratorModel


class Service:
    def __init__(self, database: Database):
        self._database = database

    @staticmethod
    @asynccontextmanager
    async def from_engine(
        engine: AsyncEngine
    ):
        async with AsyncSession(engine) as session:
            async with session.begin():
                yield Service.from_session(session)

    @staticmethod
    def from_session(
        session: AsyncSession
    ) -> Service:
        database = Database(session)
        return Service(database)

    async def get_administrator_by_criteria(self, filter: GetAdministratorFilter) -> AdministratorModel:
        return await self._database.get_administrator(filter)

    async def save_administrator(self, full_name: str):
        administrator = AdministratorModel(
            full_name=full_name,
        )
        return await self._database.save_administrator(administrator)


