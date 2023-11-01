from __future__ import annotations
from typing import TypeVar, Generic, Callable, Annotated

from fastapi import Query
from pydantic import BaseModel
from pydantic.generics import GenericModel


class PaginationOptions(BaseModel):
    show_all: bool
    offset: int
    limit: int


T = TypeVar("T")
S = TypeVar("S")


class PaginatedResult(GenericModel, Generic[T]):
    items: list[T]
    offset: int
    limit: int
    count: int
    total_count: int

    @classmethod
    def create(
        cls,
        items: list[T],
        offset: int,
        limit: int,
        total_count: int,
    ) -> PaginatedResult[T]:
        return PaginatedResult(
            items=items,
            offset=offset,
            limit=limit,
            count=len(items),
            total_count=total_count,
        )

    def map(self, map_item: Callable[[T], S]) -> PaginatedResult[S]:
        return PaginatedResult(
            items=[map_item(item) for item in self.items],
            offset=self.offset,
            limit=self.limit,
            count=self.count,
            total_count=self.total_count,
        )


def get_pagination_options(
    offset: Annotated[
        int,
        Query(
            ge=0,
            description="Offset within the total dataset.",
            example=0,
        ),
    ] = 0,
    limit: Annotated[
        int,
        Query(
            ge=1,
            le=100,
            description="Count of returned results.",
            example=10,
        ),
    ] = 10,
    show_all: Annotated[
        bool,
        Query(
            description="If true, ignore `offset` and `limit` and return the complete dataset.",
            example=False,
        ),
    ] = False,
) -> PaginationOptions:
    return PaginationOptions(
        offset=offset,
        limit=limit,
        show_all=show_all,
    )

