from src.transforms.observation import (
    extract_observation_value,
    extract_reference_id,
    transform_observation,
)

quantity_observation = {
    "resourceType": "Observation",
    "id": "94697183-8162-51cb-d85c-1177d6dd5301",
    "status": "final",
    "category": [
        {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                    "code": "vital-signs",
                    "display": "Vital signs",
                }
            ]
        }
    ],
    "code": {
        "coding": [
            {
                "system": "http://loinc.org",
                "code": "8302-2",
                "display": "Body Height",
            }
        ],
        "text": "Body Height",
    },
    "subject": {"reference": "urn:uuid:94697183-8162-51cb-016a-7aaefbb845ba"},
    "encounter": {"reference": "urn:uuid:94697183-8162-51cb-d5a1-40d07064b4e1"},
    "effectiveDateTime": "2016-10-12T16:44:44-07:00",
    "issued": "2016-10-12T16:44:44.253-07:00",
    "valueQuantity": {
        "value": 56.6,
        "unit": "cm",
        "system": "http://unitsofmeasure.org",
        "code": "cm",
    },
}


coded_observation = {
    "resourceType": "Observation",
    "id": "94697183-8162-51cb-2b7c-2d93157ba875",
    "status": "final",
    "category": [
        {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                    "code": "social-history",
                    "display": "Social history",
                }
            ]
        }
    ],
    "code": {
        "coding": [
            {
                "system": "http://loinc.org",
                "code": "72166-2",
                "display": "Tobacco smoking status",
            }
        ],
        "text": "Tobacco smoking status",
    },
    "subject": {"reference": "urn:uuid:94697183-8162-51cb-016a-7aaefbb845ba"},
    "encounter": {"reference": "urn:uuid:94697183-8162-51cb-d5a1-40d07064b4e1"},
    "effectiveDateTime": "2016-10-12T16:44:44-07:00",
    "issued": "2016-10-12T16:44:44.253-07:00",
    "valueCodeableConcept": {
        "coding": [
            {
                "system": "http://snomed.info/sct",
                "code": "266919005",
                "display": "Never smoked tobacco (finding)",
            }
        ],
        "text": "Never smoked tobacco (finding)",
    },
}


blood_pressure_observation = {
    "resourceType": "Observation",
    "id": "94697183-8162-51cb-1249-ce8a923a40f1",
    "status": "final",
    "category": [
        {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                    "code": "vital-signs",
                    "display": "Vital signs",
                }
            ]
        }
    ],
    "code": {
        "coding": [
            {
                "system": "http://loinc.org",
                "code": "85354-9",
                "display": "Blood pressure panel with all children optional",
            }
        ],
        "text": "Blood pressure panel with all children optional",
    },
    "subject": {"reference": "urn:uuid:94697183-8162-51cb-016a-7aaefbb845ba"},
    "encounter": {"reference": "urn:uuid:94697183-8162-51cb-d5a1-40d07064b4e1"},
    "effectiveDateTime": "2016-10-12T16:44:44-07:00",
    "issued": "2016-10-12T16:44:44.253-07:00",
    "component": [
        {
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "8462-4",
                        "display": "Diastolic Blood Pressure",
                    }
                ]
            },
            "valueQuantity": {
                "value": 68,
                "unit": "mm[Hg]",
                "system": "http://unitsofmeasure.org",
                "code": "mm[Hg]",
            },
        },
        {
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "8480-6",
                        "display": "Systolic Blood Pressure",
                    }
                ]
            },
            "valueQuantity": {
                "value": 111,
                "unit": "mm[Hg]",
                "system": "http://unitsofmeasure.org",
                "code": "mm[Hg]",
            },
        },
    ],
}


def test_extract_reference_id():
    reference = "urn:uuid:94697183-8162-51cb-016a-7aaefbb845ba"

    assert extract_reference_id(reference) == ("94697183-8162-51cb-016a-7aaefbb845ba")


def test_extract_quantity_value():
    result = extract_observation_value(quantity_observation)

    assert result["value"] == 56.6
    assert result["unit"] == "cm"
    assert result["value_code"] is None
    assert result["value_text"] is None
    assert result["value_type"] == "quantity"


def test_transform_quantity_observation():
    results = transform_observation(quantity_observation)

    assert results["observation_id"] == ("94697183-8162-51cb-d85c-1177d6dd5301")
    assert results["patient_id"] == ("94697183-8162-51cb-016a-7aaefbb845ba")
    assert results["encounter_id"] == ("94697183-8162-51cb-d5a1-40d07064b4e1")
    assert results["status"] == "final"
    assert results["category_code"] == "vital-signs"
    assert results["category"] == "Vital signs"
    assert results["observation_code"] == "8302-2"
    assert results["observation"] == "Body Height"
    assert results["value"] == 56.6
    assert results["unit"] == "cm"
    assert results["value_code"] is None
    assert results["value_text"] is None
    assert results["value_type"] == "quantity"


def test_extract_coded_value():
    result = extract_observation_value(coded_observation)

    assert result["value"] is None
    assert result["unit"] is None
    assert result["value_code"] == "266919005"
    assert result["value_text"] == "Never smoked tobacco (finding)"
    assert result["value_type"] == "codeable_concept"


def test_transform_coded_observation():
    results = transform_observation(coded_observation)

    assert results["observation_code"] == "72166-2"
    assert results["observation"] == "Tobacco smoking status"
    assert results["value"] is None
    assert results["unit"] is None
    assert results["value_code"] == "266919005"
    assert results["value_text"] == "Never smoked tobacco (finding)"
    assert results["value_type"] == "codeable_concept"


def test_transform_component_only_observation():
    results = transform_observation(blood_pressure_observation)

    assert results["observation_code"] == "85354-9"
    assert results["observation"] == ("Blood pressure panel with all children optional")

    assert results["value"] is None
    assert results["unit"] is None
    assert results["value_code"] is None
    assert results["value_text"] is None
    assert results["value_type"] is None
