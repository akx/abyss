import sys

if sys.platform == "win32":
    from time import time, clock
    # On Windows, `clock()` "returns wall-clock seconds elapsed since the first call to this function".
    clock()  # Initialize the counter.
    t0 = time()  # Reference time
    get_time = lambda: t0 + clock()
else:
    from time import time
    # TODO: use clock_*?
    get_time = time
