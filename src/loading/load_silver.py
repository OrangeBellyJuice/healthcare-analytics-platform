from io import BytesIO

import pandas as pd
from azure.storage.blob import BlobServiceClient


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
    df = create_dataframe(records)
    parquet_bytes = serialize_parquet(df)
    write_silver_blob(
        blob_service_client, container_name, silver_blob_name, parquet_bytes
    )
