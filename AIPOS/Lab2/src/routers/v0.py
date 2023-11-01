
import logging
from typing import Annotated, Any, AsyncGenerator, Callable

from fastapi import APIRouter, Depends, Form, Query
from fastapi.responses import ORJSONResponse
from src.database import GetAdministratorFilter
from src.models.models import AdministratorModel

from src.pagination import PaginatedResult, PaginationOptions, get_pagination_options
from src.service import Service


logger = logging.getLogger(__file__)


def create_router(
    get_service: Callable[[], AsyncGenerator[Service, Any]],
) -> APIRouter:
    router = APIRouter()

    @router.get(
        "/administrator",
        name="Get administrator model",
        description="Get administrator according to the specified query",
        response_class=ORJSONResponse,
    )
    async def get_administrator(
        id: str = Query(
            alias="id",
            title="Administrator ID",
            description="Filter administrator by id",
            example="12",
        ), 
        full_name: str = Query(
            alias="full_name",
            title="Administrator Fullname",
            description="Filter administrator by fullname",
            example="Ivan Prokopovich",
        ), 
        pagination_options: PaginationOptions = Depends(get_pagination_options),
        service: Service = Depends(get_service)
    ) -> PaginatedResult[AdministratorModel]:
        return await service.get_administrator_by_criteria(
            filter=GetAdministratorFilter(
                ID=id,
                full_name=full_name, 
                pagination_options=pagination_options,
            )
        )

    @router.post(
        "/administrator",
        name="Get administrator model",
        description="Get administrator according to the specified query",
        response_class=ORJSONResponse,
    )
    async def add_administrator(
        full_name: Annotated[
            str,
            Form(
                title="Administrator full name",
                example="Ivan Prokopovich",
            ),
        ],
        service: Service = Depends(get_service)
    ):
        return await service.save_administrator(
            full_name=full_name,
        )

    return router
