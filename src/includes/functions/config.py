
midimix_midi = "midimix"

behringer    = "behringer"

sd90_port_a  = "sd90_port_a"
sd90_port_b  = "sd90_port_b"
sd90_midi_1  = "sd90_midi_1"
sd90_midi_2  = "sd90_midi_2"

mpk_port_a   = "mpk_port_a"
mpk_port_b   = "mpk_port_b"
mpk_midi     = "mpk_midi"
mpk_remote   = "mpk_remote"

gt1000_midi_1 = "gt1000_midi_1"
gt1000_midi_2 = "gt1000_midi_2"
numark_midi_0 = "numark_midi_0"
mixxx_midi_0  = "mixxx_midi_0"

um2_midi_1 = "um2_midi_1"
um2_midi_2 = "um2_midi_2"

config(

    initial_scene = 1,
    backend = 'alsa',
    client_name = 'mididings',

    out_ports = [
        (midimix_midi, ".*MIDI Mix MIDI 1.*",),
        (sd90_port_a,  '.*SD-90 Part A.*'),
        (sd90_port_b,  '.*SD-90 Part B.*'),
        (sd90_midi_1,  '.*SD-90 MIDI 1.*',),
        (sd90_midi_2,  '.*SD-90 MIDI 2.*',),
        (behringer,    '.*UMC204HD 192k MIDI 1.*'),
        (mpk_port_a,   '.*MPK249 Port A.*',),
        (mpk_port_b,   '.*MPK249 Port B.*',),
        (mpk_midi,     '.*MPK249 MIDI.*',),
        (mpk_remote,   '.*MPK249 Remote.*',),
        (gt1000_midi_1,'.*GT-1000 MIDI 1.*',),
        (gt1000_midi_2,'.*GT-1000 MIDI 2.*',),
        (mixxx_midi_0,'.*VirMIDI.*-0$',),
        (numark_midi_0,'.*Party Mix MKII MIDI 1.*',),
        (um2_midi_1,'.*UM-2 MIDI 1.*',),
        (um2_midi_2,'.*UM-2 MIDI 2.*',),
    ],

    in_ports = [
        (midimix_midi, ".*MIDI Mix MIDI 1.*",),
        (sd90_port_a,  '.*SD-90 Part A.*'),
        (sd90_port_b,  '.*SD-90 Part B.*'),
        (sd90_midi_1,  '.*SD-90 MIDI 1.*',),
        (sd90_midi_2,  '.*SD-90 MIDI 2.*',),
        (behringer,    '.*UMC204HD 192k MIDI 1.*'),
        (mpk_port_a,   '.*MPK249 Port A.*',),
        (mpk_port_b,   '.*MPK249 Port B.*',),
        (mpk_midi,     '.*MPK249 MIDI.*',),
        (mpk_remote,   '.*MPK249 Remote.*',),
        (gt1000_midi_1,'.*GT-1000 MIDI 1.*',),
        (gt1000_midi_2,'.*GT-1000 MIDI 2.*',),
        (mixxx_midi_0,'.*VirMIDI.*-0$',),
        (numark_midi_0,'.*Party Mix MKII MIDI 1.*',),
        (um2_midi_1,'.*UM-2 MIDI 1.*',),
    ],
)