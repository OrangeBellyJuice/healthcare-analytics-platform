import logging

from pydantic import ValidationError

from src.validations.models import Practitioner


def validate_practitioners(resources: list[dict]) -> list[dict]:
    logger = logging.getLogger(__name__)
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
