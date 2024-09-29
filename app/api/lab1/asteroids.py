"""This module provides Asteroids Data endpoint"""

from json import JSONDecodeError

from httpx import HTTPError

from fastapi import APIRouter, BackgroundTasks, status
from fastapi.responses import JSONResponse

from loguru import logger

from pydantic import ValidationError

from app.db import SessionLocal
from app.schemas.lab1 import AsteroidSchema
from app.crud.lab1 import AsteroidCRUD

from app.lab1.neowise import NeowiseAPIClient

router = APIRouter()


@router.get("/parse-asteroids/", response_model=list[AsteroidSchema])
async def parse_nearby_asteroids_list(
        path: str,
        background_tasks: BackgroundTasks,
):
    """Get asteroids list from API client & start background task to save them to DB"""

    logger.info(f"Requested parsing {path}")

    neowise_api_client = NeowiseAPIClient(path)

    try:
        asteroids = await neowise_api_client.get_asteroids()
    except JSONDecodeError as exc:
        logger.error(exc)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"err": "Invalid JSON"})
    except ValidationError as exc:
        logger.error(exc)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"err": "Incompatible schema", "detail": exc.title})
    except HTTPError as exc:
        logger.error(exc)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"err": "HTTP client raised exception", "detail": str(exc)}
        )

    logger.success(f"Successfully parsed asteroids")

    async with SessionLocal() as db_session:
        background_tasks.add_task(AsteroidCRUD().create_from_list, obj_in=asteroids, db_session=db_session)

    logger.success(f"Successfully saved to database")

    return asteroids
