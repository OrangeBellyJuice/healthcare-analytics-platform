from src.transforms.organization import (
    title_case,
    transform_organization,
)

fake_resource = {
    "resourceType": "Organization",
    "id": "231f25bb-2bdc-31e6-b187-3e666cb9f8fa",
    "name": "Primecare Medical Centre",
    "address": [
        {
            "line": ["201-7315 edmonds street"],
            "city": "Burnaby",
            "state": "BC",
            "postalCode": "V3N 1A7",
            "country": "CA",
        }
    ],
}


def test_title_case_for_address_string():

    raw_addresses = ["546 line rd", "6545 Whey Court", "786 brich street"]

    assert title_case(raw_addresses[0]) == "546 Line Rd"
    assert title_case(raw_addresses[1]) == "6545 Whey Court"
    assert title_case(raw_addresses[2]) == "786 Brich Street"


def test_transform_organization_basic_fields():

    results = transform_organization(fake_resource)

    assert results["organization_id"] == "231f25bb-2bdc-31e6-b187-3e666cb9f8fa"
    assert results["organization_name"] == "Primecare Medical Centre"
    assert results["address"] == "201-7315 Edmonds Street"
    assert results["city"] == "Burnaby"
    assert results["province"] == "BC"
    assert results["postal_code"] == "V3N 1A7"
    assert results["country"] == "CA"
