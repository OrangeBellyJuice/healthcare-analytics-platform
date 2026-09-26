from src.transform.practitioner import (
    remove_digits_end,
    title_case,
    transform_practitioner,
)

fake_resource = {
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


def test_remove_digits_from_end_of_string():

    raw_names = ["Alice768", "Bob456", "David123"]

    assert remove_digits_end(raw_names[0]) == "Alice"
    assert remove_digits_end(raw_names[1]) == "Bob"
    assert remove_digits_end(raw_names[2]) == "David"


def test_title_case_for_address_string():

    raw_addresses = ["546 line rd", "6545 whey court", "786 brich street"]

    assert title_case(raw_addresses[0]) == "546 Line Rd"
    assert title_case(raw_addresses[1]) == "6545 Whey Court"
    assert title_case(raw_addresses[2]) == "786 Brich Street"


def test_transform_practitioner_basic_fields():

    results = transform_practitioner(fake_resource)

    assert results["practitioner_id"] == "4ac6772e-f4cd-3862-b53c-bb433031afc9"
    assert results["last_name"] == "Schumm"
    assert results["first_name"] == "Hilari"
    assert results["prefix"] == "Dr."
    assert results["full_name"] == "Hilari Schumm"
    assert results["full_title"] == "Dr. Hilari Schumm"
    assert results["address"] == "201-7315 Edmonds Street"
    assert results["city"] == "Burnaby"
    assert results["province"] == "BC"
    assert results["postal_code"] == "V3N 1A7"
    assert results["country"] == "CA"
    assert results["gender"] == "male"
