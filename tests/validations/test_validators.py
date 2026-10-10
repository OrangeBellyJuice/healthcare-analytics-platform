from src.validations.models import (
    Condition,
    Encounter,
    MedicationRequest,
    Observation,
    ObservationComponent,
    Organization,
    Patient,
    Practitioner,
    Procedure,
)
from src.validations.validators import validate_resource, validation

patient_resource = [
    {
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
]

organization_resource = [
    {
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
]

practitioner_resource = [
    {
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
]

encounter_resource = [
    {
        "resourceType": "Encounter",
        "id": "encounter-1",
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
                        "display": "Encounter for symptom",
                    }
                ]
            }
        ],
        "subject": {
            "reference": "urn:uuid:patient-1",
        },
        "participant": [
            {
                "individual": {
                    "reference": "Practitioner?identifier=npi|123",
                }
            }
        ],
        "period": {
            "start": "2026-01-01T10:00:00-07:00",
            "end": "2026-01-01T10:30:00-07:00",
        },
        "serviceProvider": {
            "reference": "Organization?identifier=org-1",
        },
    }
]


condition_resource = [
    {
        "resourceType": "Condition",
        "id": "condition-1",
        "clinicalStatus": {
            "coding": [
                {
                    "code": "active",
                }
            ]
        },
        "verificationStatus": {
            "coding": [
                {
                    "code": "confirmed",
                }
            ]
        },
        "code": {
            "coding": [
                {
                    "code": "123456",
                    "display": "Example condition",
                }
            ]
        },
        "subject": {
            "reference": "urn:uuid:patient-1",
        },
        "encounter": {
            "reference": "urn:uuid:encounter-1",
        },
        "onsetDateTime": "2026-01-01T10:00:00-07:00",
        "recordedDate": "2026-01-01T10:00:00-07:00",
    }
]


observation_resource = [
    {
        "resourceType": "Observation",
        "id": "observation-1",
        "status": "final",
        "category": [
            {
                "coding": [
                    {
                        "code": "vital-signs",
                        "display": "Vital signs",
                    }
                ]
            }
        ],
        "code": {
            "coding": [
                {
                    "code": "8302-2",
                    "display": "Body Height",
                }
            ]
        },
        "subject": {
            "reference": "urn:uuid:patient-1",
        },
        "encounter": {
            "reference": "urn:uuid:encounter-1",
        },
        "effectiveDateTime": "2026-01-01T10:00:00-07:00",
        "issued": "2026-01-01T10:00:00-07:00",
        "valueQuantity": {
            "value": 175.0,
            "unit": "cm",
        },
    }
]


observation_component_resource = [
    {
        "code": {
            "coding": [
                {
                    "code": "8480-6",
                    "display": "Systolic Blood Pressure",
                }
            ]
        },
        "valueQuantity": {
            "value": 120,
            "unit": "mm[Hg]",
        },
    }
]


procedure_resource = [
    {
        "resourceType": "Procedure",
        "id": "procedure-1",
        "status": "completed",
        "code": {
            "coding": [
                {
                    "code": "23426006",
                    "display": "Example procedure",
                }
            ]
        },
        "subject": {
            "reference": "urn:uuid:patient-1",
        },
        "encounter": {
            "reference": "urn:uuid:encounter-1",
        },
        "performedPeriod": {
            "start": "2026-01-01T10:00:00-07:00",
            "end": "2026-01-01T10:30:00-07:00",
        },
    }
]


medication_request_resource = [
    {
        "resourceType": "MedicationRequest",
        "id": "medication-1",
        "status": "completed",
        "intent": "order",
        "medicationCodeableConcept": {
            "coding": [
                {
                    "code": "308192",
                    "display": "Amoxicillin 500 MG Oral Tablet",
                }
            ]
        },
        "subject": {
            "reference": "urn:uuid:patient-1",
        },
        "encounter": {
            "reference": "urn:uuid:encounter-1",
        },
        "authoredOn": "2026-01-01T10:00:00-07:00",
        "requester": {
            "reference": "Practitioner?identifier=npi|123",
        },
    }
]


def test_validate_resource_for_success():

    result = validate_resource(organization_resource[0], Organization)
    assert result["resourceType"] == "Organization"

    result = validate_resource(practitioner_resource[0], Practitioner)
    assert result["resourceType"] == "Practitioner"

    result = validate_resource(patient_resource[0], Patient)
    assert result["resourceType"] == "Patient"

    result = validate_resource(encounter_resource[0], Encounter)
    assert result["resourceType"] == "Encounter"

    result = validate_resource(condition_resource[0], Condition)
    assert result["resourceType"] == "Condition"

    result = validate_resource(observation_resource[0], Observation)
    assert result["resourceType"] == "Observation"

    result = validate_resource(
        observation_component_resource[0],
        ObservationComponent,
    )
    assert result["code"]["coding"][0]["code"] == "8480-6"

    result = validate_resource(procedure_resource[0], Procedure)
    assert result["resourceType"] == "Procedure"

    result = validate_resource(
        medication_request_resource[0],
        MedicationRequest,
    )
    assert result["resourceType"] == "MedicationRequest"


def test_validation_for_failure():

    bad_organization_resource = organization_resource[0].copy()
    bad_organization_resource.pop("address")

    assert validation([bad_organization_resource]) == []

    bad_practitioner_resource = practitioner_resource[0].copy()
    bad_practitioner_resource.pop("gender")

    assert validation([bad_practitioner_resource]) == []

    bad_patient_resource = patient_resource[0].copy()
    bad_patient_resource.pop("gender")

    assert validation([bad_patient_resource]) == []

    bad_encounter_resource = encounter_resource[0].copy()
    bad_encounter_resource.pop("subject")

    assert validation([bad_encounter_resource]) == []

    bad_condition_resource = condition_resource[0].copy()
    bad_condition_resource.pop("code")

    assert validation([bad_condition_resource]) == []

    bad_observation_resource = observation_resource[0].copy()
    bad_observation_resource.pop("code")

    assert validation([bad_observation_resource]) == []

    bad_procedure_resource = procedure_resource[0].copy()
    bad_procedure_resource.pop("code")

    assert validation([bad_procedure_resource]) == []

    bad_medication_request_resource = medication_request_resource[0].copy()
    bad_medication_request_resource.pop("medicationCodeableConcept")

    assert validation([bad_medication_request_resource]) == []
