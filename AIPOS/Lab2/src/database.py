from dataclasses import dataclass
from typing import Tuple, TypeVar

from sqlalchemy import Select, func, select 
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.models import AdministratorModel
from src.pagination import PaginatedResult, PaginationOptions


@dataclass(frozen=True)
class GetAdministratorFilter:
    ID: str | None
    full_name: str | None
    pagination_options: PaginationOptions



class Database:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session


    async def save_administrator(self, administrator: AdministratorModel):
        self.session.add(administrator)
        await self.session.commit()

    async def get_administrator(self, filter: GetAdministratorFilter) -> PaginatedResult[AdministratorModel]:
        stmt = select(AdministratorModel).order_by(
            AdministratorModel.ID, AdministratorModel.full_name
        )

        if filter.ID is not None:
            stmt = stmt.where(AdministratorModel.ID.ilike(filter.ID))

        if filter.full_name is not None:
            stmt = stmt.where(AdministratorModel.full_name.ilike(filter.full_name))

        return await _paginate(self.session, stmt, filter.pagination_options)


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

