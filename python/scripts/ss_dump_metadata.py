
import mido



def main(fname):
    midi_file = mido.MidiFile(fname)
    print(f"## Metadata - {fname} ##")
    for msg in midi_file.tracks[0]:
        if msg.is_meta:
            d = msg.dict()
            if d['type'] == 'track_name':
                print(f"  track name = {d['name']}")
            elif d['type'] == 'text':
                print(f"  {d['text']}")
            elif d['type'] == 'time_signature':
                print(f"  time signature = {d['numerator']} / {d['denominator']}")
            elif d['type'] == 'set_tempo':
                tempo = 60000000 // d['tempo']
                print(f"  tempo = {tempo} bpm")
            
            
    
                  

if __name__ == '__main__':
    import sys
    main(sys.argv[1])
