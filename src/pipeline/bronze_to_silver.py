import logging
from collections.abc import Callable

from azure.core.exceptions import AzureError
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, ContainerClient

from src.config.logging_config import setup_logging
from src.extraction.extract_from_bronze import (
    extract_bundle,
    extract_patient_blob_names,
    extract_resources,
)
from src.loading.load_to_silver import load_to_silver

# from src.transforms.observation import transform_observations
from src.transforms.condition import transform_conditions
from src.transforms.encounter import transform_encounters
from src.transforms.medication_request import transform_medication_requests
from src.transforms.organization import transform_organizations
from src.transforms.patient import transform_patients
from src.transforms.practitioner import transform_practitioners
from src.transforms.procedure import transform_procedures
from src.validations.validators import validation

logger = logging.getLogger(__name__)

BATCH_SIZE = 500


def process_organizations(container_client: ContainerClient, organization_blob: str):
    organization_bundle = extract_bundle(container_client, organization_blob)
    raw_organizations = extract_resources(organization_bundle, "Organization")
    valid_organizations = validation(raw_organizations)
    clean_organizations = transform_organizations(valid_organizations)
    return clean_organizations


def process_practitioners(container_client: ContainerClient, practitioner_blob: str):
    practitioner_bundle = extract_bundle(container_client, practitioner_blob)
    raw_practitioners = extract_resources(practitioner_bundle, "Practitioner")
    valid_practitioners = validation(raw_practitioners)
    clean_practitioners = transform_practitioners(valid_practitioners)
    return clean_practitioners


def process_resources(
    bundle: dict, resource_type: str, transform_func: Callable[[list[dict]], list[dict]]
) -> tuple[list[dict], int, int]:
    resources = extract_resources(bundle, resource_type)
    valid_resources = validation(resources)

    valid_count = len(valid_resources)
    failed_count = len(resources) - valid_count

    cleaned_resources = transform_func(valid_resources)

    return cleaned_resources, valid_count, failed_count


def log_and_load_batch(
    blob_service_client,
    container_name: str,
    resource_name: str,
    silver_folder: str,
    records: list[dict],
    passed: int,
    failed: int,
    batch_number: int,
) -> None:
    logger.info(f"{resource_name} validation: {passed} passed, {failed} failed")

    logger.info(f"{resource_name} transformation: {len(records)} transformed")

    load_to_silver(
        blob_service_client,
        container_name,
        f"silver/{silver_folder}/part-{batch_number:04d}.parquet",
        records,
    )

    logger.info(f"Loaded {len(records)} {resource_name} records")


def main():
    """
    NEED TO LOOK INTO OBSERVATION MORE
    """
    setup_logging("bronze_to_silver.log")
    account_url = "https://syntheagendata.blob.core.windows.net"
    container_name = "lake"

    credential = DefaultAzureCredential()
    blob_service_client = BlobServiceClient(account_url, credential=credential)

    try:
        container_client = blob_service_client.get_container_client(
            container=container_name
        )
        all_patient_blob_names = extract_patient_blob_names(container_client)
    except AzureError:
        logger.exception("Failed to retrieve patient blobs from Bronze")
        raise

    logger.info(f"Found {len(all_patient_blob_names)} patient bundles in Bronze")

    organization_blob = "bronze/hospitalInformation1790018762251.json"
    practitioner_blob = "bronze/practitionerInformation1790018762251.json"

    logger.info("Bronze to Silver ETL Started")

    # process organizations - 1 file
    load_to_silver(
        blob_service_client,
        container_name,
        "silver/organizations.parquet",
        process_organizations(container_client, organization_blob),
    )

    # process_practitioners - 1 file
    load_to_silver(
        blob_service_client,
        container_name,
        "silver/practitioners.parquet",
        process_practitioners(container_client, practitioner_blob),
    )

    for batch_number, start in enumerate(
        range(0, len(all_patient_blob_names), BATCH_SIZE), start=1
    ):
        batch = all_patient_blob_names[start : start + BATCH_SIZE]

        logger.info(f"Batch {batch_number:04d} started: {len(batch)} bundles")

        batch_patients = []
        batch_encounters = []
        # batch_observations = []
        batch_conditions = []
        batch_procedures = []
        batch_medication_requests = []

        patient_passed, patient_failed = 0, 0
        encounter_passed, encounter_failed = 0, 0
        # observation_passed, observation_failed = 0, 0
        condition_passed, condition_failed = 0, 0
        procedure_passed, procedure_failed = 0, 0
        medication_requests_passed, medication_requests_failed = 0, 0

        for blob_name in batch:
            bundle = extract_bundle(container_client, blob_name)

            patients, passed, failed = process_resources(
                bundle, "Patient", transform_patients
            )
            batch_patients.extend(patients)
            patient_passed += passed
            patient_failed += failed

            encounters, passed, failed = process_resources(
                bundle, "Encounter", transform_encounters
            )
            batch_encounters.extend(encounters)
            encounter_passed += passed
            encounter_failed += failed

            # observations, passed, failed = process_resources(
            #     bundle,
            #     "Observation",
            #     transform_observations
            # )
            # batch_observations.extend(observations)
            # condition_passed += passed
            # condition_failed += failed

            conditions, passed, failed = process_resources(
                bundle, "Condition", transform_conditions
            )
            batch_conditions.extend(conditions)
            condition_passed += passed
            condition_failed += failed

            procedures, passed, failed = process_resources(
                bundle, "Procedure", transform_procedures
            )
            batch_procedures.extend(procedures)
            procedure_passed += passed
            procedure_failed += failed

            medication_requests, passed, failed = process_resources(
                bundle, "MedicationRequest", transform_medication_requests
            )
            batch_medication_requests.extend(medication_requests)
            medication_requests_passed += passed
            medication_requests_failed += failed

        log_and_load_batch(
            blob_service_client,
            container_name,
            "Patient",
            "patients",
            batch_patients,
            patient_passed,
            patient_failed,
            batch_number,
        )

        log_and_load_batch(
            blob_service_client,
            container_name,
            "Encounter",
            "encounters",
            batch_encounters,
            encounter_passed,
            encounter_failed,
            batch_number,
        )

        # log_and_load_batch(
        #    blob_service_client,
        #    container_name,
        #    "Observation",
        #    "observations",
        #    batch_observations,
        #    observation_passed,
        #    observation_failed,
        #    batch_number,
        # )

        log_and_load_batch(
            blob_service_client,
            container_name,
            "Condition",
            "conditions",
            batch_conditions,
            condition_passed,
            condition_failed,
            batch_number,
        )

        log_and_load_batch(
            blob_service_client,
            container_name,
            "Procedure",
            "procedures",
            batch_procedures,
            procedure_passed,
            procedure_failed,
            batch_number,
        )

        log_and_load_batch(
            blob_service_client,
            container_name,
            "Medication Request",
            "medication_requests",
            batch_medication_requests,
            medication_requests_passed,
            medication_requests_failed,
            batch_number,
        )


if __name__ == "__main__":
    main()
