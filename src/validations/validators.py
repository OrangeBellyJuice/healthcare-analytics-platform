import logging

from pydantic import ValidationError

from src.validations.models import Practitioner, Organization


def validate_organizations(resources: list[dict]) -> list[dict]:
    logger = logging.getLogger(__name__)
    valid = []
    for resource in resources:
        try:
            Organization.model_validate(resource)
            valid.append(resource)
        except ValidationError as ve:
            logger.error(
                f"Organization {resource.get('id', 'unknown')} failed validation: {ve}"
            )

    return valid


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
