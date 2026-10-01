from src.transforms.encounter import (
    calculate_duration_minutes,
    clean_display_name,
    extract_reference_id,
    transform_encounter,
)


fake_resource = {
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


def test_extract_reference_id_from_uuid():
    reference = (
        "urn:uuid:c2aadfa1-256b-c450-bcd5-442316fa4fe9"
    )

    assert extract_reference_id(reference) == (
        "c2aadfa1-256b-c450-bcd5-442316fa4fe9"
    )


def test_extract_reference_id_from_identifier():
    reference = (
        "Practitioner?identifier="
        "http://hl7.org/fhir/sid/us-npi|9999976399"
    )

    assert extract_reference_id(reference) == "9999976399"


def test_clean_display_name():
    assert clean_display_name(
        "Dr. Arlene209 Olson653"
    ) == "Dr. Arlene Olson"


def test_calculate_duration_minutes():
    result = calculate_duration_minutes(
        "1997-11-16T08:55:27-08:00",
        "1997-11-16T09:10:27-08:00",
    )

    assert result == 15.0


def test_transform_encounter_basic_fields():
    results = transform_encounter(fake_resource)

    assert results["encounter_id"] == (
        "c2aadfa1-256b-c450-48e9-0a5e44171a14"
    )
    assert results["patient_id"] == (
        "c2aadfa1-256b-c450-bcd5-442316fa4fe9"
    )
    assert results["status"] == "finished"
    assert results["encounter_class"] == "AMB"
    assert results["encounter_type_code"] == "185345009"
    assert results["encounter_type"] == (
        "Encounter for symptom (procedure)"
    )
    assert results["start_datetime"] == (
        "1997-11-16T08:55:27-08:00"
    )
    assert results["end_datetime"] == (
        "1997-11-16T09:10:27-08:00"
    )
    assert results["duration_minutes"] == 15.0
    assert results["practitioner_npi"] == "9999976399"
    assert results["practitioner_name"] == "Dr. Arlene Olson"
    assert results["organization_id"] == (
        "0e58807a-a5f2-3e7d-a9d6-eca59bc3df95"
    )
    assert results["organization_name"] == "Shoreline Medical"
    assert results["reason_code"] == "444814009"
    assert results["reason"] == "Viral sinusitis (disorder)"


def test_transform_encounter_without_reason_code():
    encounter = fake_resource.copy()
    encounter.pop("reasonCode")

    results = transform_encounter(encounter)

    assert results["reason_code"] is None
    assert results["reason"] is None
