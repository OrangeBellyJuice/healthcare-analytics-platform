import logging

logger = logging.getLogger(__name__)


def extract_reference_id(reference: str) -> str:
    return reference.removeprefix("urn:uuid:")


def first_coding(codeable_concept: dict) -> dict:
    return codeable_concept["coding"][0]


def transform_condition(resource: dict) -> dict:

    clinical_status = first_coding(resource["clinicalStatus"])
    verification_status = first_coding(resource["verificationStatus"])
    condition = first_coding(resource["code"])

    data = {
        "condition_id": resource["id"],
        "patient_id": extract_reference_id(resource["subject"]["reference"]),
        "encounter_id": extract_reference_id(resource["encounter"]["reference"]),
        "clinical_status": clinical_status["code"],
        "verification_status": verification_status["code"],
        "condition_code": condition["code"],
        "condition": condition.get(
            "display",
            resource["code"].get("text"),
        ),
        "onset_datetime": resource["onsetDateTime"],
        "abatement_datetime": resource.get("abatementDateTime"),
        "recorded_datetime": resource["recordedDate"],
    }

    return data


def transform_conditions(resources: list[dict]) -> list[dict]:

    logger.info(f"Starting transformation of {len(resources)} Condtion resources")

    results = []

    for resource in resources:
        try:
            cleaned_resource = transform_condition(resource)
            results.append(cleaned_resource)

        except (KeyError, IndexError, TypeError):
            logger.exception(
                f"Failed to transform Condtion {resource.get('id', 'unknown')}"
            )
            raise

    logger.info(f"Condtion transformation finished: {len(results)} transformed")

    return results
