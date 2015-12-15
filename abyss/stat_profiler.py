# -- encoding: UTF-8 --
import sys
import threading

from abyss.activity import BackgroundActivity
from abyss.stack_utils import format_frames
from abyss.time_utils import get_time


class StatProfiler(BackgroundActivity):
    def __init__(self, queue, interval, ignored_thread_ids=()):
        super(StatProfiler, self).__init__()
        self.interval = interval
        self.queue = queue
        self.ignored_thread_ids = (ignored_thread_ids or ())

    def run(self):
        queue = self.queue
        stop_event = self.stop_event
        interval = self.interval
        ignored_thread_ids = set(self.ignored_thread_ids)
        ignored_thread_ids.add(threading.current_thread().ident)
        def capture():
            time = get_time()
            stacks = dict(
                (thread_id, format_frames(frame, 1))
                for (thread_id, frame)
                in sys._current_frames().items()
                if thread_id not in ignored_thread_ids
            )
            if stacks:
                queue.put((time, "stacks", stacks))
        while not stop_event.wait(timeout=interval):
            capture()
        capture()
