
import pytest
import sys, os, pprint

sys.path.append(os.getcwd())

from phinrip.clip_controller import ClipController, Clip, RandomClipGenerator



class StubAgent:

    def __init__(self):
        self.msg_log = []

    def send(self, msg):
        self.msg_log.append(msg)

    def blocking_listen(self):
        return object()
        

if __name__ == '__main__':
    cc = ClipController(RandomClipGenerator(),
                        StubAgent)

    cc.runFor(10)
    pprint.pprint(cc.event_log())
