import logging
import os
from typing import Annotated, Any, AsyncGenerator, Callable, Optional

from fastapi import APIRouter, Depends, Form, HTTPException, Query, status
from fastapi.responses import ORJSONResponse
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel

from src.database import AdministratorFilter, EmployeeFilter, PaymentHistoryFilter
from src.exceptions import AdministratorNotAllowedException
from src.models.models import AdministratorModel, EmployeeOut, PaymentHistoryOut
from src.service import Service, SavePaymentHistoryDTO

logger = logging.getLogger(__file__)

SECRET_KEY = os.environ["AUTH_SECRET_KEY"]
ALGORITHM = os.environ["AUTH_ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.environ["AUTH_ACCESS_TOKEN_EXPIRE_MINUTES"])

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
        "/employee",
        name="Get employee model",
        description="Get employee according to the specified query",
        response_class=ORJSONResponse,
    )
    async def get_employee(
        id: Optional[int] = Query(
            None,
            alias="id",
            title="Administrator ID",
            description="Filter administrator by id",
            example="12",
        ),
        full_name: Optional[str] = Query(
            None,
            alias="full_name",
            title="Administrator Fullname",
            description="Filter administrator by fullname",
            example="Ivan Prokopovich",
        ),
        service: Service = Depends(get_service),
        administrator: AdministratorModel = Depends(get_current_user),
    ) -> list[EmployeeOut]:
        try:
            return await service.get_employee_by_criteria(
                administrator,
                filter=EmployeeFilter(
                    ID=id,
                    full_name=full_name,
                ),
            )
        except AdministratorNotAllowedException as exc:
            return HTTPException(status_code=405, detail=str(exc))

    @router.post(
        "/employee",
        name="Add employee model",
        response_class=ORJSONResponse,
    )
    async def add_employee(
        full_name: Annotated[
            str,
            Form(
                title="Employee full name",
                example="Ivan Prokopovich",
            ),
        ],
        service: Service = Depends(get_service),
        administrator: AdministratorModel = Depends(get_current_user),
    ):
        return await service.save_employee(
            administrator,
            full_name=full_name,
        )

    @router.delete(
        "/employee",
        name="Delete employee model",
        response_class=ORJSONResponse,
    )
    async def delete_employee(
        id: Optional[int] = Query(
            None,
            alias="id",
            title="Employee ID",
            description="Filter employee by id",
            example="12",
        ),
        full_name: Optional[str] = Query(
            None,
            alias="full_name",
            title="Employee Fullname",
            description="Filter employee by fullname",
            example="Ivan Prokopovich",
        ),
        service: Service = Depends(get_service),
        current_user: AdministratorModel = Depends(get_current_user),
    ):
        return await service.delete_employee(
            EmployeeFilter(
                ID=id,
                full_name=full_name,
            )
        )

    @router.get(
        "/payment_history",
        name="Get employee payment history",
        description="Get employee according to the specified query",
        response_class=ORJSONResponse,
    )
    async def get_employee_payment_history(
        id: Optional[int] = Query(
            None,
            alias="id",
            title="Employee ID",
            description="Filter administrator by id",
            example="12",
        ),
        full_name: Optional[str] = Query(
            None,
            alias="full_name",
            title="Employee Fullname",
            description="Filter administrator by fullname",
            example="Ivan Prokopovich",
        ),
        service: Service = Depends(get_service),
        administrator: AdministratorModel = Depends(get_current_user),
    ) -> list[PaymentHistoryOut]:
        try:
            return await service.get_employee_payment_history_by_criteria(
                administrator,
                filter=PaymentHistoryFilter(
                    ID=id,
                ),
            )
        except AdministratorNotAllowedException as exc:
            return HTTPException(status_code=405, detail=str(exc))

    @router.post(
        "/payment_history",
        name="Add paymeny history model",
        response_class=ORJSONResponse,
    )
    async def add_payment_historyck(
        employee_id: Annotated[
            int,
            Form(
                title="Employee d",
            ),
        ],
        month: Annotated[
            str,
            Form(
                title="Month",
                example="January",
            ),
        ],
        earnings: Annotated[
            int,
            Form(
                title="Employee d",
            ),
        ],
        payments: Annotated[
            int,
            Form(
                title="Payments",
            ),
        ],
        deductions: Annotated[
            int,
            Form(
                title="Deductions",
            ),
        ],
        service: Service = Depends(get_service),
        administrator: AdministratorModel = Depends(get_current_user),
    ):
        return await service.save_payment_history(administrator, employee_id, dto=SavePaymentHistoryDTO(
            month=month,
            earnings=earnings,
            payments=payments,
            deductions=deductions,
        ))

    @router.delete(
        "/payment_history",
        name="Delete payment history model",
        response_class=ORJSONResponse,
    )
    async def delete_payment_history(
        id: Optional[int] = Query(
            None,
            alias="id",
            title="Employee ID",
            description="Filter employee by id",
            example="12",
        ),
        service: Service = Depends(get_service),
        current_user: AdministratorModel = Depends(get_current_user),
    ):
        return await service.delete_payment_history(
            PaymentHistoryFilter(
                ID=id,
            )
        )

    return router
