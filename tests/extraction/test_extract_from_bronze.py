from src.extraction.extract_from_bronze import (
    extract_patient_blob_names,
    extract_resources,
)


class FakeClientContainer:
    def __init__(self):
        self.uploads = []

    def upload_blob(self, blob_name):
        self.uploads.append(blob_name)

    def list_blob_names(self, name_starts_with: None):
        return self.uploads


def test_extract_patient_blob_names_ignore_hospital_and_practitioner():
    fake_container_client = FakeClientContainer()

    fake_container_client.upload_blob("bronze/hospitalInformation4636332.json")
    fake_container_client.upload_blob("bronze/practitionerInformation59352234.json")

    results = extract_patient_blob_names(fake_container_client)

    assert results == []


def test_extract_patient_blob_names_only_practitioner():
    fake_container_client = FakeClientContainer()

    fake_container_client.upload_blob(
        "bronze/Brandon345_Hay545_1325323_2322f32f_23f23f2f.json"
    )

    results = extract_patient_blob_names(fake_container_client)

    assert results == ["bronze/Brandon345_Hay545_1325323_2322f32f_23f23f2f.json"]


def test_extract_hospital_resources_from_bundle():
    fake_bundle = {
        "resourceType": "Bundle",
        "entry": [
            {
                "resource": {
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
                },
            }
        ],
    }

    result = extract_resources(fake_bundle, "Organization")

    assert len(result) == 1
    assert result[0]["resourceType"] == "Organization"
    assert result[0]["name"] == "Primecare Medical Centre"
    assert len(result[0]["address"]) == 1


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

    result = extract_resources(fake_bundle, "Practitioner")

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

    result = extract_resources(fake_bundle, "Practitioner")

    assert len(result) == 1


def test_extract_practitioner_resources_empty_bundle():
    fake_bundle = {"entry": []}

    result_practitioner = extract_resources(fake_bundle, "Practitioner")
    result_organization = extract_resources(fake_bundle, "Organization")

    assert result_practitioner == []
    assert result_organization == []
