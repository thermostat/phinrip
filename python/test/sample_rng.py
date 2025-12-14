import pytest
import sys, os

sys.path.append(os.getcwd())

SCALE = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5']

import phinrip.phrandom as phr

def print_randoms():
    print("Object 1")
    print("Gen")
    ms = phr.SeedMaster(42)
    gen_rng = ms.get('generators')
    print(gen_rng.random())
    print(gen_rng.random())
    print(gen_rng.random())
    print("Mod")    
    mod_rng = ms.get('modulators')
    print(mod_rng.random())
    print(mod_rng.random())
    print(mod_rng.random())

    print("Object 2")
    ms = phr.SeedMaster(42)
    print("Mod")    
    mod_rng = ms.get('modulators')
    print(mod_rng.random())
    print(mod_rng.random())
    print(mod_rng.random())
    print("Gen")
    gen_rng = ms.get('generators')
    print(gen_rng.random())
    print(gen_rng.random())
    print(gen_rng.random())

if __name__ == '__main__':
    print_randoms()
