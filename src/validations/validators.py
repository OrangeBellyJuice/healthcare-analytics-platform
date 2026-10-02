import logging

from pydantic import BaseModel, ValidationError

from src.validations.models import Condition, Encounter, MedicalRequest, Observation, Organization, Patient, Practitioner, Procedure

logger = logging.getLogger(__name__)


RESOURCE_MODELS = {
    "Condition": Condition,
    "Encounter": Encounter,
    "MedicalRequest": MedicalRequest,
    "Observation": Observation,
    "Organization": Organization,
    "Patient": Patient,
    "Practitioner": Practitioner,
    "Procedure": Procedure
}


def validate_resource(resource: dict, model: type[BaseModel]) -> dict | None:
    try:
        model.model_validate(resource)
        return resource
    except ValidationError as ve:
        logger.error(
            f"{model.__name__} {resource.get('id', 'unknown')} failed validation: {ve}"
        )
        return None


def validation(resources: list[dict]) -> list[dict]:
    valid = []
    for resource in resources:
        resource_type = resource["resourceType"]
        model = RESOURCE_MODELS[resource_type]
        validated = validate_resource(resource, model)
        if validated is not None:
            valid.append(validated)

    return valid
