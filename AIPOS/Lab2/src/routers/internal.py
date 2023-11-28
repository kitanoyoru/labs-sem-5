import logging
import os
from typing import Annotated, Any, AsyncGenerator, Callable

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.responses import ORJSONResponse
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel

from src.database import AdministratorFilter, EmployeeFilter, PaymentHistoryFilter
from src.models.models import (
    AdministratorModel,
    CategoryOut,
    EmployeeOut,
    PaymentHistoryOut,
)
from src.service import Service
from src.shared.enums import MonthEnum

logger = logging.getLogger(__file__)

SECRET_KEY = os.environ["AUTH_SECRET_KEY"]
ALGORITHM = os.environ["AUTH_ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ["AUTH_ACCESS_TOKEN_EXPIRE_MINUTES"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class TokenData(BaseModel):
    username: str | None = None


def create_router(
    get_service: Callable[[], AsyncGenerator[Service, Any]],
) -> APIRouter:
    router = APIRouter()

    async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        service: Service = Depends(get_service),
    ):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception
        result = await service.get_administrator_by_criteria(
            filter=AdministratorFilter(full_name=token_data.username)
        )
        assert len(result) == 1
        user = result[0]

        if user is None:
            raise credentials_exception

        return user

    @router.get(
        "/categories_for_current_date",
        name="Categories for current date",
        description="Get categories which change date is current date",
        response_class=ORJSONResponse,
    )
    async def get_categories_for_current_date(
        service: Service = Depends(get_service),
    ) -> list[CategoryOut]:
        return await service.get_categories_for_current_date()

    @router.get(
        "/employee_payments_for_month",
        name="Employee payments for month",
        description="Get employee's payments for specific month",
        response_class=ORJSONResponse,
    )
    async def get_employee_payment_for_month(
        id: str = Query(
            ...,
            alias="employee_id",
            title="Requested employee",
            example="123",
        ),
        month: MonthEnum = Query(
            ...,
            alias="month",
            title="Requested month",
            example="January",
        ),
        service: Service = Depends(get_service),
        administrator: AdministratorModel = Depends(get_current_user),
    ) -> list[PaymentHistoryOut]:
        return await service.get_employee_payment_history_by_criteria(
            administrator,
            filter=PaymentHistoryFilter(
                ID=id,
                month=month,
            ),
        )

    return router
