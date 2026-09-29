import logging
from pathlib import Path

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

from src.extraction.extract_bronze import extract_from_bronze
from src.loading.load_silver import load_to_silver
from src.transforms.organization import transform_organizations
from src.transforms.practitioner import transform_practitioners
from src.validations.validators import validate_organizations, validate_practitioners

ACCOUNT_URL = "https://syntheagendata.blob.core.windows.net"
CONTAINER_NAME = "lake"


def configure_logging() -> None:
    log_dir = Path(__file__).resolve().parents[2] / "logs"
    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / "bronze_to_silver.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        handlers=[logging.StreamHandler(), logging.FileHandler(log_file)],
    )


def run_practitioner_pipeline() -> None:
    configure_logging()

    logger = logging.getLogger(__name__)
    logger.info("Practitioner Bronze -> Silver pipeline has started")

    credential = DefaultAzureCredential()
    blob_service_client = BlobServiceClient(ACCOUNT_URL, credential=credential)
    bronze_blob_name = "bronze/practitionerInformation1790018762251.json"
    silver_blob_name = "silver/practitioners.parquet"

    raw_practitioners = extract_from_bronze(
        blob_service_client, CONTAINER_NAME, bronze_blob_name, "Practitioner"
    )

    valid_practitioners = validate_practitioners(raw_practitioners)

    clean_practitioners = transform_practitioners(valid_practitioners)

    load_to_silver(
        blob_service_client, CONTAINER_NAME, silver_blob_name, clean_practitioners
    )

    logger.info("Practitioner Bronze -> Silver pipeline has finished")


def run_organization_pipeline() -> None:
    configure_logging()

    logger = logging.getLogger(__name__)
    logger.info("Organization Bronze -> Silver pipeline has started")

    credential = DefaultAzureCredential()
    blob_service_client = BlobServiceClient(ACCOUNT_URL, credential=credential)
    bronze_blob_name = "bronze/hospitalInformation1790018762251.json"
    silver_blob_name = "silver/organizations.parquet"

    raw_organizations = extract_from_bronze(
        blob_service_client, CONTAINER_NAME, bronze_blob_name, "Organization"
    )

    valid_organizations = validate_organizations(raw_organizations)

    clean_organizations = transform_organizations(valid_organizations)

    load_to_silver(
        blob_service_client, CONTAINER_NAME, silver_blob_name, clean_organizations
    )

    logger.info("Organization Bronze -> Silver pipeline has finished")


if __name__ == "__main__":
    run_practitioner_pipeline()
    run_organization_pipeline()
