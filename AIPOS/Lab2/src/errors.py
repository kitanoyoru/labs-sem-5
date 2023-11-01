from fastapi import HTTPException, status


class APIBaseException(HTTPException):
    ...


class FileNotFound(APIBaseException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
