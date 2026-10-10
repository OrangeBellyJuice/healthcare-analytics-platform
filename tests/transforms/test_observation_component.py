from src.transforms.observation_component import (
    transform_observation_component,
    transform_observation_components,
)

blood_pressure_observation = {
    "resourceType": "Observation",
    "id": "94697183-8162-51cb-1249-ce8a923a40f1",
    "status": "final",
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


coded_component_observation = {
    "resourceType": "Observation",
    "id": "survey-observation-1",
    "status": "final",
    "component": [
        {
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "67875-5",
                        "display": "Employment status - current",
                    }
                ]
            },
            "valueCodeableConcept": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "LA17956-6",
                        "display": "Unemployed",
                    }
                ],
                "text": "Unemployed",
            },
        }
    ],
}


string_component_observation = {
    "resourceType": "Observation",
    "id": "survey-observation-2",
    "status": "final",
    "component": [
        {
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "56799-0",
                        "display": "Address",
                    }
                ]
            },
            "valueString": "851 Barton Ferry",
        }
    ],
}


def test_transform_quantity_observation_component():
    component = blood_pressure_observation["component"][0]

    result = transform_observation_component(
        blood_pressure_observation,
        component,
    )

    assert result["observation_id"] == ("94697183-8162-51cb-1249-ce8a923a40f1")
    assert result["component_code"] == "8462-4"
    assert result["component"] == "Diastolic Blood Pressure"
    assert result["value"] == 68
    assert result["unit"] == "mm[Hg]"
    assert result["value_code"] is None
    assert result["value_text"] is None
    assert result["value_type"] == "quantity"


def test_transform_coded_observation_component():
    component = coded_component_observation["component"][0]

    result = transform_observation_component(
        coded_component_observation,
        component,
    )

    assert result["observation_id"] == "survey-observation-1"
    assert result["component_code"] == "67875-5"
    assert result["component"] == "Employment status - current"
    assert result["value"] is None
    assert result["unit"] is None
    assert result["value_code"] == "LA17956-6"
    assert result["value_text"] == "Unemployed"
    assert result["value_type"] == "codeable_concept"


def test_transform_string_observation_component():
    component = string_component_observation["component"][0]

    result = transform_observation_component(
        string_component_observation,
        component,
    )

    assert result["observation_id"] == "survey-observation-2"
    assert result["component_code"] == "56799-0"
    assert result["component"] == "Address"
    assert result["value"] is None
    assert result["unit"] is None
    assert result["value_code"] is None
    assert result["value_text"] == "851 Barton Ferry"
    assert result["value_type"] == "string"


def test_transform_multiple_observation_components():
    results = transform_observation_components([blood_pressure_observation])

    assert len(results) == 2

    assert results[0]["component_code"] == "8462-4"
    assert results[0]["value"] == 68
    assert results[0]["unit"] == "mm[Hg]"

    assert results[1]["component_code"] == "8480-6"
    assert results[1]["value"] == 111
    assert results[1]["unit"] == "mm[Hg]"


def test_observation_without_components_returns_empty_list():
    observation = {
        "resourceType": "Observation",
        "id": "observation-without-components",
        "status": "final",
    }

    results = transform_observation_components([observation])

    assert results == []
