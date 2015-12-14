# -- encoding: UTF-8 --
from queue import Empty


def flush_queue(queue):
    try:
        while True:
            yield queue.get(False)
    except Empty:
        pass
