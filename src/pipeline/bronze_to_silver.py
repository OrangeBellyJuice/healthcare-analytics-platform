from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

from src.extraction.extract_bronze import extract_bronze
from src.loading.load_silver import load_to_silver
from src.transforms.practitioner import transform_practitioners
from src.validations.validators import validate_practitioners


def run_practitioner_pipeline() -> None:
    account_url = "https://syntheagendata.blob.core.windows.net"
    container_name = "lake"

    credential = DefaultAzureCredential()
    blob_service_client = BlobServiceClient(account_url, credential=credential)

    bronze_blob_name = "bronze/practitionerInformation1790018762251.json"
    silver_blob_name = "silver/practitioners.parquet"

    raw_practitioners = extract_bronze(
        blob_service_client, container_name, bronze_blob_name
    )

    valid_practitioners = validate_practitioners(raw_practitioners)

    clean_practitioners = transform_practitioners(valid_practitioners)

    load_to_silver(
        blob_service_client, container_name, silver_blob_name, clean_practitioners
    )


if __name__ == "__main__":
    run_practitioner_pipeline()
