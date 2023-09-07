#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from alsa_midi import SequencerClient, PortType

def main(args=None):
	client = SequencerClient("live")
	ports = client.list_ports(input=True, type=PortType.MIDI_GENERIC | PortType.HARDWARE)
	for port in ports:
		print(f"Name:{port.name} ClientId:{port.client_id} Port:{port.port_id}")

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]) or 0)
