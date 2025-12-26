

import random,time

# Keeping this in order is important
NAMED_RANDOMS = [
    "default",
    "generators",
    "modulators",
    "markov"
]

SEEDMASTER = None

def getSeedMaster(seed=None):
    global SEEDMASTER
    if SEEDMASTER == None:
        SEEDMASTER = SeedMaster(seed)
    return SEEDMASTER

class SeedMaster:
    def __init__(self, seed=None):
        named_randoms = NAMED_RANDOMS
        if seed == None:
            self.seed = int(time.time()) + 0x71e00000
        self.master_random = random.Random(self.seed)
        self.rng_map = {}
        for name in NAMED_RANDOMS:
            self.rng_map[name] = random.Random(self.master_random.random())
        random.setstate(self.rng_map['default'].getstate())

    def get(self, name):
        return self.rng_map[name]
