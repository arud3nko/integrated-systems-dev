"""This module provides `BaseSQLModel` class"""

from sqlmodel import SQLModel

from sqlalchemy.ext.declarative import declared_attr


class BaseSQLModel(SQLModel):
    """This class provides base model functions"""

    @declared_attr  # type: ignore
    def __tablename__(cls) -> str:
        """Sets __tablename__ attribute using lower class name and tables prefix"""
        return cls.__name__.lower()
