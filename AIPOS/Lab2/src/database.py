from dataclasses import dataclass
from typing import Tuple, TypeVar
import alembic.command

from sqlalchemy import Select, func, select, text
import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import create_alembic_config

from src.models.models import AdministratorModel
from src.pagination import PaginatedResult, PaginationOptions


@dataclass(frozen=True)
class AdministratorFilter:
    ID: int | None
    full_name: str | None
    # pagination_options: PaginationOptions


class Database:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def save_administrator(self, administrator: AdministratorModel):
        self.session.add(administrator)
        await self.session.commit()

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

    async def delete_administrator(self, filter: AdministratorFilter):
        models = await self.get_administrator(filter)

        for model in models:
            await self.session.delete(model)

        await self.session.commit()


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


def reset_database(database_url: str):
    engine = sqlalchemy.create_engine(database_url)

    with engine.connect() as connection:
        with connection.begin():
            connection.execute(
                text(
                    "DROP TABLE IF EXISTS administrator, employee, category, employee_position, payment_history, position, system_metadata CASCADE;"
                )
            )

    config = create_alembic_config(engine)

    alembic.command.stamp(config, "base", purge=True)
    alembic.command.upgrade(config, "head")

