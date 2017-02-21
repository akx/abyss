# -- encoding: UTF-8 --
import glob
import os
import time

from abyss.simple import profiling


def test_simple(request, tmpdir):
    cwd = os.getcwd()
    request.addfinalizer(lambda: os.chdir(cwd))
    os.chdir(str(tmpdir))
    with profiling():
        for x in range(5):
            time.sleep(0.1)
    assert glob.glob(os.path.join(str(tmpdir), '*.tracing'))  # Yup, tracing file generated
