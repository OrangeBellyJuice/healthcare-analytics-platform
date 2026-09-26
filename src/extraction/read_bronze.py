from json import loads

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient


def extract_practitioner_resources(bundle: dict) -> list[dict]:
    return [
        entry["resource"]
        for entry in bundle["entry"]
        if entry["resource"]["resourceType"] == "Practitioner"
    ]


def read_practitioner_bronze(
    blob_service_client: BlobServiceClient, container_name: str, blob_name: str
) -> list[dict]:
    blob_client = blob_service_client.get_blob_client(
        container=container_name, blob=blob_name
    )

    bundle = loads(blob_client.download_blob().readall())

    return extract_practitioner_resources(bundle)


if __name__ == "__main__":
    container_name = "lakehouse"
    blob_name = "bronze/practitionerInformation1790018762251.json"
    account_url = "https://syntheagendata.blob.core.windows.net"
    default_credential = DefaultAzureCredential()
    blob_service_client = BlobServiceClient(account_url, credential=default_credential)

    practitioners_bronze = read_practitioner_bronze(
        blob_service_client, container_name, blob_name
    )
