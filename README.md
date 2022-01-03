abyss
=====

... is a statistical profiler and Chrome tracing file generator for Python.

* Status: WIP but works for me!
* Compatibility: Python 3.6+

Installation
------------

* Clone Abyss somewhere, say, `~/abyss`
* In your "client project", i.e. whatever you're profiling, `pip install -e ~/abyss`

Usage - Python
--------------

```python
from abyss.simple import profiling

with profiling():
    my_slow_code()
```

Abyss will generate a tracing file you can load in `chrome://tracing`

Usage - Django middleware
-------------------------

Add `abyss.django.AbyssMiddleware` to your `MIDDLEWARE`.

By default, the middleware will generate a tracing file for every request that
either has any truthy value in a header or a query parameter named `abyss`.

The generated files will be saved to the configured django media storage
backend, with a prefix of `abyss-django/`.

You can customize the behavior easily by subclassing the middleware and
modifying a few variables or functions, for example:

```python
from abyss.django import AbyssMiddleware
from django.http import HttpRequest


class CustomAbyssMiddleware(AbyssMiddleware):
    STORAGE_CLASS = "storages.backends.s3boto3.S3Boto3Storage"
    FILENAME_PREFIX = "traces/"

    def should_profile_request(self, request: HttpRequest) -> bool:
        return super().should_profile_request(request) and request.user.is_superuser
```

How to analyze tracing files
----------------------------

* [ui.perfetto.dev](https://ui.perfetto.dev/) is pretty snazzy in general.
* The Chrome browser also has a built-in tool for analyzing these files: `chrome://tracing`.
