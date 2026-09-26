from src.extraction.read_bronze import extract_practitioner_resources


def test_extract_practitioner_resources_from_bundle():
    fake_bundle = {
        "resourceType": "Bundle",
        "entry": [
            {
                "resource": {
                    "resourceType": "Practitioner",
                    "id": "p1",
                }
            },
            {
                "resource": {
                    "resourceType": "Practitioner",
                    "id": "p2",
                }
            },
        ],
    }

    result = extract_practitioner_resources(fake_bundle)

    assert len(result) == 2
    assert result[0]["id"] == "p1"
    assert result[1]["id"] == "p2"


def test_extract_practitioner_resources_ignores_other_resources():
    fake_bundle = {
        "entry": [
            {
                "resource": {
                    "resourceType": "Practitioner",
                    "id": "p1",
                }
            },
            {
                "resource": {
                    "resourceType": "Patient",
                    "id": "patient1",
                }
            },
        ]
    }

    result = extract_practitioner_resources(fake_bundle)

    assert len(result) == 1


def test_extract_practitioner_resources_empty_bundle():
    fake_bundle = {"entry": []}

    result = extract_practitioner_resources(fake_bundle)

    assert result == []
