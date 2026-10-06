import logging

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

from src.config.logging_config import setup_logging
from src.extraction.extract_from_bronze import extract_from_bronze
from src.loading.load_to_silver import load_to_silver
from src.transforms.patient import transform_patients
from src.validations.validators import validation

ACCOUNT_URL = "https://syntheagendata.blob.core.windows.net"
CONTAINER_NAME = "lake"

logger = logging.getLogger(__name__)


def run_patient_pipeline() -> None:

    logger.info("Patient Bronze -> Silver pipeline has started")

    credential = DefaultAzureCredential()
    blob_service_client = BlobServiceClient(ACCOUNT_URL, credential=credential)
    bronze_blob_name = "bronze/hospitalInformation1790018762251.json"
    silver_blob_name = "silver/patinets.parquet"

    raw_patientss = extract_from_bronze(
        blob_service_client, CONTAINER_NAME, bronze_blob_name, "Patient"
    )

    valid_patientss = validation(raw_patients)

    clean_patients = transform_organizations(valid_patients)

    load_to_silver(
        blob_service_client, CONTAINER_NAME, silver_blob_name, clean_patients
    )

    logger.info("Patient Bronze -> Silver pipeline has finished")


if __name__ == "__main__":
    setup_logging("bronze_to_silver.log")

    run_patient_pipeline()
