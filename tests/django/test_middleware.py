import pytest
from django.core.files.storage import get_storage_class
from django.test import Client
from django.urls import reverse

from abyss.django import AbyssMiddleware


@pytest.mark.parametrize("header", (False, True))
@pytest.mark.parametrize("query", (False, True))
def test_middleware(client: Client, header: bool, query: bool):
    storage = get_storage_class(AbyssMiddleware.STORAGE_CLASS)()

    def get_filecount():
        if storage.exists(AbyssMiddleware.FILENAME_PREFIX):
            return len(storage.listdir(AbyssMiddleware.FILENAME_PREFIX)[1])
        return 0

    old_tracefile_count = get_filecount()
    should_trace = header or query

    url = reverse("test")
    if query:
        url = f"{url}?abyss=1"
    headers = {}
    if header:
        headers["HTTP_ABYSS"] = "1"

    response = client.get(url, **headers)
    assert response.status_code == 200
    assert response.content == b"OK"

    new_tracefile_count = get_filecount()

    if should_trace:
        assert new_tracefile_count == old_tracefile_count + 1
    else:
        assert new_tracefile_count == old_tracefile_count
