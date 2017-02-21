# -- encoding: UTF-8 --
import json

from six import text_type
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
        while True:
            try:
                ts, type, payload = queue.get(timeout=0.1)
            except Empty:
                if stop_event.isSet():
                    break
                continue
            ts *= 1000000.0  # seconds to microseconds
            if type == "stacks":
                stacks = payload
                new_last_stacks = last_stacks.copy()
                for thread_id, new_stack in stacks.items():
                    last_stack = last_stacks.get(thread_id, [])
                    if new_stack and new_stack[-1].is_generator:
                        self.log.debug(
                            "Gluing generator stack of length %d to old stack %d",
                            len(new_stack), len(last_stack)
                        )
                        new_stack = new_stack + last_stack
                    last_stack_i = last_stack[::-1]
                    new_stack_i = new_stack[::-1]
                    remove_common([last_stack_i, new_stack_i])
                    for type, frame in diff_stacks(last_stack_i, new_stack_i):
                        if frame.classname:
                            name = "%s:%s" % (frame.classname, frame.func)
                        elif frame.func == "<module>":
                            name = frame.filename
                        else:
                            name = frame.func
                        self.emit_event({
                            "name": name,
                            "ts": ts,
                            "tid": thread_id,
                            "pid": 0,
                            "ph": ("B" if type == "enter" else "E"),
                        })
                    new_last_stacks[thread_id] = new_stack
                last_stacks = new_last_stacks
            elif type == "instant":
                self.emit_event({
                    "name": text_type(payload),
                    "ts": ts,
                    "pid": 0,
                    "ph": "i",
                    "s": "g",  # TODO: Support other scopes?
                })

    def stopped(self):
        self.log.info("Emitted %d entries.", self.n_emitted)
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
