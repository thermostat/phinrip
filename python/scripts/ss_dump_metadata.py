
import mido
import math

_TICKS_PER_QUARTER = 480

def main(fname):
    midi_file = mido.MidiFile(fname)
    print(f"## Metadata - {fname} ##")
    time_sum = 0
    for msg in midi_file.tracks[0]:
        d = msg.dict()
        time_sum += d['time']
        if msg.is_meta:
            if d['type'] == 'track_name':
                print(f"  track name = {d['name']}")
            elif d['type'] == 'text':
                print(f"  {d['text']}")
            elif d['type'] == 'time_signature':
                ts_denom = d['denominator']
                ts_num = d['numerator']
                print(f"  time signature = {d['numerator']} / {d['denominator']}")
            elif d['type'] == 'set_tempo':
                tempo = 60000000 // d['tempo']
                print(f"  tempo = {tempo} bpm")
    quarters = time_sum / _TICKS_PER_QUARTER
    if ts_denom == 4 and ts_num == 4:
        print(f"  bars = {math.ceil(quarters/4)}")
    
                  

if __name__ == '__main__':
    import sys
    main(sys.argv[1])
