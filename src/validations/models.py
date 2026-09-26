from typing import Literal

from pydantic import BaseModel


class PractionerName(BaseModel):
    family: str
    given: list[str]
    prefix: list[str]


class PractitionerAddress(BaseModel):
    line: list[str]
    city: str
    state: str = "BC"
    postalCode: str
    country: str = "CA"


class Practitioner(BaseModel):
    resourceType: str = "Practitioner"
    id: str
    name: list[PractionerName]
    address: list[PractitionerAddress]
    gender: Literal["female", "male"]
