from __future__ import annotations

from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Optional

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.database import (
    AdministratorFilter,
    Database,
    EmployeeFilter,
    PaymentHistoryFilter,
    PositionFilter,
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
    PositionOut,
    SystemMetadataOut,
)
from src.shared.enums import MonthEnum


class SavePaymentHistoryDTO(BaseModel):
    month: MonthEnum


class EmployeePaymentForMonthDTO(BaseModel):
    employee: EmployeeOut
    positions: list[PositionOut]
    categories: dict[int, CategoryOut]
    payment_histories: list[PaymentHistoryOut]


class GetEmployeeDTO(BaseModel):
    employee: EmployeeOut
    positions: list[PositionOut]
    categories: dict[int, CategoryOut]


class GetPositionDTO(BaseModel):
    positions: list[PositionOut]
    categories: dict[int, CategoryOut]


class MinEmployeeSalaryDTO(BaseModel):
    employee: EmployeeOut
    positions: list[PositionOut]
    payment_histories: list[PaymentHistoryOut]
    categories: dict[int, CategoryOut]


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

    async def save_employee(
        self, admin: AdministratorModel, full_name: str, position: str
    ):
        employee = EmployeeModel(
            full_name=full_name,
            administrator_id=admin.ID,
        )

        position = await self._database.get_position_by_name(position)

        return await self._database.save_employee(employee, position)

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
    ) -> list[GetEmployeeDTO]:
        employees = await self._database.get_employee(filter)

        for employee in employees:
            if employee.administrator_id != admin.ID:
                raise AdministratorNotAllowedException(employee.ID)

        result: list[GetEmployeeDTO] = []
        for employee in employees:
            positions = [
                PositionOut.from_model(model)
                for model in await self._database.get_employee_positions(
                    employee.ID, filter
                )
            ]
            if len(positions) == 0:
                continue

            categories: dict[int, CategoryOut] = {}
            for position in positions:
                category = await self._database.get_position_category(position.ID)
                categories[position.ID] = CategoryOut.from_model(category)

            result.append(
                GetEmployeeDTO(
                    employee=EmployeeOut.from_model(employee),
                    positions=positions,
                    categories=categories,
                )
            )

        return result

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

        system_metadata = await self._database.get_system_metadata()
        positions = await self._database.get_employee_positions(employee_id)

        payments = 0
        for position in positions:
            category = await self._database.get_position_category(position.ID)
            payments += system_metadata.minimum_salary * category.coefficient

        payments *= 1.15

        deductions = 0.87 * payments + 0.01 * system_metadata.pension_contribution
        if employee.is_trade_union_member:
            deductions += 0.01 * system_metadata.trade_union_contribution

        earnings = payments - deductions

        history = PaymentHistoryModel(
            employee_id=employee_id,
            month=dto.month.value,
            earnings=earnings,
            payments=payments,
            deductions=deductions,
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

    async def get_employees_with_min_salary_for_month(
        self, admin: AdministratorModel, month: MonthEnum
    ) -> list[MinEmployeeSalaryDTO]:
        employees = await self._database.get_employees_with_min_salary_for_month(month)

        result: list[MinEmployeeSalaryDTO] = []
        for employee in employees:
            empl_out = EmployeeOut.from_model(employee)

            positions = [
                PositionOut.from_model(model)
                for model in await self._database.get_employee_positions(employee.ID)
            ]

            categories: dict[int, CategoryOut] = {}
            for position in positions:
                category = await self._database.get_position_category(position.ID)
                categories[position.ID] = CategoryOut.from_model(category)

            histories = [
                PaymentHistoryOut.from_model(model)
                for model in await self._database.get_history(
                    filter=PaymentHistoryFilter(employee_id=employee.ID)
                )
            ]

            result.append(
                MinEmployeeSalaryDTO(
                    employee=empl_out,
                    positions=positions,
                    categories=categories,
                    payment_histories=histories,
                )
            )

        return result

    async def get_employee_payment_for_month(
        self, admin: AdministratorModel, employee_id, month: MonthEnum
    ) -> EmployeePaymentForMonthDTO:
        employee = await self._database._get_employee_by_id(employee_id)
        if employee.administrator_id != admin.ID:
            raise AdministratorNotAllowedException(employee_id)

        empl_out = EmployeeOut.from_model(employee)

        positions = [
            PositionOut.from_model(model)
            for model in await self._database.get_employee_positions(employee.ID)
        ]

        categories: dict[int, CategoryOut] = {}
        for position in positions:
            category = await self._database.get_position_category(position.ID)
            categories[position.ID] = CategoryOut.from_model(category)

        histories = [
            PaymentHistoryOut.from_model(model)
            for model in await self._database.get_history(
                filter=PaymentHistoryFilter(employee_id=employee.ID)
            )
        ]

        return EmployeePaymentForMonthDTO(
            employee=empl_out,
            positions=positions,
            categories=categories,
            payment_histories=histories,
        )

    async def get_position_by_criteria(
        self,
        admin: AdministratorModel,
        filter: PositionFilter,
    ) -> GetPositionDTO:
        positions = await self._database.get_position(filter)

        categories: dict[int, CategoryOut] = {}
        for position in positions:
            category = await self._database.get_position_category(position.ID)
            categories[position.ID] = CategoryOut.from_model(category)

        return GetPositionDTO(
            positions=positions,
            categories=categories,
        )

    async def patch_position(
        self,
        admin: AdministratorModel,
        id: int,
        name: Optional[str] = None,
        category_id: Optional[int] = None,
    ):
        result = await self._database.get_position(filter=PositionFilter(ID=id))

        """
        for position in result:
            if position.employees.any(EmployeeModel.administrator_id != admin.ID):
                raise AdministratorNotAllowedException()
        """

        return await self._database.patch_position(id, name, category_id)
