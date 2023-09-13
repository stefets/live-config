#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import argh
import json
import alsaaudio
from mako.template import Template
from alsa_midi import SequencerClient, PortType

def configure_asoundrc():   
    audio_devices = alsa["asoundrc"]
    asoundrc = Template(filename=alsa["template"])
    for device_number, card_name in enumerate(alsaaudio.cards()):
        audio_devices[card_name] = f"hw:{device_number},0"
    with open(os.path.expanduser('~') + "/.asoundrc", "w") as FILE:
        FILE.write(asoundrc.render(**audio_devices))

def configure_sequencers():
    # Map the ALSA client name to a Mako variable ...
    mapping = alsa["mapping"]

    # ... Mako variables that will contains sequencer ids
    sequencers = alsa["sequencers"]

    client = SequencerClient("live")
    ports = client.list_ports(input=True, type=PortType.MIDI_GENERIC | PortType.HARDWARE)
    for port in ports:
        key = mapping[port.name]    # Get the Mako variable name for the template
        sequencers[key] = f"{port.client_id}:{port.port_id}"
    return sequencers

def build(key, scene=None):

    template = Template(filename=content["template"])

    body_content = content[key]
    scene_content = content["scene_dir"] + scene if scene else content["scene_dir"] + content["default_scene"] 
    control_content = content["control"]

    return template.render(
        **configure_sequencers(), 
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
