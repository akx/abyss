# -- encoding: UTF-8 --
import time

from abyss.stat_profiler import StatProfiler
from queue import Queue

from tests.utils import flush_queue


def test_stat_profiler_takes_samples():
    q = Queue()
    sp = StatProfiler(queue=q, interval=0.05)
    t0 = time.time()
    LENGTH = 1
    sp.start()
    while time.time() - t0 <= LENGTH:
        x = locals().get("t0")
    sp.stop()
    samples = list(flush_queue(q))
    expected_n_samples = int(LENGTH / sp.interval)
    assert abs(len(samples) - expected_n_samples) < expected_n_samples / 3
