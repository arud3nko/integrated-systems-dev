"""This module provides Asteroids Data endpoint"""

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession

from sqlmodel import select

from app.schemas.lab1 import AsteroidSchema
from app.crud.lab1 import AsteroidCRUD
from app.db.lab1 import Asteroid

from app.api import get_db


router = APIRouter()


@router.get("/asteroids/", response_model=list[Asteroid])
async def get_asteroids_list(
        filter_by: AsteroidSchema = Depends(),
        db_session: AsyncSession = Depends(get_db)
):
    """
    Get asteroids list

    :param filter_by: Filter by AsteroidSchema fields
    :param db_session: DB session
    """

    if any([getattr(filter_by, field_name) for field_name, _ in filter_by.__fields__.items()]):
        return await AsteroidCRUD().get_filtered(obj=filter_by, db_session=db_session)

    return await AsteroidCRUD().get(db_session=db_session)


@router.get("/amount/asteroids/")
async def get_asteroids_amount(db_session: AsyncSession = Depends(get_db)):
    """
    Get asteroids amount

    :param db_session: DB session
    """

    asteroids = await AsteroidCRUD().get(db_session=db_session)

    return JSONResponse(content={"asteroids": len(asteroids)})


@router.get("/last_updated/asteroids/")
async def get_asteroids_last_updated(db_session: AsyncSession = Depends(get_db)):
    """
    Get asteroids last updated datetime

    :param db_session: DB session
    """

    query = select(Asteroid).order_by(Asteroid.updated_at.desc())

    last_updated_at = await db_session.execute(query)
    last_updated_at = last_updated_at.scalars().first()

    return JSONResponse(content={"last_updated_at": str(last_updated_at.updated_at)})


@router.get("/asteroids/{id}/", response_model=Asteroid)
async def get_asteroid(
        id: int,
        db_session: AsyncSession = Depends(get_db),
):
    """
    Get asteroid, specified by ID

    :param id: Asteroid ID
    :param db_session: DB session
    """
    asteroid = await AsteroidCRUD().get_by_id(obj_id=id, db_session=db_session)

    return asteroid


@router.post("/asteroids/", response_model=Asteroid)
async def create_asteroid(
        asteroid: AsteroidSchema,
        db_session: AsyncSession = Depends(get_db)
):
    """
    Create asteroid, specified by ID

    :param asteroid: Asteroid data
    :param db_session: DB session
    """
    asteroid = await AsteroidCRUD().create(obj_in=asteroid, db_session=db_session)

    return asteroid
