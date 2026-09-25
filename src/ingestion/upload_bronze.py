import logging
from collections.abc import Callable
from functools import partial
from pathlib import Path

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

logger = logging.getLogger(__name__)


def find_json_files(folder_path: Path) -> list[Path]:
    return list(folder_path.glob("*.json"))


def upload_files(json_files: list[Path], uploader: Callable[[Path], None]) -> None:
    if not json_files:
        logger.warning("No JSON files found to upload")
        return 0, 0

    logger.info(f"Starting the upload of {len(json_files)} files")
    files_uploaded, files_failed = 0, 0

    for index, json_file in enumerate(json_files, start=1):
        try:
            uploader(json_file)
            files_uploaded += 1
            logger.info(f"[{index}/{len(json_files)}] {json_file.name} uploaded")
        except Exception as e:
            files_failed += 1
            logger.error(f"[{index}/{len(json_files)}] {json_file.name} failed - {e}")

    logger.info(f"Upload finished: {files_uploaded} succeeded, {files_failed} failed")

    return files_uploaded, files_failed


def upload_blob_file(
    blob_service_client: BlobServiceClient, container_name: str, file_path: Path
) -> None:

    container_client = blob_service_client.get_container_client(
        container=container_name
    )

    with file_path.open("rb") as data:
        container_client.upload_blob(
            name=f"bronze/{file_path.name}", data=data, overwrite=True
        )


if __name__ == "__main__":
    folder_path = Path("~/synthea/output/fhir/").expanduser()

    container_name = "lakehouse"
    account_url = "https://synhealthcarelake.blob.core.windows.net"

    credential = DefaultAzureCredential()
    blob_service_client = BlobServiceClient(account_url, credential=credential)

    uploader = partial(upload_blob_file, blob_service_client, container_name)

    logging.basicConfig(level=logging.INFO)
    logger.info("Ingestion Started")

    json_files = find_json_files(folder_path)
    uploaded, failed = upload_files(json_files, uploader)

    logger.info("Ingestion Finished")
