import sys, os, json

sys.path.append(os.getcwd())

import phinrip.step_sequence as psseq
import phinrip.note_generator as pgen


def sample_json_file():
    fd = open('../data/sequence_gen/markov.json', 'r')
    data = json.load(fd)
    ss = psseq.sequence_gen_json(data)
    midifile = ss.generate_steps(96)
    midifile.save('sample_json.mid')


if __name__ == '__main__':
    sample_json_file()


