import logging

from pydantic import BaseModel, ValidationError

from src.validations.models import Organization, Practitioner

logger = logging.getLogger(__name__)


def validate_practitioners(resources: list[dict]) -> list[dict]:
    # logger = logging.getLogger(__name__)
    valid = []
    for resource in resources:
        try:
            Practitioner.model_validate(resource)
            valid.append(resource)
        except ValidationError as ve:
            logger.error(
                f"Practitioner {resource.get('id', 'unknown')} failed validation: {ve}"
            )

    return valid


RESOURCE_MODELS = {
    "Practitioner": Practitioner,
    "Organization": Organization,
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
