# -*- coding: utf-8 -*-
import datetime
import os
from contextlib import contextmanager

import six
import sys

from abyss.time_utils import get_time

try:
    from queue import Queue
except ImportError:
    from six.moves.queue import Queue

from abyss.queue_processor import QueueProcessor
from abyss.stat_profiler import StatProfiler


class SimpleProfiler(object):
    def __init__(self, output_file, interval=0):
        if isinstance(output_file, six.string_types):
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
    setattr(sys, "_default_abyss", profiler)


def post_event(text):
    profiler = get_default()
    if profiler:
        profiler.post_event(text)


@contextmanager
def profiling(output_file=None, **kwargs):
    if not output_file:
        output_file = 'abyss-%08x-%s.tracing' % (os.getpid(), datetime.datetime.now().isoformat().replace(':', '-'))
    old_default = get_default()
    profiler = SimpleProfiler.new_default(output_file=output_file, **kwargs)
    profiler.start()
    yield
    profiler.stop()
    sys.stderr.write('** Abyss: Wrote to %s\n' % output_file)
    set_default(old_default)
