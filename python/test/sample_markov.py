


import pytest
import sys, os

sys.path.append(os.getcwd())

import phinrip.markov as pmark

def sample_markov():
    a = pmark.MarkovNode()
    a.label = 'a'
    b = pmark.MarkovNode()
    b.label = 'b'
    c = pmark.MarkovNode()
    c.label = 'c'

    a.add_transition(b, 6)
    a.add_transition(c, 4)
    b.add_transition(c, 8)
    b.add_transition(a, 2)
    c.add_transition(a, 9)
    c.add_transition(b, 1)

    proc = pmark.MarkovProcess()
    proc.nodes = [a,b,c]
    proc.current_node = a

    labels = [a.label]
    for _ in range(20):
        n = proc.step()
        labels.append(n.label)
    print(",".join(labels))

if __name__ == '__main__':
    sample_markov()
