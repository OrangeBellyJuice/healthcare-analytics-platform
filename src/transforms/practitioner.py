def title_case(address: str) -> str:
    return address.title()


def remove_digits_end(name: str) -> str:
    return name.rstrip("0123456789")


def transform_practitioner(resource: dict) -> dict:

    last_name = remove_digits_end(resource["name"][0]["family"])
    first_name = remove_digits_end(resource["name"][0]["given"][0])
    prefix = resource["name"][0]["prefix"][0]
    address = title_case(resource["address"][0]["line"][0])
    data = {
        "practitioner_id": resource["id"],
        "last_name": last_name,
        "first_name": first_name,
        "prefix": prefix,
        "full_name": first_name + " " + last_name,
        "full_title": prefix + " " + first_name + " " + last_name,
        "address": address,
        "city": resource["address"][0]["city"],
        "province": resource["address"][0]["state"],
        "postal_code": resource["address"][0]["postalCode"],
        "country": resource["address"][0]["country"],
        "gender": resource["gender"],
    }

    return data


def transform_practitioners(resources: list[dict]) -> list[dict]:

    results = []

    for resource in resources:
        cleaned_resource = transform_practitioner(resource)
        results.append(cleaned_resource)

    return results
