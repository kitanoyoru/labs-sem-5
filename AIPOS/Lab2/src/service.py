from __future__ import annotations

from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.database import AdministratorFilter, Database, EmployeeFilter
from src.exceptions import AdministratorNotAllowedException
from src.models.models import (
    AdministratorModel,
    AdministratorOut,
    EmployeeModel,
    EmployeeOut,
)


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

    async def save_employee(self, admin: AdministratorModel, full_name: str):
        employee = EmployeeModel(
            full_name=full_name,
            administrator_id=admin.ID,
        )

        return await self._database.save_employee(employee)

    async def get_employee_by_criteria(
        self, admin: AdministratorModel, filter: EmployeeFilter
    ) -> list[EmployeeOut]:
        result = await self._database.get_employee(filter)

        for employee in result:
            if employee.administrator_id != admin.ID:
                raise AdministratorNotAllowedException(employee.ID)

        return [EmployeeOut.from_model(model) for model in result]

    async def delete_employee(self, filter: EmployeeFilter):
        return await self._database.delete_employee(filter)
