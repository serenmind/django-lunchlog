import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse
from rest_framework.test import APIClient

from receipts.models import Receipt, ReceiptImage, PlaceInfo


@pytest.fixture
def user(db):
    User = get_user_model()
    return User.objects.create_user(username="testuser", password="pw")


@pytest.fixture
def auth_client(user):
    client = APIClient()
    client.force_authenticate(user)
    return client


@pytest.fixture
def receipt(user):
    return Receipt.objects.create(
        user=user,
        date="2025-09-01",
        price="10.00",
        restaurant_name="Cafe",
        address="Main St",
    )


@pytest.mark.django_db
def test_upload_images(auth_client, receipt, tmp_path):
    # Use local FS with a tmp media root to avoid touching real storage.
    with override_settings(
        DEFAULT_FILE_STORAGE="django.core.files.storage.FileSystemStorage",
        MEDIA_ROOT=str(tmp_path),
    ):
        url = reverse("receipt-upload-images", args=[receipt.id])
        file = SimpleUploadedFile("img.jpg", b"JPEGDATA", content_type="image/jpeg")

        resp = auth_client.post(url, {"images": [file]}, format="multipart")
        assert resp.status_code == 201
        assert ReceiptImage.objects.filter(receipt=receipt).count() == 1


@pytest.mark.django_db
def test_delete_receipt_image_triggers_storage_delete(receipt, tmp_path, monkeypatch):
    # Use local FS with a tmp media root to avoid external calls.
    with override_settings(
        DEFAULT_FILE_STORAGE="django.core.files.storage.FileSystemStorage",
        MEDIA_ROOT=str(tmp_path),
    ):
        ri = ReceiptImage.objects.create(receipt=receipt)
        # Assign a fake name to avoid writing a real file.
        ri.image.name = "receipts/fake.jpg"
        ri.save(update_fields=["image"])

        called = {"deleted": False}

        def fake_delete(name, *args, **kwargs):
            called["deleted"] = True

        # Patch the concrete storage used by this FieldFile (works regardless of backend).
        monkeypatch.setattr(ri.image.storage, "delete", fake_delete, raising=True)

        ri.delete()
        assert called["deleted"] is True


@pytest.mark.django_db
def test_fetch_places_task(monkeypatch):
    # Import inside test to ensure settings/patches apply to the module.
    import receipts.tasks as tasks

    class FakeResp:
        def raise_for_status(self):
            return None

        def json(self):
            return {
                "results": [
                    {
                        "place_id": "p1",
                        "name": "Place 1",
                        "formatted_address": "Addr 1",
                        "types": ["restaurant"],
                        "rating": 4.5,
                    },
                    {
                        "place_id": "p2",
                        "name": "Place 2",
                        "formatted_address": "Addr 2",
                        "types": ["restaurant"],
                        "rating": 4.0,
                    },
                ]
            }

    with override_settings(GOOGLE_PLACES_API_KEY="fake-key"):
        # Patch requests at the point of use in the tasks module.
        monkeypatch.setattr("receipts.tasks.requests.get", lambda *a, **k: FakeResp())

        saved = tasks._fetch_places_for_receipt("1", "Some Address")

    assert isinstance(saved, list)
    assert len(saved) == 2
    assert set(saved) == {"p1", "p2"}
    assert PlaceInfo.objects.filter(place_id__in=saved).count() == 2
