import io

import pandas as pd

from src.loading.write_silver import (
    create_dataframe,
    serialize_parquet,
    write_practitioners_to_silver,
    write_silver_blob,
)


class FakeContainerClient:
    def __init__(self):
        self.uploads = []

    def upload_blob(self, name, data, overwrite):
        self.uploads.append((name, overwrite))


class FakeBlobServiceClient:
    def __init__(self):
        self.container_client = FakeContainerClient()

    def get_container_client(self, container):
        return self.container_client


practitioners = [
    {
        "practitioner_id": "4ac6772e-f4cd-3862-b53c-bb433031afc9",
        "last_name": "Schumm",
        "first_name": "Hilari",
        "prefix": "Dr.",
        "full_name": "Hilari Schumm",
        "full_title": "Dr. Hilari Schumm",
        "address": "201-7315 Edmonds Street",
        "city": "Burnaby",
        "province": "BC",
        "postal_code": "V3N 1A7",
        "country": "CA",
        "gender": "male",
    }
]


def test_write_practitioner_to_silver_orchestration():
    fake_client = FakeBlobServiceClient()

    write_practitioners_to_silver(
        fake_client,
        "lake",
        "silver/practitioners.parquet",
        practitioners,
    )

    assert len(fake_client.container_client.uploads) == 1
    assert fake_client.container_client.uploads[0][0] == (
        "silver/practitioners.parquet"
    )


def test_write_silver_blob():
    fake_client = FakeBlobServiceClient()

    write_silver_blob(
        fake_client,
        "lake",
        "practitioners.parquet",
        serialize_parquet(create_dataframe(practitioners)),
    )

    assert len(fake_client.container_client.uploads) == 1
    assert fake_client.container_client.uploads[0][0] == "practitioners.parquet"


def test_create_dataframe_from_practitioners():

    results = create_dataframe(practitioners)

    assert len(results) == 1
    assert (results["practitioner_id"] == "4ac6772e-f4cd-3862-b53c-bb433031afc9").any()
    assert list(results.columns) == [
        "practitioner_id",
        "last_name",
        "first_name",
        "prefix",
        "full_name",
        "full_title",
        "address",
        "city",
        "province",
        "postal_code",
        "country",
        "gender",
    ]


def test_serialize_parquet_from_dataframe():

    results = serialize_parquet(create_dataframe(practitioners))

    assert isinstance(results, bytes)


def test_practitioner_dataframe_can_round_trip_through_parquet():

    results_df = create_dataframe(practitioners)
    results_parq = serialize_parquet(results_df)

    results_back_to_df = pd.read_parquet(io.BytesIO(results_parq))

    assert len(results_back_to_df) == 1
    assert (
        results_back_to_df["practitioner_id"] == "4ac6772e-f4cd-3862-b53c-bb433031afc9"
    ).any()
    assert list(results_back_to_df.columns) == [
        "practitioner_id",
        "last_name",
        "first_name",
        "prefix",
        "full_name",
        "full_title",
        "address",
        "city",
        "province",
        "postal_code",
        "country",
        "gender",
    ]
