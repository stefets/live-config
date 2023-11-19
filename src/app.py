#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import argh
import json
import alsaaudio
from mako.template import Template

def configure_asoundrc():   
    audio_devices = alsa["asoundrc"]
    asoundrc = Template(filename=alsa["template"])
    for device_number, card_name in enumerate(alsaaudio.cards()):
        audio_devices[card_name] = f"hw:{device_number},0"
    with open(os.path.expanduser('~') + "/.asoundrc", "w") as FILE:
        FILE.write(asoundrc.render(**audio_devices))

def build(key, scene=None):

    template = Template(filename=content["template"])

    body_content = content[key]
    scene_content = content["scene_dir"] + scene if scene else content["scene_dir"] + content["default_scene"] 
    control_content = content["control"]

    return template.render(
        body_content=body_content, 
        scene_content=scene_content,
        control_content=control_content,
        debug=False
    )


def complete(scene=None):
    source = build("complete", scene)
    print(source)


def minimal(scene=None):
    source = build("minimal", scene)
    print(source)


'''
    Main
'''
global alsa
global context
with open('app.json') as file:
    config = json.load(file)
alsa = config["alsa"]
content = config["content"]

parser = argh.ArghParser()
parser.add_commands([complete, minimal])

configure_asoundrc()

if __name__ == '__main__':
    parser.dispatch()
