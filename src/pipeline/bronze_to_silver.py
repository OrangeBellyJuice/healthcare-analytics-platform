import logging

from azure.core.exceptions import AzureError
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, ContainerClient

from src.config.logging_config import setup_logging
from src.extraction.extract_from_bronze import extract_bundle, extract_resources, extract_patient_blob_names
from src.validations.validators import validation
from src.transforms.patient import transform_patients
from src.loading.load_to_silver import load_to_silver

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

        batch_patients = []
        # batch_encounters = []
        # batch_observations = []
        # batch_conditions = []
        # batch_procedures = []
        # batch_medication_requests = []

        for blob_name in batch:
            bundle = extract_bundle(container_client, blob_name)

            patient_resources = extract_resources(bundle, "Patient")
            valid_patients = validation(patient_resources) 
            clean_patients = transform_patients(valid_patients) 
            batch_patients.extend(clean_patients)

        # write this batch's parquet parts
        load_to_silver(blob_service_client, container_name, f"silver/patients/part-{batch_number:04d}.parquet", batch_patients)
        # ..

        batch_number += 1

if __name__ == "__main__":
    main()

