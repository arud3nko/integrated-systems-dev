"""This module contains Asteroid ORM model"""

from sqlmodel import Field

from app.db import BaseSQLModel


class Asteroid(BaseSQLModel, table=True):
    """This class contains Asteroid model fields"""

    id: int | None = Field(primary_key=True, default=None)

    discovery_date: str
    designation: str = Field(nullable=False, unique=True)
    h_mag: float | None = Field(nullable=True)
    moid_au: float | None = Field(nullable=True)
    q_au_1: float | None = Field(nullable=True)
    q_au_2: float | None = Field(nullable=True)
    period_yr: float | None = Field(nullable=True)
    i_deg: float | None = Field(nullable=True)
    pha: str | None = Field(nullable=True)
    orbit_class: str | None = Field(nullable=True)
