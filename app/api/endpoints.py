"""This module contains all available API endpoints"""

from fastapi import APIRouter

from app.api.lab1 import lab1_asteroids_router
from app.api.lab2 import lab2_asteroids_router


lab1 = APIRouter(
    prefix="/lab1"
)
lab1.include_router(lab1_asteroids_router)

lab2 = APIRouter(
    prefix="/lab2"
)
lab2.include_router(lab2_asteroids_router)
