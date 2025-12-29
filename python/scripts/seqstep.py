#!/usr/bin/env python3
"""Command-line interface for building step sequences from JSON specs."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from phinrip.step_sequence import GenerateStepSequencer, sequence_gen_json
from phinrip.phrandom import getSeedMaster


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a MIDI file from a JSON step sequence definition."
    )
    parser.add_argument(
        "config",
        type=Path,
        help="Path to the JSON configuration describing the sequence.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Destination MIDI file (defaults to CONFIG with .mid extension).",
    )
    parser.add_argument(
        "-s",
        "--steps",
        type=int,
        help="Override number of steps to generate (defaults to sum of notecounts).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        help="Optional phrandom seed to reproduce a sequence exactly.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose logging.",
    )
    return parser.parse_args()


def load_config(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def infer_step_count(config: dict) -> int:
    total = 0
    for entry in config.get("sequence-gen", []):
        total += int(entry.get("notecount", 0) or 0)
    return total


def resolve_output_path(config_path: Path, override: Path | None) -> Path:
    if override:
        return override
    return config_path.with_suffix(".mid")


def main() -> None:
    args = parse_args()
    config_path = args.config.expanduser()
    if not config_path.exists():
        raise SystemExit(f"Configuration file not found: {config_path}")

    config = load_config(config_path)

    # Initialize phrandom before building generators so metadata captures the seed.
    if args.seed is not None:
        getSeedMaster(args.seed)
    else:
        getSeedMaster()

    sequencer: GenerateStepSequencer = sequence_gen_json(config)

    steps = args.steps or infer_step_count(config)
    if steps <= 0:
        raise SystemExit(
            "Unable to determine the number of steps. "
            "Specify --steps or provide notecount values in JSON."
        )

    if args.verbose:
        print(
            f"[seqstep] Generating {steps} steps from {config_path} (seed={getSeedMaster().seed})",
            file=sys.stderr,
        )

    step_sequence = sequencer.generate_steps(steps)
    output_path = resolve_output_path(config_path, args.output)
    saved_path = step_sequence.save(output_path)

    if args.verbose:
        print(f"[seqstep] Wrote MIDI file to {saved_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
