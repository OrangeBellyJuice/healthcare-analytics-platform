import logging
from io import BytesIO

import pandas as pd
from azure.storage.blob import BlobServiceClient


logger = logging.getLogger(__name__)


def create_dataframe(records: list[dict]) -> pd.DataFrame:
    return pd.DataFrame(records)


def serialize_parquet(df: pd.DataFrame) -> bytes:
    buffer = BytesIO()

    df.to_parquet(buffer, engine="pyarrow", index=False)

    return buffer.getvalue()


def write_silver_blob(
    blob_service_client: BlobServiceClient,
    container_name: str,
    silver_blob_name: str,
    parquet_bytes: bytes,
) -> None:

    container_client = blob_service_client.get_container_client(
        container=container_name
    )

    container_client.upload_blob(
        name=silver_blob_name, data=parquet_bytes, overwrite=True
    )


def load_to_silver(
    blob_service_client: BlobServiceClient,
    container_name: str,
    silver_blob_name: str,
    records: list[dict],
) -> None:

    logger.info(f"Loading {len(records)} records to {silver_blob_name}")

    df = create_dataframe(records)

    logger.info(f"Created DataFrame with {len(df)} rows and {len(df.columns)} columns")

    parquet_bytes = serialize_parquet(df)

    logger.info(f"Serialized {silver_blob_name} to Parquet ({len(parquet_bytes)}) bytes")

    write_silver_blob(
        blob_service_client, container_name, silver_blob_name, parquet_bytes
    )

    logger.info(f"Successfully loaded {silver_blob_name} to Silver")
