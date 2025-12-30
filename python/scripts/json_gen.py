

NOTES_3_ALL = [
    "C3", "Db3", "D3",
    "Eb3", "E3", "F3",
    "Gb3", "G3", "Ab3",
    "A3", "Bb3", "B3"
    ]

def make_nmap(note_list):
    "Make a name map"
    result = {}
    for note in note_list:
        result["note_"+note] = note
    return result

def make_transitions(note_list):
    result = []
    # ex C3:
    x = [
        4, # C3, self
        0,
        16,   # second
        8,    # m3
        2,     # M3
        32,
        0,
        32,
        2,
        8, # M6
        16,
        0
        ]
    for src in note_list:
        for i,target in enumerate(note_list):
            if x[i] > 0:
                result.append(["note_"+src, "note_"+target, x[i]])
        v = x.pop()
        x.insert(0, v)
    return result

def sequence_gen_fourths():
    json = {}
    sg = []
    json['sequence-gen'] = sg
    ms = {}
    ms['cls'] = "MarkovSequence"
    ms['nmap'] = make_nmap(NOTES_3_ALL)
    ms['transition_map'] = make_transitions(NOTES_3_ALL)
    ms['notecount'] = 256
    sg.append(ms)
    return json

if __name__ == '__main__':
    import json
    fd = open('fourths.json', 'w')
    json.dump(sequence_gen_fourths(), fd, indent=2)
