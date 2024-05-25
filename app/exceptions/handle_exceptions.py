import logging
from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse

from app.exceptions.configure_exceptions import ServerErrorException

logger = logging.getLogger("__main__")


def configure_exceptions_handlers(app: FastAPI):
    @app.exception_handler(Exception)
    async def handle_exception(request: Request, exc: Exception) -> ORJSONResponse:
        logger.error(exc, exc_info=exc)
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"status": False, "content": exc.__str__()},
        )

    @app.exception_handler(ServerErrorException)
    async def handle_server_error_exception(
        request: Request, exc: ServerErrorException
    ) -> ORJSONResponse:
        logger.error(exc, exc_info=exc)
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"status": False, "content": exc.__str__()},
        )
