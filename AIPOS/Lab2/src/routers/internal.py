import logging
import os
from datetime import datetime
from typing import Annotated, Any, AsyncGenerator, Callable, Optional

from fastapi import APIRouter, Depends, Form, HTTPException, Query, Request, status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from jose import JWTError, jwt
from pydantic import BaseModel

from src.database import AdministratorFilter, EmployeeFilter, PaymentHistoryFilter
from src.exceptions import AdministratorNotAllowedException
from src.models.models import (
    AdministratorModel,
    CategoryOut,
    EmployeeOut,
    PaymentHistoryOut,
    SystemMetadataOut,
)
from src.service import (
    EmployeePaymentForMonthDTO,
    GetEmployeeDTO,
    MinEmployeeSalaryDTO,
    Service,
)
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
    templates: Jinja2Templates,
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

    @router.get(
        "/categories_for_current_date",
        name="Categories for current date",
        description="Get categories which change date is current date",
        response_class=HTMLResponse,
    )
    async def get_categories_for_current_date(
        request: Request,
        service: Service = Depends(get_service),
    ):
        categories: list[CategoryOut] = await service.get_categories_for_current_date()
        return templates.TemplateResponse(
            "functions/categories_for_current_date.html",
            {
                "request": request,
                "now": datetime.now(),
                "categories": categories,
                "route": "home",
            },
        )

    @router.post(
        "/employee_payments_for_month",
        name="Employee payments for month",
        description="Get employee's payments for specific month",
        response_class=HTMLResponse,
    )
    async def get_employee_payment_for_month(
        request: Request,
        employee_id: Annotated[
            int,
            Form(
                alias="employee_id",
                title="Requested employee",
                example="123",
            ),
        ],
        month: Annotated[
            MonthEnum,
            Form(
                alias="month",
                title="Requested month",
                example="January",
            ),
        ],
        service: Service = Depends(get_service),
        administrator: AdministratorModel = Depends(get_current_user),
    ):
        dto: EmployeePaymentForMonthDTO = await service.get_employee_payment_for_month(
            administrator,
            employee_id=employee_id,
            month=month,
        )

        return templates.TemplateResponse(
            "functions/employee_payments_for_month.html",
            {"request": request, "dto": dto, "route": "home"},
        )

    @router.post(
        "/get_employees_with_min_salary_for_month",
        name="Employee with min salary for the month",
        description="Get employee with min salary for the month",
        response_class=HTMLResponse,
    )
    async def get_employees_with_min_salary_for_month(
        request: Request,
        month: Annotated[
            MonthEnum,
            Form(
                alias="month",
                title="Requested month",
                example="January",
            ),
        ],
        service: Service = Depends(get_service),
        administrator: AdministratorModel = Depends(get_current_user),
    ):
        dtos: list[
            MinEmployeeSalaryDTO
        ] = await service.get_employees_with_min_salary_for_month(
            administrator,
            month=month,
        )
        return templates.TemplateResponse(
            "functions/employees_with_min_salary_for_month.html",
            {"request": request, "dtos": dtos, "route": "home"},
        )

    @router.post(
        "/get_employee",
        name="Get employee model",
        description="Get employee according to the specified query",
        response_class=HTMLResponse,
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
        position: Annotated[
            Optional[str],
            Form(
                title="Employee position",
                example="Developer",
            ),
        ] = None,
        service: Service = Depends(get_service),
        administrator: AdministratorModel = Depends(get_current_user),
    ):
        try:
            dtos: list[GetEmployeeDTO] = await service.get_employee_by_criteria(
                administrator,
                filter=EmployeeFilter(ID=id, full_name=full_name, position=position),
            )

            return templates.TemplateResponse(
                "functions/get_employee.html",
                {"request": request, "dtos": dtos, "route": "home"},
            )
        except AdministratorNotAllowedException as exc:
            return HTTPException(status_code=405, detail=str(exc))

    @router.post(
        "/get_payment_history",
        name="Get employee payment history",
        description="Get employee according to the specified query",
        response_class=HTMLResponse,
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
        employee_id: Annotated[
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
        earnings: Annotated[
            int,
            Form(
                title="Payment history earnings",
                example="12",
            ),
        ] = None,
        payments: Annotated[
            int,
            Form(
                title="Payment history payments",
                example="12",
            ),
        ] = None,
        deductions: Annotated[
            int,
            Form(
                title="Payment history deductions",
                example="12",
            ),
        ] = None,
        service: Service = Depends(get_service),
        administrator: AdministratorModel = Depends(get_current_user),
    ):
        try:
            histories: list[
                PaymentHistoryOut
            ] = await service.get_employee_payment_history_by_criteria(
                administrator,
                filter=PaymentHistoryFilter(
                    ID=id,
                    employee_id=employee_id,
                    month=month,
                    earnings=earnings,
                    payments=payments,
                    deductions=deductions,
                ),
            )
            return templates.TemplateResponse(
                "functions/get_payment_history.html",
                {"request": request, "histories": histories, "route": "home"},
            )
        except AdministratorNotAllowedException as exc:
            return HTTPException(status_code=405, detail=str(exc))

    @router.get(
        "/system_metadata",
        name="Get system metadata",
        response_class=HTMLResponse,
    )
    async def get_system_metadata(
        request: Request,
        service: Service = Depends(get_service),
        administrator: AdministratorModel = Depends(get_current_user),
    ):
        metadata: SystemMetadataOut = await service.get_system_metadata(administrator)
        return templates.TemplateResponse(
            "functions/get_system_metadata.html",
            {"request": request, "system_metadata": metadata, "route": "home"},
        )

    return router

    return router
