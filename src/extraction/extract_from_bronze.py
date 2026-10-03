from json import loads

from azure.storage.blob import BlobServiceClient


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
    blob_client = blob_service_client.get_blob_client(
        container=container_name, blob=blob_name
    )

    bundle = loads(blob_client.download_blob().readall())

    return extract_resources(bundle, resource_type)
