from src.transforms.observation import (
    extract_component_quantity,
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
    assert results["coded_value"] is None
    assert results["systolic_value"] is None
    assert results["diastolic_value"] is None


def test_transform_coded_observation():
    results = transform_observation(coded_observation)

    assert results["observation_code"] == "72166-2"
    assert results["observation"] == "Tobacco smoking status"
    assert results["value"] is None
    assert results["unit"] is None
    assert results["coded_value_code"] == "266919005"
    assert results["coded_value"] == "Never smoked tobacco (finding)"


def test_extract_blood_pressure_components():
    systolic, systolic_unit = extract_component_quantity(
        blood_pressure_observation["component"],
        "8480-6",
    )
    diastolic, diastolic_unit = extract_component_quantity(
        blood_pressure_observation["component"],
        "8462-4",
    )

    assert systolic == 111
    assert systolic_unit == "mm[Hg]"
    assert diastolic == 68
    assert diastolic_unit == "mm[Hg]"


def test_transform_blood_pressure_observation():
    results = transform_observation(blood_pressure_observation)

    assert results["observation_code"] == "85354-9"
    assert results["systolic_value"] == 111
    assert results["diastolic_value"] == 68
    assert results["blood_pressure_unit"] == "mm[Hg]"
