"""This module contains `Asteroid` CRUD"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_

from loguru import logger

from app.crud import BaseCRUD
from app.crud.base import SchemaT, ModelT

from app.db.lab1 import Asteroid
from app.schemas.lab1 import AsteroidSchema


# pylint: disable=R0903
class AsteroidCRUD(BaseCRUD[Asteroid, AsteroidSchema]):
    """`Asteroid` model CRUD"""
    def __init__(self):
        super().__init__(Asteroid)

    async def create_from_list(
            self,
            *,
            obj_in: list[SchemaT] | list[ModelT],
            db_session: AsyncSession
    ):
        """Save list of Asteroid instances to DB"""

        logger.info(f"Creating {len(obj_in)} instances of class {obj_in[0].__class__}")

        for asteroid in obj_in:
            await self.create(obj_in=asteroid, db_session=db_session)

    @staticmethod
    async def get_filtered(
            *,
            obj: AsteroidSchema,
            db_session: AsyncSession
    ) -> ModelT | None:

        filter_clauses = [getattr(Asteroid, field_name) == getattr(obj, field_name)
                          for field_name, _ in obj.dict(exclude_none=True).items()]

        query = select(Asteroid).where(and_(*filter_clauses))

        response = await db_session.execute(query)

        return response.scalars().all()
