from src.transforms.medical_request import (
    clean_display_name,
    extract_reference_id,
    transform_medication_request,
)


regular_medication_request = {
    "resourceType": "MedicationRequest",
    "id": "94697183-8162-51cb-8ffd-e654fe53c12c",
    "status": "completed",
    "intent": "order",
    "medicationCodeableConcept": {
        "coding": [
            {
                "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
                "code": "308192",
                "display": "Amoxicillin 500 MG Oral Tablet",
            }
        ],
        "text": "Amoxicillin 500 MG Oral Tablet",
    },
    "subject": {
        "reference": "urn:uuid:94697183-8162-51cb-016a-7aaefbb845ba"
    },
    "encounter": {
        "reference": "urn:uuid:94697183-8162-51cb-fd4f-db0eeae721a6"
    },
    "authoredOn": "2017-09-02T16:44:44-07:00",
    "requester": {
        "reference": (
            "Practitioner?identifier="
            "http://hl7.org/fhir/sid/us-npi|9999997791"
        ),
        "display": "Dr. Marcy588 Hamill307",
    },
    "dosageInstruction": [
        {
            "sequence": 1,
            "text": (
                "Take at regular intervals. Complete the prescribed "
                "course unless otherwise directed (qualifier value)"
            ),
            "timing": {
                "repeat": {
                    "frequency": 3,
                    "period": 1.0,
                    "periodUnit": "d",
                }
            },
            "asNeededBoolean": False,
            "doseAndRate": [
                {
                    "doseQuantity": {
                        "value": 1.0,
                    }
                }
            ],
        }
    ],
}


as_needed_medication_request = {
    "resourceType": "MedicationRequest",
    "id": "94697183-8162-51cb-68fd-ae569aef58d4",
    "status": "completed",
    "intent": "order",
    "medicationCodeableConcept": {
        "coding": [
            {
                "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
                "code": "313820",
                "display": "Acetaminophen 160 MG Chewable Tablet",
            }
        ],
        "text": "Acetaminophen 160 MG Chewable Tablet",
    },
    "subject": {
        "reference": "urn:uuid:94697183-8162-51cb-016a-7aaefbb845ba"
    },
    "encounter": {
        "reference": "urn:uuid:94697183-8162-51cb-fd4f-db0eeae721a6"
    },
    "authoredOn": "2017-09-02T16:44:44-07:00",
    "requester": {
        "reference": (
            "Practitioner?identifier="
            "http://hl7.org/fhir/sid/us-npi|9999997791"
        ),
        "display": "Dr. Marcy588 Hamill307",
    },
    "dosageInstruction": [
        {
            "sequence": 1,
            "text": "Take as needed.",
            "asNeededBoolean": True,
        }
    ],
}


medication_request_with_reason = {
    "resourceType": "MedicationRequest",
    "id": "94697183-8162-51cb-69ff-d1a52e13db0f",
    "status": "completed",
    "intent": "order",
    "medicationCodeableConcept": {
        "coding": [
            {
                "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
                "code": "313782",
                "display": "Acetaminophen 325 MG Oral Tablet",
            }
        ],
        "text": "Acetaminophen 325 MG Oral Tablet",
    },
    "subject": {
        "reference": "urn:uuid:94697183-8162-51cb-016a-7aaefbb845ba"
    },
    "encounter": {
        "reference": "urn:uuid:94697183-8162-51cb-10f8-1df2d9f6e882"
    },
    "authoredOn": "2024-04-01T11:03:43-07:00",
    "requester": {
        "reference": (
            "Practitioner?identifier="
            "http://hl7.org/fhir/sid/us-npi|9999997791"
        ),
        "display": "Dr. Marcy588 Hamill307",
    },
    "reasonReference": [
        {
            "reference": "urn:uuid:94697183-8162-51cb-b39b-2b8c6b950f1b",
            "display": "Acute bronchitis (disorder)",
        }
    ],
}


def test_extract_reference_id_from_practitioner_reference():
    reference = (
        "Practitioner?identifier="
        "http://hl7.org/fhir/sid/us-npi|9999997791"
    )

    assert extract_reference_id(reference) == "9999997791"


def test_clean_display_name():
    assert clean_display_name(
        "Dr. Marcy588 Hamill307"
    ) == "Dr. Marcy Hamill"


def test_transform_regular_medication_request():
    results = transform_medication_request(regular_medication_request)

    assert results["medication_request_id"] == (
        "94697183-8162-51cb-8ffd-e654fe53c12c"
    )
    assert results["patient_id"] == (
        "94697183-8162-51cb-016a-7aaefbb845ba"
    )
    assert results["encounter_id"] == (
        "94697183-8162-51cb-fd4f-db0eeae721a6"
    )
    assert results["status"] == "completed"
    assert results["intent"] == "order"
    assert results["medication_code"] == "308192"
    assert results["medication"] == "Amoxicillin 500 MG Oral Tablet"
    assert results["practitioner_npi"] == "9999997791"
    assert results["practitioner_name"] == "Dr. Marcy Hamill"
    assert results["as_needed"] is False
    assert results["frequency"] == 3
    assert results["period"] == 1.0
    assert results["period_unit"] == "d"
    assert results["dose_value"] == 1.0


def test_transform_as_needed_medication_request():
    results = transform_medication_request(as_needed_medication_request)

    assert results["as_needed"] is True
    assert results["dosage_text"] == "Take as needed."
    assert results["frequency"] is None
    assert results["period"] is None
    assert results["dose_value"] is None


def test_transform_medication_request_with_reason():
    results = transform_medication_request(medication_request_with_reason)

    assert results["reason_condition_id"] == (
        "94697183-8162-51cb-b39b-2b8c6b950f1b"
    )
    assert results["reason"] == "Acute bronchitis (disorder)"
    assert results["dosage_text"] is None
    assert results["as_needed"] is None
