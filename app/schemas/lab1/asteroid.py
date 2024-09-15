"""This module contains NEOWISE Near Asteroids API mapping schema"""

from pydantic import BaseModel


class AsteroidSchema(BaseModel):
    """This model contains Asteroid schema fields"""

    designation: str
    discovery_date: str
    h_mag: float | None = None
    moid_au: float | None = None
    q_au_1: float | None = None
    q_au_2: float | None = None
    period_yr: float | None = None
    i_deg: float | None = None
    pha: str | None = None
    orbit_class: str | None = None
