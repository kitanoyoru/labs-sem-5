import logging
from typing import Any, AsyncGenerator, Callable

from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse

from src.service import Service

logger = logging.getLogger(__file__)


def create_router(
    get_service: Callable[[], AsyncGenerator[Service, Any]],
) -> APIRouter:
    router = APIRouter()

    @router.get(
        "/categories_for_current_date",
        name="Categories for current date",
        description="Get categories which change date is current date",
        response_class=ORJSONResponse,
    )
    async def get_categories_for_current_date(
        service: Service = Depends(get_service),
    ):
        return await service.get_categories_for_current_date()

    return router
