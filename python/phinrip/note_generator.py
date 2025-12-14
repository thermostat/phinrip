
import itertools

"""
Generate notes
"""

def take(n, iterable):
    """Return first n items of the iterable as a list."""
    return list(itertools.islice(iterable, n))

from .note import Note

class NoteGenerator:

    def __init__(self):
        self._history = []

    def __iter__(self):
        return self

    def __next__(self):
        note = self._generate_note()
        self._history.append(note)
        return note
        
    def _generate_note(self):
        return Note('C3')


class Arpeggiator(NoteGenerator):

    def __init__(self, notelist):
        super().__init__()
        self._notelist = notelist
        self.idx = 0

    def _generate_note(self):
        note = self._notelist[self.idx]
        self.idx += 1
        if self.idx >= len(self._notelist):
            self.idx = 0
        return note
