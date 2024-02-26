#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import argh
import json
import alsaaudio
from mako.template import Template


def make_asoundrc(config) -> None:
    audio_devices = config["asoundrc"]
    asoundrc = Template(filename=config["template"])
    for device_number, card_name in enumerate(alsaaudio.cards()):
        audio_devices[card_name] = f"hw:{device_number},0"
    with open(os.path.expanduser('~') + "/.asoundrc", "w") as FILE:
        FILE.write(asoundrc.render(**audio_devices))

def make_script(config, scene=None) -> str:
    # Generates the mididings script code
    return Template(filename=config["template"]).render(
        scenes  = config["scene_dir"] + scene if scene else config["scene_dir"] + config["default_scene"] ,
        patches = config["patches"]
    )

def main(scene=None):
    with open('config.json') as FILE:
        config = json.load(FILE)

    make_asoundrc(config["alsa"])
    src = make_script(config, scene)

    print(src)


'''
    Entry point
'''

argh.dispatch_command(main)
