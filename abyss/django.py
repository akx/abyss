import datetime
import os

from abyss.simple import profiling


def abyss_middleware(get_response):
    def middleware(request):
        timestamp = datetime.datetime.now().isoformat().replace(":", "-")
        path_stamp = request.path.strip("/").replace("/", "-")
        filename = f"abyss-django/{path_stamp}_{timestamp}.tracing"
        dir = os.path.dirname(filename)
        if not os.path.isdir(dir):
            os.makedirs(dir)
        with profiling(filename):
            response = get_response(request)
            if hasattr(response, "render") and callable(response.render):
                response.render()
            return response

    return middleware
