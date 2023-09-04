#!/usr/bin/env python
#-*- coding: utf-8 -*-

import alsaaudio
from mako.template import Template

# Configure ALSA
card_info = {
	"U192k" : "",
	"SD90" : "",
	"GT10B" : "",
}
alsa = Template(filename='asoundrc.mako')
for device_number, card_name in enumerate(alsaaudio.cards()):
    card_info[card_name] = f"hw:{device_number},0"
print(alsa.render(**card_info))
	

# Configure
template = Template(filename='template.mako')
body_definition = [
        "functions/common.py",
        "functions/soundcraft.py",
        'patches/000-filters.py', 
        "patches/001-sd90.py",
        "patches/002-gt10b.py",
        "patches/003-hd500.py",
        "patches/004-soundcraft.py",
        "patches/800-common.py",
    ]

scene_definition = "scenes/default.py"
control_definition = "patches/900-controls.py"
memorize = ".hook.memorize_scene"

ports = {
    "midimix" : "24:0"
}

# Generate a mididings script
source = template.render(
    **ports, 
    body_definition=body_definition, 
    scene_definition=scene_definition,
    control_definition=control_definition,
    memorize=memorize,
    debug=False
)

#print(source)
