import logging
import re
from json import JSONDecodeError, loads

from azure.core.exceptions import AzureError
from azure.storage.blob import BlobServiceClient, ContainerClient

logger = logging.getLogger(__name__)


def extract_patient_blob_names(container_client: ContainerClient) -> list[str]:
    blob_names = container_client.list_blob_names(name_starts_with="bronze/")
    pattern = r"bronze\/(?!hospital|practitioner).*$"
    return sorted(
        blob_name for blob_name in blob_names if bool(re.match(pattern, blob_name))
    )


# write test for this functiou
def extract_bundle(container_client: ContainerClient, blob_name: str) -> dict:
    blob_client = container_client.get_blob_client(blob_name)
    blob_bytes = blob_client.download_blob().readall()
    return loads(blob_bytes)


def extract_resources(bundle: dict, resource_type: str) -> list[dict]:
    return [
        entry["resource"]
        for entry in bundle["entry"]
        if entry["resource"]["resourceType"] == resource_type
    ]


def extract_from_bronze(
    blob_service_client: BlobServiceClient,
    container_name: str,
    blob_name: str,
    resource_type: str,
) -> list[dict]:

    logger.info(f"Extracting {resource_type} from {blob_name}")

    try:
        blob_client = blob_service_client.get_blob_client(
            container=container_name, blob=blob_name
        )

        bundle = loads(blob_client.download_blob().readall())
    except (AzureError, JSONDecodeError):
        logger.exception(
            f"Failed to extract {resource_type} resources from {blob_name}"
        )
        raise

    resources = extract_resources(bundle, resource_type)

    if not resources:
        logger.warning(f"No {resource_type} resources found in {blob_name}")
    else:
        logger.info(f"Extracted {len(resources)} {resource_type} resources")

    return resources
