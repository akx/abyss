# -- encoding: UTF-8 --

from abyss.activity import BackgroundActivity
from abyss.stack_utils import diff_stacks


class QueueProcessor(BackgroundActivity):
    def __init__(self, queue, interval):
        super(QueueProcessor, self).__init__()
        self.interval = interval
        self.queue = queue

    def run(self):
        queue = self.queue
        stop_event = self.stop_event
        last_stacks = {}
        while not stop_event.isSet():
            stacks = queue.get()
            for thread_id, new_stack in stacks.items():
                last_stack = last_stacks.get(thread_id)
                events = diff_stacks(last_stack, new_stack)


            print(last_stacks, stacks)
            last_stacks = stacks
