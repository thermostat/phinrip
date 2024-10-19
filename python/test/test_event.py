import pytest
import sys, os

sys.path.append(os.getcwd())

from phinrip.event import DiscreteEventQueue, Event

def test_eventq():
    q = DiscreteEventQueue()
    q.tick()
    assert q.current_time() == 1

def test_event():
    e = Event(0, lambda x: print(repr(x)))
    e.fire()
    
