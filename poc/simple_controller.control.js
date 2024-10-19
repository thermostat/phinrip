// Simple Controller - Proof of concept


loadAPI(2);

// Force updated usage
host.setShouldFailOnDeprecatedUse(true);

host.defineController("Dan W",
                      "simple_controller",
                      "0.1",
                      "03684d0f-b167-4ebb-bbe8-478705f65b71",
                      "Generic");

// One input for clip launch messages, one output for
// sync ticks
host.defineMidiPorts(1, 1);

// Platform specific - currently using loopback
// and haven't tested across platforms
if (host.platformIsWindows())
{
}
else if (host.platformIsMac())
{
}
else if (host.platformIsLinux())
{
}

// Global for tracks
var dwtracks;


function init() {
    transport = host.createTransport();
    host.getMidiInPort(0).setMidiCallback(onMidi0);
    host.getMidiInPort(0).setSysexCallback(onSysex0);
   
    dwtracks = host.createTrackBank(8, 5, 8)

    println("simple_controller initialized!");
}

// Called when a short MIDI message is received on MIDI input port 0.
function onMidi0(status, data1, data2) {
    if ( !isNoteOn( status ) ) {
        return;
    }

    // Track and scene calculator
    track_nbr = Math.floor((data1-10) / 8)
    scene_nbr = (data1-10) % 8
    if ( track_nbr > 7 || scene_nbr > 7) {
        println("Out of bounds: track " + track_nbr + " scene " + scene_nbr);
        return;
    }
    
    println("Launching track " + track_nbr + " scene " + scene_nbr);
    
    dwtracks.getChannel(track_nbr).clipLauncherSlotBank().launch(scene_nbr);
}

// Called when a MIDI sysex message is received on MIDI input port 0.
function onSysex0(data) {
   // MMC Transport Controls:
   switch (data) {
      case "f07f7f0605f7":
         transport.rewind();
         break;
      case "f07f7f0604f7":
         transport.fastForward();
         break;
      case "f07f7f0601f7":
         transport.stop();
         break;
      case "f07f7f0602f7":
         transport.play();
         break;
      case "f07f7f0606f7":
         transport.record();
         break;
   }
}

function flush() {
   // TODO: Flush any output to your controller here.
}

function exit() {

}
