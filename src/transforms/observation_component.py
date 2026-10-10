import logging

from src.transforms.observation import extract_observation_value, first_coding

logger = logging.getLogger(__name__)


def transform_observation_component(
    observation: dict,
    component: dict,
) -> dict:

    component_code = first_coding(component["code"])
    component_value = extract_observation_value(component)

    data = {
        "observation_id": observation["id"],
        "component_code": component_code.get("code"),
        "component": component_code.get(
            "display",
            component["code"].get("text"),
        ),
        "value": component_value["value"],
        "unit": component_value["unit"],
        "value_code": component_value["value_code"],
        "value_text": component_value["value_text"],
        "value_type": component_value["value_type"],
    }

    return data


def transform_observation_components(
    observations: list[dict],
) -> list[dict]:

    results = []

    for observation in observations:
        try:
            components = observation.get("component", [])

            for component in components:
                cleaned_component = transform_observation_component(
                    observation,
                    component,
                )
                results.append(cleaned_component)

        except (KeyError, IndexError, TypeError):
            logger.exception(
                f"Failed to transform Observation components "
                f"{observation.get('id', 'unknown')}"
            )
            raise

    return results
