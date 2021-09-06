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

Add `abyss.django.abyss_middleware` to your `MIDDLEWARE`.

Abyss will generate a tracing file in `abyss-django/` for every request.

You can load these in `chrome://tracing`.
