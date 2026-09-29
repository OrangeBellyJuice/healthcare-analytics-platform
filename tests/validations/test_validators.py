from src.validations.validators import validate_practitioners, validate_organizations

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


def test_validate_organization_for_success():

    results = validate_organizations(organization_resource)

    assert results[0]["id"] == "231f25bb-2bdc-31e6-b187-3e666cb9f8fa"


def test_validate_practitioner_for_success():

    results = validate_practitioners(practitioner_resource)

    assert results[0]["id"] == "4ac6772e-f4cd-3862-b53c-bb433031afc9"


def test_validate_practitioners_for_failure():

    bad_organization_resource = organization_resource[0]
    del bad_organization_resource["address"]

    results = validate_organizations([bad_organization_resource])

    assert results == []


def test_validate_practitioners_for_failure():

    bad_practitioner_resource = practitioner_resource[0]
    del bad_practitioner_resource["gender"]

    results = validate_practitioners([bad_practitioner_resource])

    assert results == []
