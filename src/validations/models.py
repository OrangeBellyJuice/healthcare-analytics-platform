from typing import Literal

from pydantic import BaseModel


class Practitioner(BaseModel):
    resourceType: str = "Practitioner"
    id: str
    family: str
    given: list[str]
    prefix: list[str]
    line: str
    city: str
    state: str = "BC"
    country: str = "CA"
    gender: Literal["male", "female"]
