
import random


def getMkRand():
    return random.Random()


class MarkovNode:
    """
    Markov node with weighted transitions
    """
    def __init__(self):
        self.transitions = []
        self.wsum = 0.0
        self.rand = getMkRand()
        self.payload = None
        self.label = None

    def _freeze(self):
        self.wsum = 0.0
        for node, weight in self.transitions:
            self.wsum += weight
        

    def add_transition(self, node, weight):
        self.transitions.append((node, weight))
        self._freeze()
    
    def next_node(self):
        val = self.rand.random()
        test_val = val * self.wsum
        choice = None
        inc = 0.0
        for node, weight in self.transitions:
            inc += weight
            if inc > test_val:
                choice = node
                break
        return choice
    

class MarkovProcess:
    def __init__(self):
        self.nodes = []
        self._run_history = []
        self.current_node = None

    def add_node(self, node):
        self.nodes.append(node)

    def step(self):
        self._run_history.append(self.current_node)        
        self.current_node = self.current_node.next_node()
        return self.current_node

    def run(step_count):
        for _ in range(step_count):
            self.step()
