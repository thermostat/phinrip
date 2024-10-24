

from .midi_queue import MidiAgent, ExternalSyncQueue
from .event import Event
import mido

import random

SCENE_COUNT = 8
TRACK_COUNT = 8

class Clip:
    def __init__(self, track_nbr, scene_nbr):
        self.track_nbr = track_nbr
        self.scene_nbr = scene_nbr

    def _convertToNoteVal(self):
        return ((self.track_nbr*SCENE_COUNT)+self.scene_nbr)+10

    def constructMidiMessage(self):
        msg = mido.Message('note_on', note=self._convertToNoteVal())
        return msg

    def __str__(self):
        return f"[Track {self.track_nbr}:Scene {self.scene_nbr}]"

class UpdateEvent(Event):
    def __init__(self, parent, firetime):
        super().__init__(firetime)
        self._parent = parent

    def _fire_event(self):
        self._parent.generateNewEvents(self.firetime())
        # no callback
        return False

    def __repr__(self):
        return f"{self.time_str()} Update event"

class LaunchClipEvent(Event):
    def __init__(self, parent, clip, firetime):
        super().__init__(firetime)
        self._parent = parent
        self._clip = clip

    def _fire_event(self):
        self._parent.sendClip(self._clip)

    def __repr__(self):
        return f"{self.time_str()} Launched {self._clip} at {self.firetime()}"



class RandomClipGenerator:
    def __init__(self,
                 scene_count=SCENE_COUNT,
                 track_count=TRACK_COUNT):
        self._scene_count = scene_count
        self._track_count = track_count
        self._delta = 10

    def generate(self, firetime, controller):
        clip = Clip(random.randint(0, self._track_count-1),
                    random.randint(0, self._scene_count-1))
        launch_event = LaunchClipEvent(controller, clip,
                                       self._delta+firetime)
        return [launch_event]
        
class ClipController:
    """
    Control Bitwig-based clip launcher to 
    play a song
    """

    def __init__(self, clip_event_gen, agent_cls=MidiAgent):
        self._agent = agent_cls()
        self._queue = ExternalSyncQueue(self._agent)
        # default 24 ticks per quarter note
        self.update_interval = 24*4
        self._event_gen = clip_event_gen
        self.update_count = 0

    def generateNewEvents(self, firetime):
        # Add another update item
        self._queue.add(UpdateEvent(self, firetime+self.update_interval))
        self.update_count += 1
        for event in self._event_gen.generate(firetime, self):
            self._queue.add(event)
        if self._end_check(self):
            self._queue.stop()

    def sendClip(self, clip):
        self._agent.send(clip.constructMidiMessage())

    def runFor(self, n):
        self._end_check = lambda x: x.update_count > n
        self._queue.add(UpdateEvent(self, 1))
        self._queue.run()
        # n is the number of updates

    def event_log(self):
        return self._queue.event_log()
