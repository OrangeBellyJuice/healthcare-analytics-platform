from src.transforms.condition import transform_condition


fake_resource = {
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


def test_transform_condition_basic_fields():
    results = transform_condition(fake_resource)

    assert results["condition_id"] == (
        "c2aadfa1-256b-c450-e2a4-42a0880217f0"
    )
    assert results["patient_id"] == (
        "c2aadfa1-256b-c450-bcd5-442316fa4fe9"
    )
    assert results["encounter_id"] == (
        "c2aadfa1-256b-c450-8612-54e6414afc28"
    )
    assert results["clinical_status"] == "resolved"
    assert results["verification_status"] == "confirmed"
    assert results["condition_code"] == "109838007"
    assert results["condition"] == (
        "Overlapping malignant neoplasm of colon (disorder)"
    )
    assert results["onset_datetime"] == (
        "2002-06-18T00:15:36-07:00"
    )
    assert results["abatement_datetime"] == (
        "2004-10-23T21:02:28-07:00"
    )
    assert results["recorded_datetime"] == (
        "2002-06-18T00:15:36-07:00"
    )


def test_transform_active_condition_without_abatement_datetime():
    condition = fake_resource.copy()
    condition["clinicalStatus"] = {
        "coding": [
            {
                "code": "active",
            }
        ]
    }
    condition.pop("abatementDateTime")

    results = transform_condition(condition)

    assert results["clinical_status"] == "active"
    assert results["abatement_datetime"] is None
