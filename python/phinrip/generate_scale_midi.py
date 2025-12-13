"""Utility script that writes an eighth-note C-major scale to a MIDI file."""

from __future__ import annotations

import argparse
from pathlib import Path

from mido import Message, MetaMessage, MidiFile, MidiTrack, bpm2tempo

TICKS_PER_BEAT = 480
TEMPO_BPM = 120
NOTE_LENGTH = TICKS_PER_BEAT // 2  # eighth notes


def create_scale_track() -> MidiTrack:
    """Build a single track that plays a C-major scale up and down."""
    track = MidiTrack()
    track.append(
        MetaMessage(
            "time_signature",
            numerator=4,
            denominator=4,
            clocks_per_click=24,
            notated_32nd_notes_per_beat=8,
            time=0,
        )
    )
    track.append(MetaMessage("set_tempo", tempo=bpm2tempo(TEMPO_BPM), time=0))

    ascending = [60, 62, 64, 65, 67, 69, 71, 72]
    descending = ascending[-2::-1]  # exclude the topmost note to avoid repeating it
    scale = ascending + descending

    for note in scale:
        track.append(Message("note_on", note=note, velocity=96, time=0))
        track.append(Message("note_off", note=note, velocity=0, time=NOTE_LENGTH))

    track.append(MetaMessage("end_of_track", time=0))
    return track


def build_file(output_path: Path) -> Path:
    """Create the MIDI file and write it to disk."""
    mid = MidiFile(type=0, ticks_per_beat=TICKS_PER_BEAT)
    mid.tracks.append(create_scale_track())
    mid.save(output_path.as_posix())
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write a 1-track SMF with an eighth-note C-major scale."
    )
    parser.add_argument(
        "--output",
        default=Path(__file__).with_name("c_major_scale.mid"),
        type=Path,
        help="Destination MIDI file (default: %(default)s)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_path = build_file(args.output)
    print(f"Wrote C-major scale to {output_path}")


if __name__ == "__main__":
    main()
