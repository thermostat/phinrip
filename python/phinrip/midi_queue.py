
"""
"""

import mido

from .event import DiscreteEventQueue


class MidiAgent:
    def __init__(self, out_str=None, in_str=None):
        self._out_str = out_str
        self._in_str = in_str
        self.in_port = None
        self.out_port = None

    def open_ports(self, out_str=None, in_str=None):
        if out_str:
            self._out_str = out_str
        if in_str:
            self._in_str = in_str
        if self._out_str:
            self.out_port = mido.open_output(self._out_str)
        if self._in_str:
            self.in_port = mido.open_input(self._in_str)

    def blocking_listen(self):
        return self.in_port.receive()

    def send(self, midimsg):
        self.out_port.send(msg)

class ExternalSyncQueue:
    def __init__(self, agent):
        self._queue = DiscreteEventQueue()
        self._agent = agent
        self._keep_running = True

    def run(self):
        while self._keep_running:
            msg = self._agent.blocking_listen()
            # TODO: check msg --
            # Assume it is a tick message for now.
            self._queue.tick()

    def add(self, event):
        self._queue.add(event)

    def current_time(self):
        return self._queue.current_time()

    def event_log(self):
        return self._queue.event_log()

    def stop(self):
        self._keep_running = False
