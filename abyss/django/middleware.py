import datetime
from tempfile import SpooledTemporaryFile
from typing import IO, Callable, Optional, cast

from django.core.files.storage import Storage, get_storage_class
from django.http import HttpRequest, HttpResponse

from abyss.simple import profiling


class AbyssMiddleware:
    BUFFER_SIZE: int = 1048576
    STORAGE_CLASS: Optional[str] = None
    FILENAME_PREFIX: Optional[str] = "abyss-django/"

    get_response: Callable
    storage: Storage

    def __init__(self, get_response: Callable):
        self.get_response = get_response  # type: ignore
        self.storage = self.get_storage()

    def get_storage(self) -> Storage:
        return get_storage_class(self.STORAGE_CLASS)()

    def should_profile_request(self, request: HttpRequest) -> bool:
        return bool(request.headers.get("abyss", False)) or bool(
            request.GET.get("abyss", False)
        )

    def build_filename_for_request(self, request: HttpRequest) -> str:
        timestamp = datetime.datetime.now().isoformat().replace(":", "-")
        path_stamp = request.path.strip("/").replace("/", "-")
        prefix = self.FILENAME_PREFIX or ""
        return f"{prefix}{timestamp}_{path_stamp}.tracing"

    def get_tempfile(self) -> IO:
        return cast(IO, SpooledTemporaryFile(max_size=self.BUFFER_SIZE))

    def save_profiling_tempfile(self, request: HttpRequest, tempfile: IO) -> None:
        filename = self.build_filename_for_request(request)
        self.storage.save(filename, tempfile)

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if not self.should_profile_request(request):
            return self.get_response(request)

        tracefile = self.get_tempfile()
        with profiling(output_file=tracefile):
            response = self.get_response(request)
            if hasattr(response, "render") and callable(response.render):
                response.render()
        self.save_profiling_tempfile(request, tracefile)
        return response
