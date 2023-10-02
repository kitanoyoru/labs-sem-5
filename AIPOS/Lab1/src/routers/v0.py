import os

from fastapi import APIRouter
from fastapi.responses import ORJSONResponse, StreamingResponse

from src.config import Directories
from src.errors import FileNotFound


def create_router(
    directories: Directories,
) -> APIRouter:
    router = APIRouter()

    @router.get(
        "/{file_path}",
        response_class=StreamingResponse,
        name="Get file",
        description="Get file according to the requested file path",
    )
    async def get_file(file_path: str):
        host_file_path = os.path.join(directories.static, file_path)

        if os.path.isfile(host_file_path):
            file_stream = open(host_file_path, mode="rb")
            print("hello")
            return StreamingResponse(file_stream, media_type="application/octet-stream")

        raise FileNotFound(f"File {file_path} not found")

    @router.options(
        "/{file_path}",
        response_class=ORJSONResponse,
        name="Check existance of the requested file and get allowed methods",
    )
    async def options_file(file_path: str):
        host_file_path = os.path.join(directories.static, file_path)

        allowed_methods = ["GET", "OPTIONS"]
        file_exist = os.path.isfile(host_file_path)

        return {"allow": allowed_methods, "exists": file_exist}

    return router
