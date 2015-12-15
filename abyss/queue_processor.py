# -- encoding: UTF-8 --
import json
from six.moves.queue import Empty

from abyss.activity import BackgroundActivity
from abyss.stack_utils import diff_stacks, remove_common


class QueueProcessor(BackgroundActivity):
    def __init__(self, queue, fd):
        super(QueueProcessor, self).__init__()
        self.queue = queue
        self.fd = fd
        assert hasattr(fd, "write")
        self.n_emitted = 0

    def run(self):
        queue = self.queue
        stop_event = self.stop_event
        last_stacks = {}
        while not stop_event.isSet():
            try:
                ts, type, payload = queue.get(timeout=0.1)
            except Empty:
                continue
            ts *= 1000000.0  # seconds to microseconds
            if type == "stacks":
                stacks = payload
                for thread_id, new_stack in stacks.items():
                    last_stack = last_stacks.get(thread_id, [])[::-1]
                    new_stack = new_stack[::-1]
                    remove_common([last_stack, new_stack])
                    for type, frame in diff_stacks(last_stack, new_stack):
                        self.emit_event({
                            "name": frame[1],
                            "ts": ts,
                            "tid": thread_id,
                            "pid": 0,
                            "ph": ("B" if type == "enter" else "E")
                        })
                last_stacks = stacks

    def stopped(self):
        if self.n_emitted > 0:
            self.fd.write(b"\n]")
        self.fd.flush()

    def emit_event(self, blob):
        fd = self.fd
        if self.n_emitted == 0:
            fd.write(b"[\n")
        else:
            fd.write(b",\n")
        self.n_emitted += 1
        fd.write(json.dumps(blob, separators=",:").encode("utf8"))
