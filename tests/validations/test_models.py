import pytest
from pydantic import ValidationError

from src.validations.models import Organization, Patient, Practitioner

valid_patient = {
    "resourceType": "Patient",
    "id": "c2aadfa1-256b-c450-bcd5-442316fa4fe9",
    "name": [
        {
            "use": "official",
            "family": "DuBuque211",
            "given": ["Aaron697"],
            "prefix": ["Mr."],
        }
    ],
    "gender": "male",
    "birthDate": "1951-04-21",
    "deceasedDateTime": "2007-05-20T04:55:27-07:00",
    "address": [
        {
            "line": ["818 Rodriguez Junction Unit 57"],
            "city": "Sidney",
            "state": "BC",
            "postalCode": "V8L",
            "country": "CA",
        }
    ],
    "maritalStatus": {
        "text": "Married",
    },
    "multipleBirthBoolean": False,
}

valid_practitioner = {
    "resourceType": "Practitioner",
    "id": "4ac6772e-f4cd-3862-b53c-bb433031afc9",
    "name": [
        {
            "family": "Schumm995",
            "given": ["Hilari0934"],
            "prefix": ["Dr."],
        }
    ],
    "address": [
        {
            "line": ["201-7315 edmonds street"],
            "city": "Burnaby",
            "state": "BC",
            "postalCode": "V3N 1A7",
            "country": "CA",
        }
    ],
    "gender": "male",
}

valid_organization = {
    "resourceType": "Organization",
    "id": "231f25bb-2bdc-31e6-b187-3e666cb9f8fa",
    "name": "Primecare Medical Centre",
    "address": [
        {
            "line": ["201-7315 edmonds street"],
            "city": "Burnaby",
            "state": "BC",
            "postalCode": "V3N 1A7",
            "country": "CA",
        }
    ],
}


def test_valid_patient_passes_validation():
    result = Patient.model_validate(valid_patient)

    assert result.id == "c2aadfa1-256b-c450-bcd5-442316fa4fe9"
    assert result.resourceType == "Patient"
    assert result.name[0].family == "DuBuque211"
    assert result.address[0].state == "BC"


def test_valid_organization_passes_validation():
    result = Organization.model_validate(valid_organization)

    assert result.id == "231f25bb-2bdc-31e6-b187-3e666cb9f8fa"
    assert result.resourceType == "Organization"
    assert result.name == "Primecare Medical Centre"
    assert result.address[0].state == "BC"


def test_valid_practitioner_passes_validation():
    result = Practitioner.model_validate(valid_practitioner)

    assert result.id == "4ac6772e-f4cd-3862-b53c-bb433031afc9"
    assert result.resourceType == "Practitioner"
    assert result.name[0].family == "Schumm995"
    assert result.address[0].state == "BC"


def test_patient_missing_name_fails_validation():
    invalid_patient = valid_patient.copy()
    invalid_patient.pop("name")

    with pytest.raises(ValidationError):
        Patient.model_validate(invalid_patient)


def test_organization_missing_name_fails_validation():
    invalid_organization = valid_organization.copy()
    invalid_organization.pop("name")

    with pytest.raises(ValidationError):
        Organization.model_validate(invalid_organization)


def test_practitioner_missing_name_fails_validation():
    invalid_practitioner = valid_practitioner.copy()
    invalid_practitioner.pop("name")

    with pytest.raises(ValidationError):
        Practitioner.model_validate(invalid_practitioner)
