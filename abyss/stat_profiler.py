import sys
import threading

from abyss.activity import BackgroundActivity
from abyss.stack_utils import format_frames
from abyss.time_utils import get_time


class StatProfiler(BackgroundActivity):
    def __init__(self, queue, interval, capture_classnames=True, ignored_thread_ids=()):
        super().__init__()
        self.interval = interval
        self.queue = queue
        self.capture_classnames = capture_classnames
        self.ignored_thread_ids = ignored_thread_ids or ()

    def run(self):
        queue = self.queue
        stop_event = self.stop_event
        interval = self.interval
        capture_classnames = self.capture_classnames
        ignored_thread_ids = set(self.ignored_thread_ids)
        ignored_thread_ids.add(threading.current_thread().ident)

        def capture():
            time = get_time()
            stacks = {
                thread_id: format_frames(frame, with_class=capture_classnames)
                for (thread_id, frame) in sys._current_frames().items()
                if thread_id not in ignored_thread_ids
            }
            if stacks:
                queue.put((time, "stacks", stacks))

        self.log.info("Entering capture loop...")
        n_caps = 0
        while not stop_event.wait(timeout=interval):
            capture()
            n_caps += 1
        self.log.info(
            "Capture loop exited (%d captures). Doing last capture...", n_caps
        )
        capture()
