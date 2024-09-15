"""This module contains entry point & app configuration"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import get_lab_conf

from app.api.lab1 import lab1_asteroids_router
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

app.include_router(lab1_asteroids_router, prefix="/lab1")
