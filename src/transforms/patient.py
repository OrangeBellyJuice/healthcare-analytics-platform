def title_case(address: str) -> str:
    return address.title()


def remove_digits_end(name: str) -> str:
    return name.rstrip("0123456789")


def transform_patient(resource: dict) -> dict:

    last_name = remove_digits_end(resource["name"][0]["family"])
    first_name = remove_digits_end(resource["name"][0]["given"][0])
    prefix = resource["name"][0]["prefix"][0]
    address = resource["address"][0]
    data = {
        "patient_id": resource["id"],
        "last_name": last_name,
        "first_name": first_name,
        "prefix": prefix,
        "full_name": first_name + " " + last_name,
        "full_title": prefix + " " + first_name + " " + last_name,
        "gender": resource["gender"],
        "birth_date": resource["birthDate"],
        "deceased_datetime": resource.get("deceasedDateTime"),
        "is_deceased": bool(resource.get("deceasedDateTime")),
        "address": title_case(address["line"][0]),
        "city": address["city"],
        "province": address["state"],
        "postal_code": address["postalCode"],
        "country": address["country"],
        "marital_status": resource["maritalStatus"]["text"],
        "multiple_birth": resource["multipleBirthBoolean"],
    }

    return data


def transform_patients(resources: list[dict]) -> list[dict]:

    results = []

    for resource in resources:
        cleaned_resource = transform_patient(resource)
        results.append(cleaned_resource)

    return results
