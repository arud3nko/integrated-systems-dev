"""This module provides Asteroids Data endpoint"""

from fastapi import APIRouter, BackgroundTasks, status
from fastapi.requests import Request
from fastapi.responses import Response

from pydantic import ValidationError

from app.db import SessionLocal
from app.schemas.lab1 import AsteroidSchema
from app.crud.lab1 import AsteroidCRUD

from app.lab1.neowise import NeowiseAPIClient

router = APIRouter()


@router.get("/parse-asteroids/", response_model=list[AsteroidSchema])
async def parse_nearby_asteroids_list(
        request: Request,
        background_tasks: BackgroundTasks,
):
    """Get asteroids list from API client & start background task to save them to DB"""

    neowise_api_client: NeowiseAPIClient = request.state.neowise_api_client

    try:
        asteroids = await neowise_api_client.get_asteroids()
    except ValidationError:
        return Response(status_code=status.HTTP_400_BAD_REQUEST, content="Incompatible schema")

    async with SessionLocal() as db_session:
        background_tasks.add_task(AsteroidCRUD().create_from_list, obj_in=asteroids, db_session=db_session)

    return asteroids
