import logging
import os
from typing import Annotated, Any, AsyncGenerator, Callable, Optional

from fastapi import APIRouter, Depends, Form, HTTPException, Query, Request, status
from fastapi.responses import ORJSONResponse
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel

from src.database import AdministratorFilter, EmployeeFilter, PaymentHistoryFilter
from src.exceptions import AdministratorNotAllowedException
from src.models.models import AdministratorModel, EmployeeOut, PaymentHistoryOut
from src.service import SavePaymentHistoryDTO, Service

logger = logging.getLogger(__file__)

SECRET_KEY = os.environ["AUTH_SECRET_KEY"]
ALGORITHM = os.environ["AUTH_ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ["AUTH_ACCESS_TOKEN_EXPIRE_MINUTES"])


class TokenData(BaseModel):
    username: str | None = None


def create_router(
    get_service: Callable[[], AsyncGenerator[Service, Any]],
) -> APIRouter:
    router = APIRouter()

    async def get_current_user(
        request: Request,
        service: Service = Depends(get_service),
    ):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        token = request.cookies.get("access_token")
        if not token:
            raise credentials_exception

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

    @router.post(
        "/get_employee",
        name="Get employee model",
        description="Get employee according to the specified query",
        response_class=ORJSONResponse,
    )
    async def get_employee(
        request: Request,
        id: Annotated[
            Optional[int],
            Form(
                title="Employee id",
                example="12",
            ),
        ] = None,
        full_name: Annotated[
            Optional[str],
            Form(
                title="Employee full name",
                example="Ivan Prokopovich",
            ),
        ] = None,
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
        request: Request,
        full_name: Annotated[
            str,
            Form(
                title="Employee full name",
                example="Ivan Prokopovich",
            ),
        ],
        position: Annotated[
            str,
            Form(
                title="Employee position",
                example="Developer",
            ),
        ],
        service: Service = Depends(get_service),
        administrator: AdministratorModel = Depends(get_current_user),
    ):
        return await service.save_employee(
            administrator,
            full_name=full_name,
            position=position,
        )

    @router.post(
        "/patch_employee",
        name="Patch employee model",
        response_class=ORJSONResponse,
    )
    async def patch_employee(
        request: Request,
        id: Annotated[
            int,
            Form(
                title="Employee id",
                example="12",
            ),
        ],
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
        try:
            return await service.patch_employee(
                administrator, id=id, full_name=full_name
            )
        except AdministratorNotAllowedException as exc:
            return HTTPException(status_code=405, detail=str(exc))

    @router.post(
        "/employee/position",
        name="Assign new positon to the employee",
        response_class=ORJSONResponse,
    )
    async def assign_position_to_employee(
        request: Request,
        employee_id: Annotated[
            int,
            Form(
                title="Employee id",
                example="12",
            ),
        ],
        position_id: Annotated[
            int,
            Form(title="Employee's position id", example="1"),
        ],
        service: Service = Depends(get_service),
        administrator: AdministratorModel = Depends(get_current_user),
    ):
        return await service.assign_position_to_employee(
            administrator,
            employee_id=employee_id,
            position_id=position_id,
        )

    @router.post(
        "/delete_employee",
        name="Delete employee model",
        response_class=ORJSONResponse,
    )
    async def delete_employee(
        request: Request,
        id: Annotated[
            int,
            Form(
                title="Employee id",
                example="12",
            ),
        ],
        full_name: Annotated[
            Optional[str],
            Form(
                title="Employee full name",
                example="Ivan Prokopovich",
            ),
        ] = None,
        service: Service = Depends(get_service),
        current_user: AdministratorModel = Depends(get_current_user),
    ):
        return await service.delete_employee(
            EmployeeFilter(
                ID=id,
                full_name=full_name,
            )
        )

    @router.post(
        "/get_payment_history",
        name="Get employee payment history",
        description="Get employee according to the specified query",
        response_class=ORJSONResponse,
    )
    async def get_employee_payment_history(
        request: Request,
        id: Annotated[
            int,
            Form(
                title="Payment history id",
                example="12",
            ),
        ] = None,
        month: Annotated[
            str,
            Form(
                alias="month",
                title="Payment History Month",
                description="Filter payment history by month",
                example="January",
            ),
        ] = None,
        service: Service = Depends(get_service),
        administrator: AdministratorModel = Depends(get_current_user),
    ) -> list[PaymentHistoryOut]:
        try:
            return await service.get_employee_payment_history_by_criteria(
                administrator,
                filter=PaymentHistoryFilter(
                    ID=id,
                    month=month,
                ),
            )
        except AdministratorNotAllowedException as exc:
            return HTTPException(status_code=405, detail=str(exc))

    @router.post(
        "/payment_history",
        name="Add payment history model",
        response_class=ORJSONResponse,
    )
    async def add_payment_history(
        request: Request,
        employee_id: Annotated[
            int,
            Form(
                title="Employee id",
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
                title="Earnings",
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
        return await service.save_payment_history(
            administrator,
            employee_id,
            dto=SavePaymentHistoryDTO(
                month=month,
                earnings=earnings,
                payments=payments,
                deductions=deductions,
            ),
        )

    @router.post(
        "/delete_payment_history",
        name="Delete payment history model",
        response_class=ORJSONResponse,
    )
    async def delete_payment_history(
        request: Request,
        id: Annotated[
            int,
            Form(
                title="Employee id",
                example="12",
            ),
        ],
        service: Service = Depends(get_service),
        administrator: AdministratorModel = Depends(get_current_user),
    ):
        return await service.delete_payment_history(
            PaymentHistoryFilter(
                ID=id,
            )
        )

    @router.get(
        "/system_metadata",
        name="Get system metadata",
        response_class=ORJSONResponse,
    )
    async def get_system_metadata(
        request: Request,
        service: Service = Depends(get_service),
        administrator: AdministratorModel = Depends(get_current_user),
    ):
        return await service.get_system_metadata(administrator)

    return router
