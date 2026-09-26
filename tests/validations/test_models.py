import pytest
from pydantic import ValidationError

from src.validations.models import Practitioner


valid_practitioner = {
    "resourceType": "Practitioner",
    "id": "4ac6772e-f4cd-3862-b53c-bb433031afc9",
    "name": [
        {
            "family": "Schumm995",
            "given": ["Hilari0934"],
            "prefix": ["Dr."],
        }
    ],
    "address": [
        {
            "line": ["201-7315 edmonds street"],
            "city": "Burnaby",
            "state": "BC",
            "postalCode": "V3N 1A7",
            "country": "CA",
        }
    ],
    "gender": "male",
}


def test_valid_practitioner_passes_validation():
    result = Practitioner.model_validate(valid_practitioner)

    assert result.id == "4ac6772e-f4cd-3862-b53c-bb433031afc9"
    assert result.resourceType == "Practitioner"
    assert result.name[0].family == "Schumm995"
    assert result.address[0].state == "BC"


def test_practitioner_missing_name_fails_validation():
    invalid_practitioner = valid_practitioner.copy()
    invalid_practitioner.pop("name")

    with pytest.raises(ValidationError):
        Practitioner.model_validate(invalid_practitioner)
