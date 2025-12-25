
import itertools,inspect,sys

"""
Generate notes


"""

from .note import Note
from .markov import MarkovProcess, MarkovNode

CLASS_MAP = None

def generator_map():
    global CLASS_MAP
    if CLASS_MAP:
        return CLASS_MAP
    class_map = {}
    scls = NoteGenerator
    current_mod = sys.modules[__name__]
    for g in dir(current_mod):
        val = getattr(current_mod,g)
        if inspect.isclass(val) and issubclass(val,scls):
            class_map[val.__name__] = val
    CLASS_MAP = class_map
    return class_map

def take(n, iterable):
    """Return first n items of the iterable as a list."""
    return list(itertools.islice(iterable, n))

class NoteGenerator:
    """
    Iterator class that generates untimed sequence of notes to feed into
    the step sequencer
    """
    def __init__(self, notecount=None, **args):
        self._history = []
        self.count = notecount

    def __iter__(self):
        return self

    def __next__(self):
        if self.count == 0:
            return None
        if self.count != None:
            self.count -= 1
        note = self._generate_note()
        self._history.append(note)
        return note
        
    def _generate_note(self):
        return Note('C3')

    @classmethod
    def from_json(cls, json):
        return cls(*json)

class Arpeggiator(NoteGenerator):
    """
    Generate a repeating sequence of notes.
    """
    def __init__(self, notelist, **args):
        super().__init__(**args)
        self._notelist = []
        for note in notelist:
            if type(note) == type(""):
                note = Note(note)
            self._notelist.append(note)
                
        
        self.idx = 0

    def _generate_note(self):
        note = self._notelist[self.idx]
        self.idx += 1
        if self.idx >= len(self._notelist):
            self.idx = 0
        return note

class MarkovSequence(NoteGenerator):
    """
    Generate a sequence based on a
    Markov process
    """

    def __init__(self, nmap ,transition_map, **args):
        """
        """
        super().__init__(**args)
        self.nodes = {}
        self.start_node = None
        self.markov = MarkovProcess()
        for k,v in nmap.items():
            n = MarkovNode()
            n.label=n
            n.payload=Note(v)
            self.nodes[k] = n
        for from_node, to_node, w in transition_map:
            f = self.nodes[from_node]
            if self.start_node == None:
                self.start_node = f
            t = self.nodes[to_node]
            f.add_transition(t, w)

        self.markov.current_node = self.start_node

    def _generate_note(self):
        n = self.markov.step()
        return n.payload

        
