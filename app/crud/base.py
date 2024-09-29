"""This module contains `BaseCRUD` class"""

from typing import Generic, TypeVar, Any

from sqlalchemy.ext.asyncio import AsyncSession

from sqlmodel import SQLModel, select

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

    async def get(
            self,
            *,
            db_session: AsyncSession
    ) -> list[ModelT] | None:
        """
        This method reads the instances from the database

        :param db_session: DB session
        :return: Model instances
        """
        query = select(self.model)
        response = await db_session.execute(query)

        return response.scalars().all()

    async def get_by_id(
            self,
            *,
            obj_id: int,
            db_session: AsyncSession
    ) -> ModelT | None:
        """Get object specified by `id` field"""
        query = select(self.model).where(self.model.id == obj_id)
        response = await db_session.execute(query)

        return response.scalars().one()

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

    async def update(
            self,
            *,
            obj_current: ModelT,
            obj_new: SchemaT | dict[str, Any] | ModelT,
            db_session: AsyncSession
    ) -> ModelT:
        """
        This method updates instance in DB

        :param obj_current: Instance to be updated
        :param obj_new: New instance
        :param db_session: DB session
        :return:
        """

        if isinstance(obj_new, dict):
            update_data = obj_new
        else:
            update_data = obj_new.dict(exclude={"id", "created_at", })
        for field in update_data:
            setattr(obj_current, field, update_data[field])

        db_session.add(obj_current)
        await db_session.commit()
        await db_session.refresh(obj_current)

        return obj_current
