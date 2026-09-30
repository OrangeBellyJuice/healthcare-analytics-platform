from src.validations.models import Organization, Patient, Practitioner
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


def test_validate_resource_for_success():

    result = validate_resource(organization_resource[0], Organization)
    assert result["resourceType"] == "Organization"

    result = validate_resource(practitioner_resource[0], Practitioner)
    assert result["resourceType"] == "Practitioner"

    result = validate_resource(patient_resource[0], Patient)
    assert result["resourceType"] == "Patient"


def test_validation_for_failure():

    bad_organization_resource = organization_resource[0]
    del bad_organization_resource["address"]

    results = validation([bad_organization_resource])
    assert results == []

    bad_practitioner_resource = practitioner_resource[0]
    del bad_practitioner_resource["gender"]

    results = validation([bad_practitioner_resource])
    assert results == []

    bad_patient_resource = patient_resource[0]
    del bad_patient_resource["gender"]

    results = validation([bad_patient_resource])
    assert results == []
