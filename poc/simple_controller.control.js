loadAPI(2);

// Remove this if you want to be able to use deprecated methods without causing script to stop.
// This is useful during development.
host.setShouldFailOnDeprecatedUse(true);

host.defineController("Dan W", "simple_controller", "0.1", "03684d0f-b167-4ebb-bbe8-478705f65b71", "Generic");

host.defineMidiPorts(1, 1);

if (host.platformIsWindows())
{
   // TODO: Set the correct names of the ports for auto detection on Windows platform here
   // and uncomment this when port names are correct.
   // host.addDeviceNameBasedDiscoveryPair(["Input Port 0"], ["Output Port 0"]);
}
else if (host.platformIsMac())
{
   // TODO: Set the correct names of the ports for auto detection on Mac OSX platform here
   // and uncomment this when port names are correct.
   // host.addDeviceNameBasedDiscoveryPair(["Input Port 0"], ["Output Port 0"]);
}
else if (host.platformIsLinux())
{
   // TODO: Set the correct names of the ports for auto detection on Linux platform here
   // and uncomment this when port names are correct.
   // host.addDeviceNameBasedDiscoveryPair(["Input Port 0"], ["Output Port 0"]);
}

var dwtracks;

function init() {
    transport = host.createTransport();
    host.getMidiInPort(0).setMidiCallback(onMidi0);
    host.getMidiInPort(0).setSysexCallback(onSysex0);
   
    //host.getMidiOutPort(0).setShouldSendMidiBeatClock(true); 

    dwtracks = host.createTrackBank(8, 5, 8)

   // TODO: Perform further initialization here.
   println("simple_controller initialized!");
}

// Called when a short MIDI message is received on MIDI input port 0.
function onMidi0(status, data1, data2) {
    if ( !isNoteOn( status ) ) {
        return;
    }

    track_nbr = Math.floor((data1-10) / 8)
    scene_nbr = (data1-10) % 8
    if ( track_nbr > 7 || scene_nbr > 7) {
        println("Out of bounds: track " + track_nbr + " scene " + scene_nbr);
        return;
    }
    
    //printMidi(status, data1, data2);
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
