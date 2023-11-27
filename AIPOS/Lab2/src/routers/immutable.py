from __future__ import annotations

import os
from typing import Annotated, Any, AsyncGenerator, Callable

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from jose import JWTError, jwt
from pydantic import BaseModel
from starlette.responses import HTMLResponse

from src.database import AdministratorFilter, AdministratorModel
from src.service import Service

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
        token: Annotated[str, Depends(oauth2_scheme)],
        service: Service = Depends(get_service),
    ) -> AdministratorModel:
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

    @router.get("/", response_class=HTMLResponse)
    def index(request: Request):
        return templates.TemplateResponse(
            "index.html", {"request": request, "route": "home"}
        )

    @router.get("/services/get/employee", response_class=HTMLResponse)
    def get_employee_form(request: Request):
        return templates.TemplateResponse(
            "get/employee/index.html", {"request": request, "route": "home"}
        )

    @router.get("/employee/{employee_id}", response_class=HTMLResponse)
    async def get_employee_template(
        request: Request,
        employee_id,
        service: Service = Depends(get_service),
        administrator: AdministratorModel = Depends(get_current_user),
    ):
        try:
            employees = await service.get_employee_by_criteria()
            assert len(employees) == 1
        except AssertionError:
            return templates.TemplateResponse("404.html")

        return templates.TemplateResponse(
            "employee_detail.html",
            {"request": request, "employee": employees[0], "route": "home"},
        )

    @router.get("/payment_history")
    def get_paymeny_history_form():
        ...

    @router.get("/system_metadata")
    def get_system_metadata_form():
        ...

    return router