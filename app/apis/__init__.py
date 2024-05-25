from . import travel
from fastapi import FastAPI
from app.config import config


def configure_routes(app: FastAPI):
    app.include_router(router=travel.router, prefix=config.OPENAPI_PREFIX)
