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


def extract_component_quantity(
    components: list[dict],
    component_code: str,
) -> tuple[float | None, str | None]:

    for component in components:
        coding = first_coding(component.get("code"))

        if coding.get("code") == component_code:
            quantity = component.get("valueQuantity", {})
            return quantity.get("value"), quantity.get("unit")

    return None, None


def transform_observation(resource: dict) -> dict:

    category = first_coding(resource["category"][0])
    observation = first_coding(resource["code"])

    value_quantity = resource.get("valueQuantity", {})
    coded_value = first_coding(resource.get("valueCodeableConcept"))

    components = resource.get("component", [])

    systolic_value, systolic_unit = extract_component_quantity(
        components,
        "8480-6",
    )
    diastolic_value, diastolic_unit = extract_component_quantity(
        components,
        "8462-4",
    )

    data = {
        "observation_id": resource["id"],
        "patient_id": extract_reference_id(
            resource["subject"]["reference"]
        ),
        "encounter_id": extract_reference_id(
            resource["encounter"]["reference"]
        ),
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
        "value": value_quantity.get("value"),
        "unit": value_quantity.get("unit"),
        "coded_value_code": coded_value.get("code"),
        "coded_value": coded_value.get(
            "display",
            resource.get("valueCodeableConcept", {}).get("text"),
        ),
        "systolic_value": systolic_value,
        "diastolic_value": diastolic_value,
        "blood_pressure_unit": systolic_unit or diastolic_unit,
    }

    return data


def transform_observations(resources: list[dict]) -> list[dict]:

    logger.info(
        f"Starting transformation of {len(resources)} Observation resources"
    )

    results = []

    for resource in resources:
        cleaned_resource = transform_observation(resource)
        results.append(cleaned_resource)

    logger.info(
        f"Observation transformation finished: {len(results)} transformed"
    )

    return results
