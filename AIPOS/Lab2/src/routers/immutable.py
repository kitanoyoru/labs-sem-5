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

    @router.get("/login", response_class=HTMLResponse)
    def login(request: Request):
        return templates.TemplateResponse(
            "login.html", {"request": request, "route": "home"}
        )

    @router.get("/services/get/employee", response_class=HTMLResponse)
    def get_employee_form(request: Request):
        return templates.TemplateResponse(
            "get/employee/index.html", {"request": request, "route": "home"}
        )

    @router.get("/services/get/payment_history", response_class=HTMLResponse)
    def get_payment_history_form(request: Request):
        return templates.TemplateResponse(
            "get/payment_history/index.html", {"request": request, "route": "home"}
        )

    @router.get("/services/get/system_metadata", response_class=HTMLResponse)
    def get_system_metadata_form(request: Request):
        return templates.TemplateResponse(
            "get/system_metadata/index.html", {"request": request, "route": "home"}
        )

    @router.get("/services/get/position", response_class=HTMLResponse)
    def get_position_form(request: Request):
        return templates.TemplateResponse(
            "get/position/index.html", {"request": request, "route": "home"}
        )

    @router.get("/services/post/employee", response_class=HTMLResponse)
    def post_employee_form(request: Request):
        return templates.TemplateResponse(
            "post/employee/index.html", {"request": request, "route": "home"}
        )

    @router.get("/services/post/payment_history", response_class=HTMLResponse)
    def post_payment_history_form(request: Request):
        return templates.TemplateResponse(
            "post/payment_history/index.html", {"request": request, "route": "home"}
        )

    @router.get("/services/post/position", response_class=HTMLResponse)
    def post_position_form(request: Request):
        return templates.TemplateResponse(
            "post/position/index.html", {"request": request, "route": "home"}
        )

    @router.get("/services/delete/employee", response_class=HTMLResponse)
    def delete_employee_form(request: Request):
        return templates.TemplateResponse(
            "delete/employee/index.html", {"request": request, "route": "home"}
        )

    @router.get("/services/delete/payment_history", response_class=HTMLResponse)
    def delete_payment_history_form(request: Request):
        return templates.TemplateResponse(
            "delete/payment_history/index.html", {"request": request, "route": "home"}
        )

    @router.get("/services/patch/employee", response_class=HTMLResponse)
    def patch_payment_history_form(request: Request):
        return templates.TemplateResponse(
            "patch/employee/index.html", {"request": request, "route": "home"}
        )

    @router.get("/services/patch/position", response_class=HTMLResponse)
    def patch_position_form(request: Request):
        return templates.TemplateResponse(
            "patch/position/index.html", {"request": request, "route": "home"}
        )

    return router
