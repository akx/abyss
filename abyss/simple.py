# -*- coding: utf-8 -*-
import six
from six.moves.queue import Queue

from abyss.queue_processor import QueueProcessor
from abyss.stat_profiler import StatProfiler


class SimpleProfiler(object):
    def __init__(self, output_file, interval=0.005):
        if isinstance(output_file, six.string_types):
            output_file = open(output_file, "wb")
        self.q = Queue()
        self.output_file = output_file
        self.qp = QueueProcessor(queue=self.q, fd=self.output_file)
        self.qp.start()
        self.sp = StatProfiler(queue=self.q, interval=0, ignored_thread_ids=(self.qp.id(),))

    def start(self):
        self.sp.start()

    def stop(self):
        self.sp.stop()
        self.qp.stop()
