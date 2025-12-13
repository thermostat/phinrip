"""Fixed-step MIDI file helper built on top of mido."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from pathlib import Path
from typing import List, Optional

from mido import Message, MetaMessage, MidiFile, MidiTrack, bpm2tempo


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


class StepLength(Enum):
    """Enumeration of supported fixed step lengths."""

    WHOLE = Fraction(4, 1)
    HALF = Fraction(2, 1)
    QUARTER = Fraction(1, 1)
    EIGHTH = Fraction(1, 2)
    SIXTEENTH = Fraction(1, 4)

    def ticks(self, ticks_per_quarter: int) -> int:
        ticks = int(self.value * ticks_per_quarter)
        if ticks <= 0:
            raise ValueError("Step length must produce a positive tick count.")
        return ticks


@dataclass(frozen=True)
class StepEvent:
    """Represents a single fixed-length step which is either a note or a rest."""

    note: Optional[int]
    velocity: int = 96
    channel: int = 0

    @classmethod
    def note(cls, note: int, velocity: int = 96, channel: int = 0) -> "StepEvent":
        return cls(note=note, velocity=velocity, channel=channel)

    @classmethod
    def from_name(
        cls, note_name: str, velocity: int = 96, channel: int = 0
    ) -> "StepEvent":
        """Create a note step using a human-readable note name (e.g., C#4)."""
        note_value = NoteName.to_midi(note_name)
        return cls.note(note_value, velocity=velocity, channel=channel)

    @classmethod
    def rest(cls) -> "StepEvent":
        return cls(note=None, velocity=0, channel=0)

    def is_rest(self) -> bool:
        return self.note is None


class StepSequenceFile:
    """
    Convenience wrapper that emits a single-track Standard MIDI File made of
    fixed-length steps (eighth-notes by default).
    """

    _SUPPORTED_SIGNATURES = {(4, 4), (6, 8)}
    _TICKS_PER_QUARTER = 480

    def __init__(
        self,
        *,
        bpm: int = 120,
        time_signature: tuple[int, int] = (4, 4),
        step_length: StepLength = StepLength.EIGHTH,
        track_name: str = "Step Sequence",
    ) -> None:
        if time_signature not in self._SUPPORTED_SIGNATURES:
            raise ValueError(
                f"Unsupported time signature {time_signature}; "
                "supported signatures are 4/4 and 6/8."
            )
        self._ticks_per_quarter = self._TICKS_PER_QUARTER
        self._bpm = bpm
        self._time_signature = time_signature
        self._step_length = step_length
        self._step_ticks = step_length.ticks(self._ticks_per_quarter)
        self._track_name = track_name
        self._steps: List[StepEvent] = []
        self._mid = MidiFile(type=0, ticks_per_beat=self._ticks_per_quarter)

    def add_step(self, event: StepEvent) -> None:
        """Append a step (note or rest) to the backing sequence."""
        self._steps.append(event)

    def add_note(self, note: int, velocity: int = 96, channel: int = 0) -> None:
        """Convenience helper for adding note steps."""
        self.add_step(StepEvent.note(note, velocity=velocity, channel=channel))

    def add_note_name(
        self, note_name: str, velocity: int = 96, channel: int = 0
    ) -> None:
        """Add a step using a human-readable note name (e.g., 'C4')."""
        self.add_step(
            StepEvent.from_name(note_name, velocity=velocity, channel=channel)
        )

    def add_rest(self) -> None:
        """Convenience helper for adding rest steps."""
        self.add_step(StepEvent.rest())

    def _build_track(self) -> MidiTrack:
        track = MidiTrack()
        track.append(MetaMessage("track_name", name=self._track_name, time=0))
        numerator, denominator = self._time_signature
        track.append(
            MetaMessage(
                "time_signature",
                numerator=numerator,
                denominator=denominator,
                clocks_per_click=24,
                notated_32nd_notes_per_beat=8,
                time=0,
            )
        )
        track.append(MetaMessage("set_tempo", tempo=bpm2tempo(self._bpm), time=0))

        accumulated_rest = 0
        for event in self._steps:
            if event.is_rest():
                accumulated_rest += self._step_ticks
                continue
            track.append(
                Message(
                    "note_on",
                    note=event.note,
                    velocity=event.velocity,
                    channel=event.channel,
                    time=accumulated_rest,
                )
            )
            accumulated_rest = 0
            track.append(
                Message(
                    "note_off",
                    note=event.note,
                    velocity=0,
                    channel=event.channel,
                    time=self._step_ticks,
                )
            )

        track.append(MetaMessage("end_of_track", time=accumulated_rest))
        return track

    def save(self, path: Path | str) -> Path:
        """Finalize the track and persist the Standard MIDI File."""
        track = self._build_track()
        self._mid.tracks = [track]
        destination = Path(path)
        self._mid.save(destination.as_posix())
        return destination

    def to_midifile(self) -> MidiFile:
        """Return an in-memory MidiFile representation of the sequence."""
        track = self._build_track()
        self._mid.tracks = [track]
        return self._mid
