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

