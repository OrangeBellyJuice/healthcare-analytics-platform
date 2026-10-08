import logging

from azure.core.exceptions import AzureError
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

from src.config.logging_config import setup_logging
from src.extraction.extract_from_bronze import (
    extract_bundle,
    extract_patient_blob_names,
    extract_resources,
)
from src.loading.load_to_silver import load_to_silver
from src.transforms.encounter import transform_encounters
from src.validations.validators import validation

logger = logging.getLogger(__name__)

BATCH_SIZE = 500


def main():
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

    logger.info(f"Found {len(all_patient_blob_names)} patient bundlls in Bronze")

    organization_blob = "bronze/hospitalInformation1790018762251.json"
    practitioner_blob = "bronze/practitionerInformation1790018762251.json"

    logger.info("Bronze to Silver ETL Started")

    # process_organizations(organization_blob)
    # process_practitioners(practitioner_blob)
    # process_patients(all_patient_blob_names)

    batch_number = 1
    for start in range(0, len(all_patient_blob_names), BATCH_SIZE):
        batch = all_patient_blob_names[start : start + BATCH_SIZE]

        logger.info(f"Batch {batch_number:04d} started: {len(batch)} bundles")

        # batch_patients = []
        batch_encounters = []
        # batch_observations = []
        # batch_conditions = []
        # batch_procedures = []
        # batch_medication_requests = []
        #
        # patient_valid_count = 0
        # patient_failed_count = 0
        encounter_valid_count = 0
        encounter_failed_count = 0

        for blob_name in batch:
            bundle = extract_bundle(container_client, blob_name)

            # patient_resources = extract_resources(bundle, "Patient")
            # valid_patients = validation(patient_resources)
            # patient_valid_count += len(valid_patients)
            # patient_failed_count += len(patient_resources) - len(valid_patients)
            # clean_patients = transform_patients(valid_patients)
            # batch_patients.extend(clean_patients)

            encounter_resources = extract_resources(bundle, "Encounter")
            valid_encounters = validation(encounter_resources)
            encounter_valid_count += len(valid_encounters)
            encounter_failed_count += len(encounter_resources) - len(valid_encounters)
            clean_encounters = transform_encounters(valid_encounters)
            batch_encounters.extend(clean_encounters)

        # logger.info(
        # f"Patient validation: {patient_valid_count} passed, {patient_failed_count} failed"
        # )

        # logger.info(f"Patient transformation: {len(batch_patients)} transformed")

        logger.info(
            f"Encounter validation: {encounter_valid_count} passed, {encounter_failed_count} failed"
        )

        logger.info(f"Encounter transformation: {len(batch_encounters)} transformed")

        # load_to_silver(
        # blob_service_client,
        # container_name,
        # f"silver/patients/part-{batch_number:04d}.parquet",
        # batch_patients,
        # )

        load_to_silver(
            blob_service_client,
            container_name,
            f"silver/encounters/part-{batch_number:04d}.parquet",
            batch_encounters,
        )

        # logger.info(f"Loaded {len(batch_patients)} Patient records")

        logger.info(f"Loaded {len(batch_encounters)} Encounter records")

        logger.info(f"Batch {batch_number:04d} finished")

        batch_number += 1


if __name__ == "__main__":
    main()
