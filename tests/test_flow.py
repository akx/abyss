# -- encoding: UTF-8 --
import json
import random
import time
from queue import Queue

from six import BytesIO

from abyss.queue_processor import QueueProcessor
from abyss.stat_profiler import StatProfiler


def test_stat_profiler_flow(output_dir):
    q = Queue()
    buffer = BytesIO()
    qp = QueueProcessor(queue=q, fd=buffer)
    qp.start()
    sp = StatProfiler(queue=q, interval=0, ignored_thread_ids=(qp.id(),))
    t0 = time.time()
    sp.start()

    def f(a=0):
        while time.time() - t0 <= 1:
            time.sleep(random.uniform(0, 0.1))
            f(a + 1)

    f(0)
    sp.stop()
    qp.stop()
    jv = buffer.getvalue()
    assert json.loads(jv.decode("utf8"))
    with open(output_dir + "flow.json", "wb") as outf:
        print(outf.name)
        outf.write(jv)
