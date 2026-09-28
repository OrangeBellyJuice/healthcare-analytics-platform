from src.validations.validators import validate_practitioners

resource = [
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


def test_validate_practitioners_for_success():

    results = validate_practitioners(resource)

    assert results[0]["id"] == "4ac6772e-f4cd-3862-b53c-bb433031afc9"


def test_validate_practitioners_for_failure():

    bad_resource = resource[0]
    del bad_resource["gender"]

    results = validate_practitioners([bad_resource])

    assert results == []
