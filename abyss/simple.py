import datetime
import os
import sys
from contextlib import contextmanager
from queue import Queue

from abyss.queue_processor import QueueProcessor
from abyss.stat_profiler import StatProfiler
from abyss.time_utils import get_time


class SimpleProfiler:
    def __init__(self, output_file, interval=0):
        if isinstance(output_file, str):
            output_file = open(output_file, "wb")
        self.queue = Queue()
        self.output_file = output_file
        self.queue_proc = QueueProcessor(queue=self.queue, fd=self.output_file)
        self.queue_proc.start()
        self.stat_prof = StatProfiler(
            queue=self.queue,
            interval=interval,
            ignored_thread_ids=(self.queue_proc.id(),),
        )

    def start(self):
        self.stat_prof.start()

    def stop(self):
        self.stat_prof.stop()
        self.queue_proc.stop()
        if get_default() is self:
            set_default(None)

    def post_event(self, text):
        self.queue.put((get_time(), "instant", text))

    @classmethod
    def new_default(cls, *args, **kwargs):
        profiler = cls(*args, **kwargs)
        set_default(profiler)
        return profiler


def get_default():
    return getattr(sys, "_default_abyss", None)


def set_default(profiler):
    sys._default_abyss = profiler


def post_event(text):
    profiler = get_default()
    if profiler:
        profiler.post_event(text)


@contextmanager
def profiling(output_file=None, **kwargs):
    if not output_file:
        output_file = f"abyss-{datetime.datetime.now().isoformat().replace(':', '-')}-{os.getpid():d}.tracing"
    old_default = get_default()
    profiler = SimpleProfiler.new_default(output_file=output_file, **kwargs)
    profiler.start()
    try:
        yield
    finally:
        profiler.stop()
        sys.stderr.write(f"** Abyss: Wrote to {output_file}\n")
        set_default(old_default)
