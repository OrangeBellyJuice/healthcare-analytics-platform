import pytest
from pydantic import ValidationError

from src.validations.models import (
    Condition,
    Encounter,
    Organization,
    Patient,
    Practitioner,
)

valid_encounter = {
    "resourceType": "Encounter",
    "id": "c2aadfa1-256b-c450-48e9-0a5e44171a14",
    "status": "finished",
    "class": {
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
        "code": "AMB",
    },
    "type": [
        {
            "coding": [
                {
                    "system": "http://snomed.info/sct",
                    "code": "185345009",
                    "display": "Encounter for symptom (procedure)",
                }
            ],
            "text": "Encounter for symptom (procedure)",
        }
    ],
    "subject": {
        "reference": "urn:uuid:c2aadfa1-256b-c450-bcd5-442316fa4fe9",
        "display": "Mr. Aaron697 DuBuque211",
    },
    "participant": [
        {
            "individual": {
                "reference": (
                    "Practitioner?identifier="
                    "http://hl7.org/fhir/sid/us-npi|9999976399"
                ),
                "display": "Dr. Arlene209 Olson653",
            }
        }
    ],
    "period": {
        "start": "1997-11-16T08:55:27-08:00",
        "end": "1997-11-16T09:10:27-08:00",
    },
    "reasonCode": [
        {
            "coding": [
                {
                    "system": "http://snomed.info/sct",
                    "code": "444814009",
                    "display": "Viral sinusitis (disorder)",
                }
            ]
        }
    ],
    "serviceProvider": {
        "reference": (
            "Organization?identifier="
            "https://github.com/synthetichealth/synthea|"
            "0e58807a-a5f2-3e7d-a9d6-eca59bc3df95"
        ),
        "display": "Shoreline Medical",
    },
}


valid_condition = {
    "resourceType": "Condition",
    "id": "c2aadfa1-256b-c450-e2a4-42a0880217f0",
    "clinicalStatus": {
        "coding": [
            {
                "system": (
                    "http://terminology.hl7.org/"
                    "CodeSystem/condition-clinical"
                ),
                "code": "resolved",
            }
        ]
    },
    "verificationStatus": {
        "coding": [
            {
                "system": (
                    "http://terminology.hl7.org/"
                    "CodeSystem/condition-ver-status"
                ),
                "code": "confirmed",
            }
        ]
    },
    "code": {
        "coding": [
            {
                "system": "http://snomed.info/sct",
                "code": "109838007",
                "display": (
                    "Overlapping malignant neoplasm "
                    "of colon (disorder)"
                ),
            }
        ],
        "text": "Overlapping malignant neoplasm of colon (disorder)",
    },
    "subject": {
        "reference": "urn:uuid:c2aadfa1-256b-c450-bcd5-442316fa4fe9",
    },
    "encounter": {
        "reference": "urn:uuid:c2aadfa1-256b-c450-8612-54e6414afc28",
    },
    "onsetDateTime": "2002-06-18T00:15:36-07:00",
    "abatementDateTime": "2004-10-23T21:02:28-07:00",
    "recordedDate": "2002-06-18T00:15:36-07:00",
}

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


def test_valid_encounter_passes_validation():
    result = Encounter.model_validate(valid_encounter)

    assert result.id == "c2aadfa1-256b-c450-48e9-0a5e44171a14"
    assert result.resourceType == "Encounter"
    assert result.status == "finished"
    assert result.class_.code == "AMB"
    assert result.subject.reference == (
        "urn:uuid:c2aadfa1-256b-c450-bcd5-442316fa4fe9"
    )
    assert result.period.start.year == 1997


def test_valid_condition_passes_validation():
    result = Condition.model_validate(valid_condition)

    assert result.id == "c2aadfa1-256b-c450-e2a4-42a0880217f0"
    assert result.resourceType == "Condition"
    assert result.clinicalStatus.coding[0].code == "resolved"
    assert result.verificationStatus.coding[0].code == "confirmed"
    assert result.code.coding[0].code == "109838007"


def test_encounter_missing_subject_fails_validation():
    invalid_encounter = valid_encounter.copy()
    invalid_encounter.pop("subject")

    with pytest.raises(ValidationError):
        Encounter.model_validate(invalid_encounter)


def test_condition_missing_code_fails_validation():
    invalid_condition = valid_condition.copy()
    invalid_condition.pop("code")

    with pytest.raises(ValidationError):
        Condition.model_validate(invalid_condition)

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

def test_encounter_without_reason_code_passes_validation():
    encounter = valid_encounter.copy()
    encounter.pop("reasonCode")

    result = Encounter.model_validate(encounter)

    assert result.reasonCode is None


def test_condition_without_abatement_datetime_passes_validation():
    condition = valid_condition.copy()
    condition.pop("abatementDateTime")

    result = Condition.model_validate(condition)

    assert result.abatementDateTime is None  

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
