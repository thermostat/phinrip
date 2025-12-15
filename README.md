# Phinrip

Non-repeating music control


## Step Sequence Generation

The step sequence generator provides tools generate and module a
sequence.

* Library
  * StepSequence
  * NoteGenerator
    * Arpeggiator
    * MarkovProc (planned)
  * NoteModulator
    * ModCompose
    * RndPred
    * Transpose
    


<details>

## Proof of concept

Setup components:

* Windows (11 Home)
* Bitwig Studio 5.2.4 (trial)
* Python 3.10.8 (+ frozen.txt dependencies)
* loopMidi v 1.0.16

Bitwig project, control_test, has clip arranger running 8 tracks with
randomly selected synth instruments, each track has 8 scenes one bar
for each scene, with a quarter note playing in the bar on a simple
acsending scale.

The simple_controller.control.js is installed as a software controller
with sync messages turned on. mido_test.py is run, waits for syncs to
start, then triggers a random clip each bar.

</details>