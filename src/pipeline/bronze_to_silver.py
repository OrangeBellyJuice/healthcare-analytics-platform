import logging

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

from src.config.logging_config import setup_logging
from src.extraction.extract_bronze import extract_from_bronze
from src.loading.load_silver import load_to_silver
from src.transforms.organization import transform_organizations
from src.transforms.practitioner import transform_practitioners
from src.validations.validators import validation

ACCOUNT_URL = "https://syntheagendata.blob.core.windows.net"
CONTAINER_NAME = "lake"

logger = logging.getLogger(__name__)


def run_practitioner_pipeline() -> None:

    logger.info("Practitioner Bronze -> Silver pipeline has started")

    credential = DefaultAzureCredential()
    blob_service_client = BlobServiceClient(ACCOUNT_URL, credential=credential)
    bronze_blob_name = "bronze/practitionerInformation1790018762251.json"
    silver_blob_name = "silver/practitioners.parquet"

    raw_practitioners = extract_from_bronze(
        blob_service_client, CONTAINER_NAME, bronze_blob_name, "Practitioner"
    )

    valid_practitioners = validation(raw_practitioners)

    clean_practitioners = transform_practitioners(valid_practitioners)

    load_to_silver(
        blob_service_client, CONTAINER_NAME, silver_blob_name, clean_practitioners
    )

    logger.info("Practitioner Bronze -> Silver pipeline has finished")


def run_organization_pipeline() -> None:

    logger.info("Organization Bronze -> Silver pipeline has started")

    credential = DefaultAzureCredential()
    blob_service_client = BlobServiceClient(ACCOUNT_URL, credential=credential)
    bronze_blob_name = "bronze/hospitalInformation1790018762251.json"
    silver_blob_name = "silver/organizations.parquet"

    raw_organizations = extract_from_bronze(
        blob_service_client, CONTAINER_NAME, bronze_blob_name, "Organization"
    )

    valid_organizations = validation(raw_organizations)

    clean_organizations = transform_organizations(valid_organizations)

    load_to_silver(
        blob_service_client, CONTAINER_NAME, silver_blob_name, clean_organizations
    )

    logger.info("Organization Bronze -> Silver pipeline has finished")


if __name__ == "__main__":
    setup_logging("bronze_to_silver.log")

    run_practitioner_pipeline()
    run_organization_pipeline()
