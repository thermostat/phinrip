import pytest
import sys, os

sys.path.append(os.getcwd())

SCALE = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5']

import phinrip.step_sequence as psseq
import phinrip.note_generator as pgen
import phinrip.note_modulator as pmod
import phinrip.note as pnote

def sample_sequence_scale():
    file = psseq.StepSequenceFile()
    for pitch in SCALE:
        noteval = pnote.NoteName.to_midi(pitch)
        step = psseq.StepEvent.note(noteval)
        file.add_step(step)
    file.save('sample_sequence_scale.mid')

def sample_arp():
    notes = [ pnote.Note(x) for x in ['A2', 'C3', 'E3', 'A3'] ]
    gen = psseq.GenerateStepSequencer(pgen.Arpeggiator(notes), [])
    file = gen.generate_steps(128)
    file.save('sample_arp.mid')


def sample_composed():
    notes = [ pnote.Note(x) for x in ['A2', 'C3', 'E3', 'A3'] ]
    ngen = pgen.Arpeggiator(notes)
    nmod = pmod.ModCompose([pmod.Transpose(-12)], [pmod.RndPred()])
    gen = psseq.GenerateStepSequencer(ngen, [nmod])
    file = gen.generate_steps(128)
    file.save('sample_composed.mid')
    

if __name__ == '__main__':
    sample_sequence_scale()
    sample_arp()
    sample_composed()
