from json import loads

from azure.storage.blob import BlobServiceClient


def extract_practitioner_resources(bundle: dict) -> list[dict]:
    return [
        entry["resource"]
        for entry in bundle["entry"]
        if entry["resource"]["resourceType"] == "Practitioner"
    ]


def extract_from_bronze(
    blob_service_client: BlobServiceClient, container_name: str, blob_name: str
) -> list[dict]:
    blob_client = blob_service_client.get_blob_client(
        container=container_name, blob=blob_name
    )

    bundle = loads(blob_client.download_blob().readall())

    return extract_practitioner_resources(bundle)
