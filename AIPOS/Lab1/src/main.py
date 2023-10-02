from __future__ import annotations

from fastapi import FastAPI, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request as StarletteRequest

from .config import get_directories
from .routers.v0 import create_router as create_api_router


class CustomCORSMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: StarletteRequest, call_next: RequestResponseEndpoint
    ) -> Response:
        response = await call_next(request)
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "*"
        return response


def create_app() -> FastAPI:
    directories = get_directories()

    app = FastAPI(
        title="Lab1",
        version="0.1.0",
        description="This is the Lab1 API.",
        swagger_ui_parameters={
            "defaultModelsExpandDepth": -1,
            "displayRequestDuration": 1,
        },
    )
    app.add_middleware(CustomCORSMiddleware)

    api_router = create_api_router(directories)
    app.include_router(api_router, prefix="/api/v0", tags=["api"])

    return app
