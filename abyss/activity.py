# -- encoding: UTF-8 --
import threading


class BackgroundActivity(object):
    def __init__(self):
        self.stop_event = threading.Event()
        self.stopped_event = threading.Event()
        self._thread = None

    def start(self):
        if self._thread:
            raise ValueError("Can't restart %r" % self)
        self._thread = thread = threading.Thread(
            name=repr(self),
            target=self._wrap_run,
            daemon=True
        )
        thread.start()

    def stop(self):
        self.stop_event.set()
        self.stopped_event.wait()

    def _wrap_run(self):
        try:
            self.run()
        finally:
            self.stopped_event.set()

    def run(self):
        raise NotImplementedError("Implement %r.run()" % self)
