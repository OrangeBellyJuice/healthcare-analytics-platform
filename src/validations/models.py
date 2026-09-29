from typing import Literal

from pydantic import BaseModel


class PractitionerName(BaseModel):
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
    name: list[PractitionerName]
    address: list[PractitionerAddress]
    gender: Literal["female", "male"]


class OrganizationAddress(BaseModel):
    line: list[str]
    city: str
    state: str = "BC"
    postalCode: str
    country: str = "CA"


class Organization(BaseModel):
    resourceType: str = "Organization"
    id: str
    name: str
    address: Literal[Organization]
