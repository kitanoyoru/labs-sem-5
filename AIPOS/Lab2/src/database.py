from dataclasses import dataclass
from typing import Tuple, TypeVar

import alembic.command
import sqlalchemy
from sqlalchemy import ScalarResult, Select, func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import create_alembic_config
from src.exceptions import EmployeeNotFoundException, PositionNotFoundException
from src.models.models import (
    AdministratorModel,
    CategoryModel,
    EmployeeModel,
    PaymentHistoryModel,
    PositionModel,
    SystemMetadataModel,
)
from src.pagination import PaginatedResult, PaginationOptions
from src.shared.enums import MonthEnum


@dataclass(frozen=True)
class AdministratorFilter:
    ID: int | None = None
    full_name: str | None = None


@dataclass(frozen=True)
class EmployeeFilter:
    ID: int | None = None
    full_name: str | None = None


@dataclass
class PaymentHistoryFilter:
    ID: int | None = None
    employee_id: int | None = None
    month: MonthEnum | None = None

    def __post_init__(self):
        if isinstance(self.month, str):
            self.month = MonthEnum[self.month]


class Database:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def get_administrator(
        self, filter: AdministratorFilter
    ) -> list[AdministratorModel]:
        stmt = select(AdministratorModel).order_by(
            AdministratorModel.ID, AdministratorModel.full_name
        )

        if filter.ID is not None:
            stmt = stmt.where(AdministratorModel.ID == filter.ID)

        if filter.full_name is not None:
            stmt = stmt.where(AdministratorModel.full_name.ilike(filter.full_name))

        results = await self.session.scalars(stmt)
        items = list(results.all())

        return items

    async def delete_employee(self, filter: EmployeeFilter):
        models = await self.get_employee(filter)

        for model in models:
            await self.session.delete(model)

        await self.session.commit()

    async def get_employee(self, filter: EmployeeFilter) -> list[EmployeeModel]:
        stmt = select(EmployeeModel).order_by(EmployeeModel.ID, EmployeeModel.full_name)

        if filter.ID is not None:
            stmt = stmt.where(EmployeeModel.ID == filter.ID)

        if filter.full_name is not None:
            stmt = stmt.where(EmployeeModel.full_name.ilike(filter.full_name))

        results = await self.session.scalars(stmt)
        items = list(results.all())

        return items

    async def patch_employee(self, id: int, full_name: str):
        employee = await self._get_employee_by_id(id)

        employee.full_name = full_name

        return await self.save_employee(employee)

    async def save_employee(self, employee: EmployeeModel):
        self.session.add(employee)
        await self.session.commit()

    async def assign_position_to_employee(self, employee_id: int, position_id: int):
        employee = await self.session.get(EmployeeModel, employee_id)
        if not employee:
            raise EmployeeNotFoundException(employee_id)

        position = await self.session.get(PositionModel, position_id)
        if not position:
            raise PositionNotFoundException(position_id)

        employee.positions.append(position)

        await self.session.commit()

    async def get_history(
        self, filter: PaymentHistoryFilter
    ) -> list[PaymentHistoryModel]:
        stmt = select(PaymentHistoryModel)

        if filter.ID is not None:
            stmt = stmt.where(PaymentHistoryModel.ID == filter.ID)

        if filter.employee_id is not None:
            stmt = stmt.where(PaymentHistoryModel.employee_id == filter.employee_id)

        if filter.month is not None:
            stmt = stmt.where(PaymentHistoryModel.month == filter.month.value)

        results = await self.session.scalars(stmt)
        items = list(results.all())

        return items

    async def save_history(self, history: PaymentHistoryModel):
        self.session.add(history)
        await self.session.commit()

    async def delete_history(self, filter: PaymentHistoryFilter):
        models = await self.get_history(filter)

        for model in models:
            await self.session.delete(model)

        await self.session.commit()

    async def get_system_metadata(self) -> SystemMetadataModel:
        stmt = select(SystemMetadataModel)
        return await self.session.scalar(stmt)

    async def get_categories_for_current_date(self) -> list[CategoryModel]:
        stmt = select(CategoryModel).where(
            CategoryModel.change_date == func.current_date()
        )

        results = await self.session.scalars(stmt)
        items = list(results.all())

        return items

    async def get_employees_with_min_salary_for_month(
        self, month: MonthEnum
    ) -> list[str]:
        result: ScalarResult[str] = await self.session.scalars(
            text(
            '''
            SELECT e.full_name
            FROM employee AS e
                     INNER JOIN (SELECT ph.employee_id
                                 FROM payment_history AS ph
                                 WHERE ph.month = :month
                                 GROUP BY ph.employee_id
                                 ORDER BY SUM(ph.earnings) DESC
                                 LIMIT 1) AS top_employee ON e."ID" = top_employee.employee_id;
            '''
            ),
            {"month": month.value},
        )

        return result.all()

    async def _get_employee_by_id(self, id: int) -> EmployeeModel:
        stmt = select(EmployeeModel).where(EmployeeModel.ID == id)
        return await self.session.scalar(stmt)


T = TypeVar("T")


async def _paginate(
    session: AsyncSession,
    query: Select[Tuple[T]],
    pagination_options: PaginationOptions,
) -> PaginatedResult[T]:
    if pagination_options.show_all:
        results = await session.scalars(query)
        items = list(results.all())
        total_count = len(items)
    else:
        count_query = select(func.count()).select_from(query.alias())
        total_count = await session.scalar(count_query) or 0

        query = query.offset(pagination_options.offset).limit(pagination_options.limit)
        results = await session.scalars(query)
        items = list(results.all())

    return PaginatedResult.create(
        items=items,
        offset=pagination_options.offset,
        limit=pagination_options.limit,
        total_count=total_count,
    )


def reset_database(database_url: str, data_path: str):
    engine = sqlalchemy.create_engine(database_url)

    with engine.connect() as connection:
        with connection.begin():
            connection.execute(
                text(
                    "DROP TABLE IF EXISTS administrator, employee, category, employee_position, payment_history, position, system_metadata CASCADE;"
                )
            )

    config = create_alembic_config(engine)

    alembic.command.upgrade(config, "head")
    alembic.command.revision(
        config, autogenerate=True, message="Auto-generated migration"
    )
    alembic.command.stamp(config, "base", purge=True)

    with engine.connect() as connection:
        with connection.begin():
            with open(data_path, "r") as file:
                sql_statements = file.read()
                connection.execute(text(sql_statements))
