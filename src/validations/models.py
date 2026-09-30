from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel


class PatientAddress(BaseModel):
    line: list[str]
    city: str
    state: str = "BC"
    postalCode: str
    country: str = "CA"


class PatientName(BaseModel):
    family: str
    given: list[str]
    prefix: list[str]


class PatientMaritalStatus(BaseModel):
    text: str


class Patient(BaseModel):
    resourceType: str = "Patient"
    id: str
    name: list[PatientName]
    gender: Literal["male", "female"]
    birthDate: date
    deceasedDateTime: datetime | None = None
    address: list[PatientAddress]
    maritalStatus: PatientMaritalStatus
    multipleBirthBoolean: bool


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
    address: list[OrganizationAddress]
