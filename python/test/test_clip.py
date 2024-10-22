import pytest
import sys, os

sys.path.append(os.getcwd())

from phinrip.clip_controller import ClipController, Clip, RandomClipGenerator


class StubAgent:

    def __init__(self):
        self.msg_log = []

    def send(self, msg):
        self.msg_log.append(msg)

    def blocking_listen(self):
        return object()
        
def test_clip_controller():
    cc = ClipController(RandomClipGenerator(),
                        StubAgent)

    cc.runFor(10)
    assert len(cc._agent.msg_log) == 10, "Did not generate msgs"
