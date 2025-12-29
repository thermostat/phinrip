"""Fixed-step MIDI file helper built on top of mido."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from pathlib import Path
from typing import List, Optional

from mido import Message, MetaMessage, MidiFile, MidiTrack, bpm2tempo

from .note import Note
from .note_generator import NoteGenerator, generator_map
from .phrandom import getSeedMaster


def sequence_gen_json(parsed_json):
    gm = generator_map()
    seq_list = parsed_json['sequence-gen']
    seq_steplen = StepLength[parsed_json.get('sequence-step-len', 'EIGHTH')]
    objs = []
    for seq_def in seq_list:
        seq_cls = gm[seq_def['cls']]
        seq_obj = seq_cls(**seq_def)
        objs.append(seq_obj)
    step_seq = GenerateStepSequencer(objs, [], step_length=seq_steplen)
    return step_seq

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

    def add_note(self, note: Note) -> None:
        self.add_step(StepEvent.note(note.pitch_value(), velocity=note.velocity()))

    def add_note_value(self, note: int, velocity: int = 96, channel: int = 0) -> None:
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
        track.append(MetaMessage("text", text=f"random_seed = {getSeedMaster().seed}", time=0))
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


class GenerateStepSequencer:

    def __init__(self, generator, mods, **ssargs):
        self._stepseq = StepSequenceFile(**ssargs)
        if type(generator) != type([]):
            self._generators = []
            self._current_generator = generator
        else:
            self._generators = generator
            self._generators.reverse()
            self._current_generator = self._generators.pop()
        self._mods = mods

    def generate_steps(self, nbr_steps):
        for i in range(nbr_steps):
            note = next(self._current_generator)
            if note == None and len(self._generators):
                self._current_generator = self._generators.pop()
                note = next(self._current_generator)
            if note == None:
                return self._stepseq
            for mod in self._mods:
                note = mod.modulate(note)
            self._stepseq.add_note(note)
        return self._stepseq



