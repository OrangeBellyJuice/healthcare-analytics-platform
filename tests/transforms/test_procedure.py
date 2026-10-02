from src.transforms.procedure import (
    calculate_duration_minutes,
    transform_procedure,
)

procedure_with_reason_reference = {
    "resourceType": "Procedure",
    "id": "94697183-8162-51cb-f2eb-3fab08e350f7",
    "status": "completed",
    "code": {
        "coding": [
            {
                "system": "http://snomed.info/sct",
                "code": "23426006",
                "display": "Measurement of respiratory function (procedure)",
            }
        ],
        "text": "Measurement of respiratory function (procedure)",
    },
    "subject": {
        "reference": "urn:uuid:94697183-8162-51cb-016a-7aaefbb845ba"
    },
    "encounter": {
        "reference": "urn:uuid:94697183-8162-51cb-10f8-1df2d9f6e882"
    },
    "performedPeriod": {
        "start": "2024-04-01T10:44:44-07:00",
        "end": "2024-04-01T11:03:43-07:00",
    },
    "reasonReference": [
        {
            "reference": "urn:uuid:94697183-8162-51cb-b39b-2b8c6b950f1b",
            "display": "Acute bronchitis (disorder)",
        }
    ],
}


procedure_with_reason_code = {
    "resourceType": "Procedure",
    "id": "94697183-8162-51cb-bb42-2ed86d5b6b30",
    "status": "completed",
    "code": {
        "coding": [
            {
                "system": "http://snomed.info/sct",
                "code": "34043003",
                "display": "Dental consultation and report (procedure)",
            }
        ],
        "text": "Dental consultation and report (procedure)",
    },
    "subject": {
        "reference": "urn:uuid:94697183-8162-51cb-016a-7aaefbb845ba"
    },
    "encounter": {
        "reference": "urn:uuid:94697183-8162-51cb-4c15-6f756591ad97"
    },
    "performedPeriod": {
        "start": "2023-09-06T16:44:44-07:00",
        "end": "2023-09-06T17:04:33-07:00",
    },
    "reasonCode": [
        {
            "coding": [
                {
                    "system": "http://snomed.info/sct",
                    "code": "103697008",
                    "display": "Patient referral for dental care (procedure)",
                }
            ],
            "text": "Patient referral for dental care (procedure)",
        }
    ],
}


def test_calculate_duration_minutes():
    result = calculate_duration_minutes(
        "2024-04-01T10:44:44-07:00",
        "2024-04-01T11:03:43-07:00",
    )

    assert result == 18.98


def test_transform_procedure_with_reason_reference():
    results = transform_procedure(procedure_with_reason_reference)

    assert results["procedure_id"] == (
        "94697183-8162-51cb-f2eb-3fab08e350f7"
    )
    assert results["patient_id"] == (
        "94697183-8162-51cb-016a-7aaefbb845ba"
    )
    assert results["encounter_id"] == (
        "94697183-8162-51cb-10f8-1df2d9f6e882"
    )
    assert results["status"] == "completed"
    assert results["procedure_code"] == "23426006"
    assert results["procedure"] == (
        "Measurement of respiratory function (procedure)"
    )
    assert results["duration_minutes"] == 18.98
    assert results["reason_code"] is None
    assert results["reason_condition_id"] == (
        "94697183-8162-51cb-b39b-2b8c6b950f1b"
    )
    assert results["reason"] == "Acute bronchitis (disorder)"


def test_transform_procedure_with_reason_code():
    results = transform_procedure(procedure_with_reason_code)

    assert results["procedure_code"] == "34043003"
    assert results["reason_code"] == "103697008"
    assert results["reason_condition_id"] is None
    assert results["reason"] == (
        "Patient referral for dental care (procedure)"
    )


def test_transform_procedure_without_reason():
    procedure = procedure_with_reason_reference.copy()
    procedure.pop("reasonReference")

    results = transform_procedure(procedure)

    assert results["reason_code"] is None
    assert results["reason_condition_id"] is None
    assert results["reason"] is None
