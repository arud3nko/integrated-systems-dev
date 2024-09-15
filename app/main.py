"""This module contains entry point & app configuration"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.lab1 import lab1_asteroids_router

from app.lab1.neowise import NeowiseAPIClient


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
        Contains lifespan events.
    """

    neowise_api_client = NeowiseAPIClient("https://data.nasa.gov/resource/2vr3-k9wn.json")

    yield {
        "neowise_api_client": neowise_api_client
    }


app = FastAPI(lifespan=lifespan)

app.include_router(lab1_asteroids_router, prefix="/lab1")
