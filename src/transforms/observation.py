import logging

logger = logging.getLogger(__name__)


def extract_reference_id(reference: str) -> str:
    return reference.removeprefix("urn:uuid:")


def first_coding(codeable_concept: dict | None) -> dict:
    if not codeable_concept:
        return {}

    coding = codeable_concept.get("coding", [])

    if not coding:
        return {}

    return coding[0]


def extract_observation_value(resource: dict) -> dict:

    value_quantity = resource.get("valueQuantity")

    if value_quantity:
        return {
            "value": value_quantity.get("value"),
            "unit": value_quantity.get("unit"),
            "value_code": None,
            "value_text": None,
            "value_type": "quantity",
        }

    value_codeable_concept = resource.get("valueCodeableConcept")

    if value_codeable_concept:
        coding = first_coding(value_codeable_concept)

        return {
            "value": None,
            "unit": None,
            "value_code": coding.get("code"),
            "value_text": coding.get(
                "display",
                value_codeable_concept.get("text"),
            ),
            "value_type": "codeable_concept",
        }

    value_string = resource.get("valueString")

    if value_string:
        return {
            "value": None,
            "unit": None,
            "value_code": None,
            "value_text": value_string,
            "value_type": "string",
        }

    return {
        "value": None,
        "unit": None,
        "value_code": None,
        "value_text": None,
        "value_type": None,
    }


def transform_observation(resource: dict) -> dict:

    category = first_coding(resource["category"][0])
    observation = first_coding(resource["code"])
    observation_value = extract_observation_value(resource)

    data = {
        "observation_id": resource["id"],
        "patient_id": extract_reference_id(resource["subject"]["reference"]),
        "encounter_id": extract_reference_id(resource["encounter"]["reference"]),
        "status": resource["status"],
        "category_code": category.get("code"),
        "category": category.get("display"),
        "observation_code": observation.get("code"),
        "observation": observation.get(
            "display",
            resource["code"].get("text"),
        ),
        "effective_datetime": resource["effectiveDateTime"],
        "issued_datetime": resource["issued"],
        "value": observation_value["value"],
        "unit": observation_value["unit"],
        "value_code": observation_value["value_code"],
        "value_text": observation_value["value_text"],
        "value_type": observation_value["value_type"],
    }

    return data


def transform_observations(resources: list[dict]) -> list[dict]:

    results = []

    for resource in resources:
        try:
            cleaned_resource = transform_observation(resource)
            results.append(cleaned_resource)

        except (KeyError, IndexError, TypeError):
            logger.exception(
                f"Failed to transform Observation {resource.get('id', 'unknown')}"
            )
            raise

    return results
