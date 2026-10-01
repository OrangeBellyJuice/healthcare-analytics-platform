from datetime import datetime


def extract_reference_id(reference: str) -> str:
    return reference.removeprefix("urn:uuid:")


def first_coding(codeable_concept: dict | None) -> dict:
    if not codeable_concept:
        return {}

    coding = codeable_concept.get("coding", [])

    if not coding:
        return {}

    return coding[0]


def calculate_duration_minutes(start: str, end: str) -> float:
    start_datetime = datetime.fromisoformat(start)
    end_datetime = datetime.fromisoformat(end)

    duration = end_datetime - start_datetime

    return round(duration.total_seconds() / 60, 2)


def transform_procedure(resource: dict) -> dict:

    procedure = first_coding(resource["code"])
    period = resource["performedPeriod"]

    reason_codes = resource.get("reasonCode", [])
    reason_code = first_coding(reason_codes[0]) if reason_codes else {}

    reason_references = resource.get("reasonReference", [])
    reason_reference = reason_references[0] if reason_references else {}

    data = {
        "procedure_id": resource["id"],
        "patient_id": extract_reference_id(
            resource["subject"]["reference"]
        ),
        "encounter_id": extract_reference_id(
            resource["encounter"]["reference"]
        ),
        "status": resource["status"],
        "procedure_code": procedure.get("code"),
        "procedure": procedure.get(
            "display",
            resource["code"].get("text"),
        ),
        "start_datetime": period["start"],
        "end_datetime": period["end"],
        "duration_minutes": calculate_duration_minutes(
            period["start"],
            period["end"],
        ),
        "reason_code": reason_code.get("code"),
        "reason_condition_id": (
            extract_reference_id(reason_reference["reference"])
            if reason_reference.get("reference")
            else None
        ),
        "reason": (
            reason_reference.get("display")
            or reason_code.get("display")
        ),
    }

    return data


def transform_procedures(resources: list[dict]) -> list[dict]:

    results = []

    for resource in resources:
        cleaned_resource = transform_procedure(resource)
        results.append(cleaned_resource)

    return results
