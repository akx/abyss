import logging
import threading


class BackgroundActivity:
    def __init__(self):
        self.log = logging.getLogger("abyss." + self.__class__.__name__)
        self.stop_event = threading.Event()
        self.stopped_event = threading.Event()
        self._thread = None

    def start(self):
        if self._thread:
            raise ValueError(f"Can't restart {self!r}")
        self._thread = thread = threading.Thread(name=repr(self), target=self._wrap_run)
        thread.daemon = True
        thread.start()

    def stopped(self):
        pass

    def stop(self, timeout=None):
        if not self._thread:  # Never started.
            return
        self.log.info("Stopping...")
        self.stop_event.set()
        self.stopped_event.wait(timeout=timeout)
        self.log.info("Stopped.")

    def _wrap_run(self):
        try:
            self.run()
        finally:
            self.log.info("run() exited.")
            self.stopped_event.set()
            self.stopped()

    def run(self):
        raise NotImplementedError(f"Implement {self!r}.run()")

    def id(self):
        if self._thread:
            return self._thread.ident
