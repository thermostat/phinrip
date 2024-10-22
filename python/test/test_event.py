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
    
def test_queue_process():
    callback = lambda x: print(repr(x))
    q = DiscreteEventQueue()
    e1 = Event(5, callback)
    e2 = Event(1, callback)
    e3 = Event(3, callback)
    q.add(e1)
    q.add(e2)
    q.add(e3)
    q.tick(10)
    # Ensure the first event fired first
    assert q.event_log()[0].firetime() == 1
    # Ensure all events were processed
    assert len(q.event_log()) == 3
