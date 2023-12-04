import logging
import os
from datetime import datetime, timedelta
from typing import Annotated, Any, AsyncGenerator, Callable

import requests

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import ORJSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from src.database import AdministratorFilter
from src.models.models import AdministratorModel
from src.service import Service

logger = logging.getLogger(__file__)

SECRET_KEY = os.environ["AUTH_SECRET_KEY"]
ALGORITHM = os.environ["AUTH_ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ["AUTH_ACCESS_TOKEN_EXPIRE_MINUTES"])

GOOGLE_CLIENT_ID = os.environ["GOOGLE_CLIENT_ID"] 
GOOGLE_CLIENT_SECRET = os.environ["GOOGLE_CLIENT_SECRET"] 
GOOGLE_REDIRECT_URI = os.environ["GOOGLE_REDIRECT_URI"] 

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Token(BaseModel):
    access_token: str
    token_type: str


def create_router(
    get_service: Callable[[], AsyncGenerator[Service, Any]],
) -> APIRouter:
    router = APIRouter()

    @router.post("/token")
    async def login_administrator(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        service: Service = Depends(get_service),
    ):
        user = await _authenticate_user(form_data.username, form_data.password, service)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.full_name}, expires_delta=access_token_expires
        )

        response = ORJSONResponse(
            {"access_token": access_token, "token_type": "bearer"}
        )

        response.set_cookie(
            key="access_token",
            value=access_token,
            expires=access_token_expires.total_seconds(),
            httponly=True,
        )

        return response

    @router.get("/login/google")
    async def login_google():
        return {
            "url": f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"
        }

    @router.get("/auth/google")
    async def auth_google(code: str):
        token_url = "https://accounts.google.com/o/oauth2/token"
        data = {
            "code": code,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri": GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }
        # TODO: change to the httpx
        response = requests.post(token_url, data=data)
        access_token = response.json().get("access_token")
        user_info = requests.get("https://www.googleapis.com/oauth2/v1/userinfo", headers={"Authorization": f"Bearer {access_token}"})
        return user_info.json()

    async def _authenticate_user(
        username: str, password: str, service: Service
    ) -> AdministratorModel:
        user = await _get_user(username, service)
        if not user:
            return False

        if not __verify_password(password, user.hashed_password):
            return False

        return user

    async def _get_user(username: str, service: Service) -> AdministratorModel:
        result = await service.get_administrator_by_criteria(
            filter=AdministratorFilter(full_name=username)
        )
        return result[0]

    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def __verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    return router
