import pytest

from src.ingestion.upload_to_bronze import (
    UploadError,
    find_json_files,
    upload_blob_file,
    upload_files,
)


class FakeContainerClient:
    def __init__(self, failures_before_success=0):
        self.uploads = []
        self.failures_before_success = failures_before_success
        self.upload_calls = 0

    def upload_blob(self, name, data, overwrite):
        self.upload_calls += 1

        if self.upload_calls <= self.failures_before_success:
            raise TimeoutError("The write operation timed out")

        self.uploads.append((name, overwrite))


class FakeBlobServiceClient:
    def __init__(self, failures_before_success=0):
        self.container_client = FakeContainerClient(
            failures_before_success=failures_before_success
        )

    def get_container_client(self, container):
        return self.container_client


def test_upload_files_continues_when_one_file_fails(tmp_path):
    alice = tmp_path / "alice.json"
    bob = tmp_path / "bob.json"
    charlie = tmp_path / "charlie.json"

    alice.touch()
    bob.touch()
    charlie.touch()

    json_files = [alice, bob, charlie]

    attempted_uploads = []

    def fake_uploader(file_path):
        attempted_uploads.append(file_path)

        if file_path.name == "bob.json":
            raise UploadError("Fake upload failure")

    uploaded, failed = upload_files(json_files, fake_uploader)

    assert len(attempted_uploads) == 3
    assert uploaded == 2
    assert failed == 1


def test_upload_blob_file(tmp_path):
    fake_client = FakeBlobServiceClient()

    alice_file = tmp_path / "alice.json"
    alice_file.write_text('{ "name": "alice" }')

    upload_blob_file(fake_client, "lake", alice_file)

    assert fake_client.container_client.upload_calls == 1
    assert len(fake_client.container_client.uploads) == 1
    assert fake_client.container_client.uploads[0][0] == "bronze/alice.json"


def test_upload_blob_file_retries_after_timeout(
    tmp_path,
    monkeypatch,
):
    fake_client = FakeBlobServiceClient(failures_before_success=1)

    alice_file = tmp_path / "alice.json"
    alice_file.write_text('{ "name": "alice" }')

    monkeypatch.setattr(
        "src.ingestion.upload_to_bronze.time.sleep",
        lambda _: None,
    )

    upload_blob_file(
        fake_client,
        "lake",
        alice_file,
        max_retries=3,
    )

    assert fake_client.container_client.upload_calls == 2
    assert len(fake_client.container_client.uploads) == 1
    assert fake_client.container_client.uploads[0][0] == "bronze/alice.json"


def test_upload_blob_file_can_retry_multiple_times(
    tmp_path,
    monkeypatch,
):
    fake_client = FakeBlobServiceClient(failures_before_success=2)

    alice_file = tmp_path / "alice.json"
    alice_file.write_text('{ "name": "alice" }')

    monkeypatch.setattr(
        "src.ingestion.upload_to_bronze.time.sleep",
        lambda _: None,
    )

    upload_blob_file(
        fake_client,
        "lake",
        alice_file,
        max_retries=3,
    )

    assert fake_client.container_client.upload_calls == 3
    assert len(fake_client.container_client.uploads) == 1


def test_upload_blob_file_raises_after_max_retries(
    tmp_path,
    monkeypatch,
):
    fake_client = FakeBlobServiceClient(failures_before_success=10)

    alice_file = tmp_path / "alice.json"
    alice_file.write_text('{ "name": "alice" }')

    monkeypatch.setattr(
        "src.ingestion.upload_to_bronze.time.sleep",
        lambda _: None,
    )

    with pytest.raises(UploadError):
        upload_blob_file(
            fake_client,
            "lake",
            alice_file,
            max_retries=3,
        )

    assert fake_client.container_client.upload_calls == 3
    assert fake_client.container_client.uploads == []


def test_find_json_files_returns_only_json_files(tmp_path):
    alice = tmp_path / "alice.json"
    bob = tmp_path / "bob.json"
    charlie = tmp_path / "charlie.txt"

    alice.touch()
    bob.touch()
    charlie.touch()

    results = find_json_files(tmp_path)

    assert len(results) == 2
    assert alice in results
    assert bob in results
    assert charlie not in results


def test_find_json_files_empty_folder_returns_empty_list(tmp_path):
    assert find_json_files(tmp_path) == []


def test_upload_files_with_no_files_returns_zero_counts():
    uploaded, failed = upload_files(
        [],
        lambda file_path: None,
    )

    assert uploaded == 0
    assert failed == 0
