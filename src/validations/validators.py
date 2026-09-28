from pydantic import ValidationError

from src.validations.models import Practitioner


def validate_practitioners(resources: list[dict]) -> list[dict]:
    valid = []
    for resource in resources:
        try:
            Practitioner.model_validate(resource)
            valid.append(resource)
        except ValidationError as ve:
            print(f"{ve}")  # make this a logger error eventually

    return valid
