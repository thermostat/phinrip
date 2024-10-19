

import mido
import time
import random

msg_on = mido.Message('note_on', note=60)

msg_off = mido.Message('note_off', note=60)

print(mido.get_output_names())
print(mido.get_input_names())
port = mido.open_output("loopMIDI Port 1")
inport = mido.open_input("loopMIDI Port 3 1")

cnt_msg = ''

#  24 pulses per quarter note.

pulse_per_q = 24
pulse_per_bar = 24 * 4

pulse_count = 0
bar_count = 0


def bar_to_trackscene(bar):
    t = random.randint(0,7)
    s = random.randint(0,7)
    return t, s

def trackscene_to_midival(ts):
    val = ts[0] * 8
    val = val + ts[1]
    val = val + 10
    return val

send_new_clip = True

while True:
    midimsg = inport.receive()
    #print(midimsg)
    pulse_count += 1
    if pulse_count == pulse_per_bar:
        bar_count += 1
        send_new_clip = True
        print(f"Bar {bar_count}")
        pulse_count = 0

    if pulse_count > (pulse_per_q*3):
        t,s = bar_to_trackscene(bar_count)
        val = trackscene_to_midival((t,s))
        if send_new_clip:
            print(f"[bar {bar_count}: sending track {t} scene {s} (midival={val})")
            msg = mido.Message('note_on', note=val)
            port.send(msg)
            send_new_clip = False


# while cnt_msg != 'quit':
#     cnt_msg = input("> ").strip()
#     port.send(msg_on)
#     time.sleep(1)
#     port.send(msg_off)
    



