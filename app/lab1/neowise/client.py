"""This module provides `NeowiseAPIClient` class """

from httpx import AsyncClient

from loguru import logger

from pydantic import ValidationError

from app.schemas.lab1 import AsteroidSchema


class NeowiseAPIClient(AsyncClient):
    """This class contains Neowise API functionality"""
    def __init__(self, url: str):
        """
        Initialization

        :param url: Neowise API URL
        """
        self.url = url
        super().__init__()

    async def get_asteroids(self) -> list[AsteroidSchema]:
        """Sends GET request & returns deserialized dict"""

        logger.info("Requesting Neowise API...")

        response = await self.get(url=self.url)

        asteroids = response.json()

        if not isinstance(asteroids, list):
            raise ValidationError.from_exception_data("Asteroids list was not provided", [])

        return [AsteroidSchema(**asteroid_data) for asteroid_data in asteroids]
