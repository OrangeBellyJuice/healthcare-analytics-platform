import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def extract_reference_id(reference: str | None) -> str | None:
    if reference is None:
        return None

    if "|" in reference:
        return reference.rsplit("|", 1)[-1]

    return reference.removeprefix("urn:uuid:")


def first_coding(codeable_concept: dict | None) -> dict:
    if not codeable_concept:
        return {}

    coding = codeable_concept.get("coding", [])

    if not coding:
        return {}

    return coding[0]


def clean_display_name(name: str | None) -> str | None:
    if name is None:
        return None

    return " ".join(
        part.rstrip("0123456789")
        for part in name.split()
    )


def calculate_duration_minutes(start: str, end: str) -> float:
    start_datetime = datetime.fromisoformat(start)
    end_datetime = datetime.fromisoformat(end)

    duration = end_datetime - start_datetime

    return round(duration.total_seconds() / 60, 2)


def transform_encounter(resource: dict) -> dict:

    encounter_type = first_coding(resource["type"][0])

    participant = resource["participant"][0]
    practitioner = participant["individual"]

    period = resource["period"]

    service_provider = resource["serviceProvider"]

    reason_codes = resource.get("reasonCode", [])
    reason = first_coding(reason_codes[0]) if reason_codes else {}

    data = {
        "encounter_id": resource["id"],
        "patient_id": extract_reference_id(
            resource["subject"]["reference"]
        ),
        "status": resource["status"],
        "encounter_class": resource["class"]["code"],
        "encounter_type_code": encounter_type.get("code"),
        "encounter_type": encounter_type.get("display"),
        "start_datetime": period["start"],
        "end_datetime": period["end"],
        "duration_minutes": calculate_duration_minutes(
            period["start"],
            period["end"],
        ),
        "practitioner_npi": extract_reference_id(
            practitioner.get("reference")
        ),
        "practitioner_name": clean_display_name(
            practitioner.get("display")
        ),
        "organization_id": extract_reference_id(
            service_provider.get("reference")
        ),
        "organization_name": service_provider.get("display"),
        "reason_code": reason.get("code"),
        "reason": reason.get("display"),
    }

    return data


def transform_encounters(resources: list[dict]) -> list[dict]:

    logger.info(
        f"Starting transformation of {len(resources)} Encounter resources"
    )

    results = []

    for resource in resources:
        cleaned_resource = transform_encounter(resource)
        results.append(cleaned_resource)

    logger.info(
        f"Encounter transformation finished: {len(results)} transformed"
    )

    return results
