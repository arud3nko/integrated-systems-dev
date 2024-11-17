"""This module provides `BaseSQLModel` class"""

import datetime

from sqlmodel import SQLModel, Field

from sqlalchemy.ext.declarative import declared_attr


class BaseSQLModel(SQLModel):
    """This class provides base model functions"""

    @declared_attr  # type: ignore
    def __tablename__(cls) -> str:
        """Sets __tablename__ attribute using lower class name and tables prefix"""
        return cls.__name__.lower()

    created_at: datetime.datetime = Field(
        default=datetime.datetime.now(),
        nullable=False,
    )

    updated_at: datetime.datetime = Field(
            default_factory=datetime.datetime.now,
            nullable=False,
        )
