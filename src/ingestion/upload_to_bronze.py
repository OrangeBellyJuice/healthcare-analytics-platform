import logging
import time
from collections.abc import Callable
from functools import partial
from pathlib import Path

from azure.core.exceptions import AzureError
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

from src.config.logging_config import setup_logging

logger = logging.getLogger(__name__)


class UploadError(Exception):
    pass


def find_json_files(folder_path: Path) -> list[Path]:
    return list(folder_path.glob("*.json"))


def upload_files(
    json_files: list[Path], uploader: Callable[[Path], None]
) -> tuple[int, int]:

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

        except UploadError as e:
            files_failed += 1

            logger.error(f"[{index}/{len(json_files)}] {json_file.name} failed - {e}")

    logger.info(f"Upload finished: {files_uploaded} succeeded, {files_failed} failed")

    return files_uploaded, files_failed


def upload_blob_file(
    blob_service_client: BlobServiceClient,
    container_name: str,
    file_path: Path,
    max_retries=3,
) -> None:
    for attempt in range(1, max_retries + 1):
        try:
            container_client = blob_service_client.get_container_client(
                container=container_name
            )

            with file_path.open("rb") as data:
                container_client.upload_blob(
                    name=f"bronze/{file_path.name}",
                    data=data,
                    overwrite=True,
                )

            return

        except (AzureError, OSError, TimeoutError) as e:
            if attempt == max_retries:
                raise UploadError(f"Failed to upload {file_path.name} - {e}") from e

            logger.warning(
                f"{file_path.name} upload attempt "
                f"{attempt}/{max_retries} failed - retrying"
            )

            time.sleep(2 * attempt)


def main():
    setup_logging("upload_to_bronze.log")
    folder_path = Path("/data/test_fhir/").expanduser()

    container_name = "lake"
    account_url = "https://syntheagendata.blob.core.windows.net"

    credential = DefaultAzureCredential()
    blob_service_client = BlobServiceClient(account_url, credential=credential)

    uploader = partial(upload_blob_file, blob_service_client, container_name)

    logger.info("Ingestion Started")

    json_files = find_json_files(folder_path)
    uploaded, failed = upload_files(json_files, uploader)

    logger.info(f"Ingestion Finished: {uploaded} uploaded and {failed} failed")


if __name__ == "__main__":
    main()
