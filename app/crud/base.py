"""This module contains `BaseCRUD` class"""

from typing import Generic, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from sqlmodel import SQLModel

from pydantic import BaseModel

ModelT = TypeVar("ModelT", bound=SQLModel)
"""SQLModel type variable"""
SchemaT = TypeVar("SchemaT", bound=BaseModel)
"""FastAPI schema type variable"""


# pylint: disable=R0903
class BaseCRUD(Generic[ModelT, SchemaT]):
    """This is base CRUD class. It uses generics to work with defined arguments types"""

    def __init__(self, model: type[ModelT]):
        """Initialize CRUD class"""
        self.model = model

    async def create(
            self,
            *,
            obj_in: SchemaT | ModelT,
            db_session: AsyncSession
    ) -> ModelT:
        """
        This method adds a new instance to the database

        :param obj_in: Instance to be added to the database
        :param db_session: DB session
        :return: Model instance
        """
        if not isinstance(obj_in, self.model):
            db_obj = self.model.model_validate(obj_in)
        else:
            db_obj = obj_in

        db_session.add(db_obj)
        await db_session.commit()
        await db_session.refresh(db_obj)

        return db_obj
