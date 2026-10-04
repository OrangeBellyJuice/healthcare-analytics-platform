import logging

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

    return " ".join(part.rstrip("0123456789") for part in name.split())


def first_dosage_instruction(resource: dict) -> dict:
    dosage_instructions = resource.get("dosageInstruction", [])

    if not dosage_instructions:
        return {}

    return dosage_instructions[0]


def transform_medication_request(resource: dict) -> dict:

    medication = first_coding(resource["medicationCodeableConcept"])
    requester = resource["requester"]

    reason_references = resource.get("reasonReference", [])
    reason_reference = reason_references[0] if reason_references else {}

    dosage = first_dosage_instruction(resource)

    timing = dosage.get("timing", {}).get("repeat", {})

    dose_and_rate = dosage.get("doseAndRate", [])
    dose_quantity = dose_and_rate[0].get("doseQuantity", {}) if dose_and_rate else {}

    data = {
        "medication_request_id": resource["id"],
        "patient_id": extract_reference_id(resource["subject"]["reference"]),
        "encounter_id": extract_reference_id(resource["encounter"]["reference"]),
        "status": resource["status"],
        "intent": resource["intent"],
        "medication_code": medication.get("code"),
        "medication": medication.get(
            "display",
            resource["medicationCodeableConcept"].get("text"),
        ),
        "authored_datetime": resource["authoredOn"],
        "practitioner_npi": extract_reference_id(requester.get("reference")),
        "practitioner_name": clean_display_name(requester.get("display")),
        "reason_condition_id": (
            extract_reference_id(reason_reference["reference"])
            if reason_reference.get("reference")
            else None
        ),
        "reason": reason_reference.get("display"),
        "dosage_text": dosage.get("text"),
        "as_needed": dosage.get("asNeededBoolean"),
        "frequency": timing.get("frequency"),
        "period": timing.get("period"),
        "period_unit": timing.get("periodUnit"),
        "dose_value": dose_quantity.get("value"),
    }

    return data


def transform_medication_requests(resources: list[dict]) -> list[dict]:

    logger.info(
        f"Starting transformation of {len(resources)} MedicationRequest resources"
    )

    results = []

    for resource in resources:
        try:
            cleaned_resource = transform_medication_request(resource)
            results.append(cleaned_resource)

        except (KeyError, IndexError, TypeError):
            logger.exception(
                f"Failed to transform MedicationRequest {resource.get('id', 'unknown')}"
            )
            raise

    logger.info(
        f"MedicationRequest transformation finished: {len(results)} transformed"
    )

    return results
