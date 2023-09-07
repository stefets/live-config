#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys
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

def build(kind="complete"):
    content = config["content"]
    
    template = Template(filename=content["template"])
    
    body_content = content[kind]
    memorize = content["memorize"]
    scene_content = content["scene"]
    control_content = content["control"]

    return template.render(
        **configure_sequencers(), 
        body_content=body_content, 
        scene_content=scene_content,
        control_content=control_content,
        memorize=memorize,
        debug=False
    )


def complete():
    source = build()
    print(source)


def minimal():
    source = build("minimal")
    print(source)


'''
    Main
'''
global alsa
global content
with open('app.json') as FILE:
    config = json.load(FILE)
alsa = config["alsa"]
content = config["content"]

parser = argh.ArghParser()
parser.add_commands([complete, minimal])

configure_asoundrc()

if __name__ == '__main__':
    parser.dispatch()
