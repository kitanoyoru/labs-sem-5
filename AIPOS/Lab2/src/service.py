from __future__ import annotations


from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.database import Database, AdministratorFilter
from src.models.models import AdministratorModel, AdministratorOut

# from src.pagination import PaginatedResult


class Service:
    def __init__(self, database: Database):
        self._database = database

    @staticmethod
    @asynccontextmanager
    async def from_engine(engine: AsyncEngine):
        async with AsyncSession(engine) as session:
            async with session.begin():
                yield Service.from_session(session)

    @staticmethod
    def from_session(session: AsyncSession) -> Service:
        database = Database(session)
        return Service(database)

    async def get_administrator_by_criteria(
        self, filter: AdministratorFilter
    ) -> list[AdministratorOut]:
        result = await self._database.get_administrator(filter)
        return [AdministratorOut.from_model(model) for model in result]

    async def save_administrator(self, full_name: str):
        administrator = AdministratorModel(
            full_name=full_name,
        )
        return await self._database.save_administrator(administrator)

    async def delete_administrator(self, filter: AdministratorFilter):
        return await self._database.delete_administrator(filter)
