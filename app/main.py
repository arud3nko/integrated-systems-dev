"""This module contains entry point & app configuration"""

from contextlib import asynccontextmanager

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI

from app import get_lab_conf, get_app_conf

from app.middlewares import BearerTokenAuthorizationMiddleware

from app.api.endpoints import (
    lab1,
    lab2,
)
from app.lab1.neowise import NeowiseAPIClient


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
        Contains lifespan events.
    """

    lab_conf = get_lab_conf()

    neowise_api_client = NeowiseAPIClient(lab_conf.neowise_api_url)

    yield {
        "neowise_api_client": neowise_api_client
    }


app = FastAPI(lifespan=lifespan)

app_conf = get_app_conf()

app.include_router(lab1)
app.include_router(lab2)

bearer_auth_middleware = BearerTokenAuthorizationMiddleware(token=app_conf.TOKEN)

app.add_middleware(BaseHTTPMiddleware, dispatch=bearer_auth_middleware)

