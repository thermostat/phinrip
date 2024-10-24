#!/bin/env python3

"""
Abstract event framework -
"""
from typing import List
from heapq import heappush, heappop

class Event:
    """
    Event 

    
    """

    def __init__(self, firetime=None, callback=None):
        self._firetime = firetime
        self._callback = callback

    def firetime(self):
        return self._firetime

    def fire(self):
        runcallback = self._fire_event()
        if self._callback and runcallback:
            self._callback(self)

    def time_str(self):
        return f"[t:{self._firetime:08}]"

    def _fire_event(self):
        """
        Override 
        """
        return True

    def __repr__(self):
        return f"{self.time_str()} Generic event @{hex(id(self))}"

    def dict(self):
        d = {
            "firetime" : self.firetime(),
            "description" : repr(self)
            }
        return d
    
class DiscreteEventQueue:

    def __init__(self):
        self._queue : List = []
        self._current_time : int = 0
        self._event_log : List = []

    def tick(self, n=1):
        self._current_time = self._current_time + n
        current_events = []
        while self._queue and (self._queue[0][0] <= self._current_time):
            e_tick, event = heappop(self._queue)
            current_events.append(event)
        self._process_events(current_events)
        for event in current_events:
            self._event_log.append(event)

    def add(self, event):
        event_item = (event.firetime(), event)
        heappush(self._queue, event_item)
            
    def current_time(self):
        return self._current_time

    def event_log(self):
        return self._event_log

    def _process_events(self, eventlist: List):
        for event in eventlist:
            event.fire()
