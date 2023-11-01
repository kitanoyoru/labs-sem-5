from __future__ import annotations

from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles
#from fastapi.templating import Jinja2Templates

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request as StarletteRequest

#import jinja2

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker

from src.service import Service

from src.config import create_engine_from_env, get_directories

from src.routers.v0 import create_router as create_api_router
#from src.routers.internal import create_router as create_internal_router


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
    engine = create_engine_from_env()

    return create_app_with_config(
        engine=engine,
    )

def create_app_with_config(
    engine: AsyncEngine
) -> FastAPI:
    directories = get_directories()

    app = FastAPI(
        title="Lab2",
        version="0.1.0",
        description="This is the Lab1 API.",
        swagger_ui_parameters={
            "defaultModelsExpandDepth": -1,
            "displayRequestDuration": 1,
        },
    )
    app.add_middleware(CustomCORSMiddleware)

    #templates = Jinja2Templates(
    #    directory=directories.templates,
    #    undefined=jinja2.StrictUndefined,
    #)

    app.mount(
        "/static",
        StaticFiles(directory=directories.static),
        name="static",
    )

    SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

    async def get_service():
        async with SessionLocal() as session:
            async with session.begin():
                service = Service.from_session(session)
                yield service

    api_router = create_api_router(get_service)
    app.include_router(api_router, prefix="/api/v0", tags=["api"])

    #internal_router = create_internal_router(templates, get_service)
    #app.include_router(internal_router, prefix="internal", tags=["internal"])

    return app

