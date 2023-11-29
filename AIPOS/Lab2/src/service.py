from __future__ import annotations

from contextlib import asynccontextmanager
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.database import (
    AdministratorFilter,
    Database,
    EmployeeFilter,
    PaymentHistoryFilter,
)
from src.exceptions import AdministratorNotAllowedException
from src.models.models import (
    AdministratorModel,
    AdministratorOut,
    CategoryOut,
    EmployeeModel,
    EmployeeOut,
    PaymentHistoryModel,
    PaymentHistoryOut,
    PositionModel,
    SystemMetadataOut,
)
from src.shared.enums import MonthEnum


@dataclass(frozen=True)
class SavePaymentHistoryDTO:
    month: str
    earnings: int
    payments: int
    deductions: int


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

    async def assign_position_to_employee(
        self,
        admin: AdministratorModel,
        employee_id: int,
        position_id: int,
    ):
        employee = await self._database._get_employee_by_id(employee_id)
        if employee.administrator_id != admin.ID:
            raise AdministratorNotAllowedException(employee_id)

        return await self._database.assign_position_to_employee(
            employee_id, position_id
        )

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

    async def patch_employee(self, admin: AdministratorModel, id: int, full_name: str):
        result = await self._database.get_employee(filter=EmployeeFilter(ID=id))

        for employee in result:
            if employee.administrator_id != admin.ID:
                raise AdministratorNotAllowedException(employee.ID)

        return await self._database.patch_employee(id, full_name)

    async def get_employee_payment_history_by_criteria(
        self, admin: AdministratorModel, filter: PaymentHistoryFilter
    ) -> list[PaymentHistoryOut]:
        histories = await self._database.get_history(filter)

        for history in histories:
            employee = await self._database._get_employee_by_id(
                history.employee_id,
            )
            if employee.administrator_id != admin.ID:
                raise AdministratorNotAllowedException(employee.ID)

        return [PaymentHistoryOut.from_model(model) for model in histories]

    async def save_payment_history(
        self, admin: AdministratorModel, employee_id: int, dto: SavePaymentHistoryDTO
    ):
        employee = await self._database._get_employee_by_id(employee_id)

        if employee.administrator_id != admin.ID:
            raise AdministratorNotAllowedException(employee.ID)

        history = PaymentHistoryModel(
            employee_id=employee_id,
            month=dto.month,
            earnings=dto.earnings,
            payments=dto.payments,
            deductions=dto.deductions,
        )

        return await self._database.save_history(history)

    async def delete_payment_history(self, filter: PaymentHistoryFilter):
        return await self._database.delete_history(filter)

    async def get_system_metadata(self, admin: AdministratorModel) -> SystemMetadataOut:
        system_metadata = await self._database.get_system_metadata()

        if system_metadata.administrator_id != admin.ID:
            raise AdministratorNotAllowedException(system_metadata.ID)

        return SystemMetadataOut.from_model(system_metadata)

    async def get_categories_for_current_date(self) -> list[CategoryOut]:
        categories = await self._database.get_categories_for_current_date()
        return [CategoryOut.from_model(category) for category in categories]
