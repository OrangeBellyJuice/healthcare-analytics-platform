from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, Field


class Coding(BaseModel):
    system: str | None = None
    code: str
    display: str | None = None


class CodeableConcept(BaseModel):
    coding: list[Coding]
    text: str | None = None


class Reference(BaseModel):
    reference: str
    display: str | None = None


class Period(BaseModel):
    start: datetime
    end: datetime

class Quantity(BaseModel):
    value: float
    unit: str | None = None
    system: str | None = None
    code: str | None = None


class ObservationComponent(BaseModel):
    code: CodeableConcept
    valueQuantity: Quantity


class Observation(BaseModel):
    resourceType: Literal["Observation"]
    id: str
    status: str
    category: list[CodeableConcept]
    code: CodeableConcept
    subject: Reference
    encounter: Reference
    effectiveDateTime: datetime
    issued: datetime
    valueQuantity: Quantity | None = None
    valueCodeableConcept: CodeableConcept | None = None
    component: list[ObservationComponent] | None = None


class Procedure(BaseModel):
    resourceType: Literal["Procedure"]
    id: str
    status: str
    code: CodeableConcept
    subject: Reference
    encounter: Reference
    performedPeriod: Period
    reasonCode: list[CodeableConcept] | None = None
    reasonReference: list[Reference] | None = None


class MedicationTimingRepeat(BaseModel):
    frequency: int | None = None
    period: float | None = None
    periodUnit: str | None = None


class MedicationTiming(BaseModel):
    repeat: MedicationTimingRepeat


class DoseAndRate(BaseModel):
    doseQuantity: Quantity | None = None


class DosageInstruction(BaseModel):
    sequence: int | None = None
    text: str | None = None
    asNeededBoolean: bool | None = None
    timing: MedicationTiming | None = None
    doseAndRate: list[DoseAndRate] | None = None


class MedicationRequest(BaseModel):
    resourceType: Literal["MedicationRequest"]
    id: str
    status: str
    intent: str
    medicationCodeableConcept: CodeableConcept
    subject: Reference
    encounter: Reference
    authoredOn: datetime
    requester: Reference
    dosageInstruction: list[DosageInstruction] | None = None
    reasonReference: list[Reference] | None = None


class Address(BaseModel):
    line: list[str]
    city: str
    state: str
    postalCode: str
    country: str



class EncounterParticipant(BaseModel):
    individual: Reference


class Encounter(BaseModel):
    resourceType: Literal["Encounter"]
    id: str
    status: str
    class_: Coding = Field(alias="class")
    type: list[CodeableConcept]
    subject: Reference
    participant: list[EncounterParticipant]
    period: Period
    reasonCode: list[CodeableConcept] | None = None
    serviceProvider: Reference


class Condition(BaseModel):
    resourceType: Literal["Condition"]
    id: str

    clinicalStatus: CodeableConcept
    verificationStatus: CodeableConcept
    code: CodeableConcept

    subject: Reference
    encounter: Reference

    onsetDateTime: datetime
    abatementDateTime: datetime | None = None
    recordedDate: datetime

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
