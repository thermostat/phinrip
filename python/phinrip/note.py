


class NoteName:
    """Utility helpers for converting textual note names (C#4) into MIDI numbers."""

    _NOTE_OFFSETS = {
        "C": 0,
        "D": 2,
        "E": 4,
        "F": 5,
        "G": 7,
        "A": 9,
        "B": 11,
    }

    @classmethod
    def to_midi(cls, name: str) -> int:
        """
        Convert a note name like ``C#4`` or ``Eb3`` into its MIDI note number.

        Octaves follow the standard where C4 == MIDI 60.
        """
        if len(name) < 2:
            raise ValueError(f"Invalid note name '{name}'.")
        name = name.strip()
        letter = name[0].upper()
        if letter not in cls._NOTE_OFFSETS:
            raise ValueError(f"Unknown note letter '{letter}' in '{name}'.")

        accidental_idx = 1
        offset_adjust = 0
        if len(name) > 2 and name[1] in ("#", "b"):
            accidental = name[1]
            offset_adjust = 1 if accidental == "#" else -1
            accidental_idx = 2
        elif len(name) > 1 and name[1] in ("#", "b"):
            accidental = name[1]
            offset_adjust = 1 if accidental == "#" else -1
            accidental_idx = 2

        octave_str = name[accidental_idx:]
        if not octave_str or not octave_str.lstrip("-").isdigit():
            raise ValueError(f"Invalid octave in note name '{name}'.")
        octave = int(octave_str)

        midi_number = (octave + 1) * 12 + cls._NOTE_OFFSETS[letter] + offset_adjust
        if not 0 <= midi_number <= 127:
            raise ValueError(f"Note '{name}' resolves outside MIDI range 0-127.")
        return midi_number



class Note:

    def __init__(self, pitch='C3', velocity=96, length=None):
        self._pitch = pitch
        self._pitch_val = NoteName.to_midi(pitch)
        self._velocity = velocity
        self._length = length

    def __repr__(self):
        return f"Note('{self._pitch}', {self._velocity})"

    def pitch_value(self):
        return self._pitch_val

    def velocity(self):
        return self._velocity
