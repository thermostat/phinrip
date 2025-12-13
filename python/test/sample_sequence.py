import pytest
import sys, os

sys.path.append(os.getcwd())

SCALE = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5']

import phinrip.step_sequence as sseq

def sequence_scale():
    file = sseq.StepSequenceFile()
    for pitch in SCALE:
        noteval = sseq.NoteName.to_midi(pitch)
        step = sseq.StepEvent.note(noteval)
        file.add_step(step)
    file.save('sample_sequence_scale.mid')

if __name__ == '__main__':
    sequence_scale()
