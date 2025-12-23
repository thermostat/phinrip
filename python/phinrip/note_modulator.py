

from .note import Note
from .phrandom import getSeedMaster

class NoteModulator:

    def __init__(self):
        pass

    def modulate(self, note):
        if self._should_modulate(note):
            note = self._do_modulate(note)
        return note

    def _should_modulate(self, note):
        return False

    def _do_modulate(self, note):
        return note

class ModCompose(NoteModulator):

    def __init__(self, mod_lst, pred_lst):
        self._mod_lst = mod_lst
        self._pred_lst = pred_lst

    def _should_modulate(self, note):
        res = all([pred._should_modulate(note) for pred in self._pred_lst])
        return res

    def _do_modulate(self, note):
        for mod in self._mod_lst:
            note = mod._do_modulate(note)
        return note

class RndPred(NoteModulator):
    def __init__(self, prob=.5):
        self._rng = getSeedMaster().get("modulators")
        self._prob = prob

    def _should_modulate(self, note):
        if self._rng.random() > self._prob:
            return True
        return False
    

class Transpose:
    def __init__(self, semi):
        self._semi = semi

    def _should_modulate(self, note):
        return True

    def _do_modulate(self, note):
        return note.transpose(self._semi)
    

