def title_case(address: str) -> str:
    return address.title()


def transform_organization(resource: dict) -> dict:

    address = title_case(resource["address"][0]["line"][0])
    data = {
        "organization_id": resource["id"],
        "organization_name": resource["name"],
        "address": address,
        "city": resource["address"][0]["city"],
        "province": resource["address"][0]["state"],
        "postal_code": resource["address"][0]["postalCode"],
        "country": resource["address"][0]["country"],
    }

    return data


def transform_organizations(resources: list[dict]) -> list[dict]:

    results = []

    for resource in resources:
        cleaned_resource = transform_organization(resource)
        results.append(cleaned_resource)

    return results
