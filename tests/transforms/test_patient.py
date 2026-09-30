from src.transforms.patient import (
    remove_digits_end,
    transform_patient,
)

fake_resource = {
    "resourceType": "Patient",
    "id": "c2aadfa1-256b-c450-bcd5-442316fa4fe9",
    "name": [
        {
            "use": "official",
            "family": "DuBuque211",
            "given": ["Aaron697"],
            "prefix": ["Mr."],
        }
    ],
    "gender": "male",
    "birthDate": "1951-04-21",
    "deceasedDateTime": "2007-05-20T04:55:27-07:00",
    "address": [
        {
            "line": ["818 rodriguez junction unit 57"],
            "city": "Sidney",
            "state": "BC",
            "postalCode": "V8L",
            "country": "CA",
        }
    ],
    "maritalStatus": {
        "text": "Married",
    },
    "multipleBirthBoolean": False,
}


def test_remove_digits_end_for_patient_names():

    assert remove_digits_end("Aaron697") == "Aaron"
    assert remove_digits_end("DuBuque211") == "DuBuque"


def test_transform_patient_basic_fields():

    results = transform_patient(fake_resource)

    assert results["patient_id"] == "c2aadfa1-256b-c450-bcd5-442316fa4fe9"
    assert results["last_name"] == "DuBuque"
    assert results["first_name"] == "Aaron"
    assert results["prefix"] == "Mr."
    assert results["full_name"] == "Aaron DuBuque"
    assert results["full_title"] == "Mr. Aaron DuBuque"
    assert results["gender"] == "male"
    assert results["birth_date"] == "1951-04-21"
    assert results["deceased_datetime"] == "2007-05-20T04:55:27-07:00"
    assert results["is_deceased"] is True
    assert results["address"] == "818 Rodriguez Junction Unit 57"
    assert results["city"] == "Sidney"
    assert results["province"] == "BC"
    assert results["postal_code"] == "V8L"
    assert results["country"] == "CA"
    assert results["marital_status"] == "Married"


def test_transform_patient_without_deceased_datetime():

    living_patient = fake_resource.copy()
    living_patient.pop("deceasedDateTime")

    results = transform_patient(living_patient)

    assert results["deceased_datetime"] is None
    assert results["is_deceased"] is False
    assert results["multiple_birth"] is False
