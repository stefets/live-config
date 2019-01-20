#!/usr/bin/env python3

# -*- coding: utf-8 -*-

import argparse
import random
import time
import sys

""" """
""" This is an OSC forwarder between mididings and a remote """
""" Since mididings notify only to localhost (i think) """
""" Server receives messages from mididings and Client forward the message to a remote """

from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc import osc_message_builder
from pythonosc import udp_client

class DeviceInfo:
    def __init__(this, _ip, _port):
        this.ip = _ip
        this.port = _port

class OscForwarder:

    def __init__(this, _local, _remote):

        this.local = _local
        this.remote = _remote

		# Dispatcher
        this.dispatcher = Dispatcher()

		# mididings
        this.dispatcher.map("/mididings/*", this.mididings_handler)
        #this.dispatcher.map("/futur/*", futur_handler)

		# Fallback
        this.dispatcher.set_default_handler(this.default_handler)

		# Server listen the client
        this.server = BlockingOSCUDPServer((this.local.ip, this.local.port), this.dispatcher)

		# Client forward to remote
        this.client = udp_client.SimpleUDPClient(this.remote.ip, this.remote.port)

    def execute(this):
        this.server.serve_forever()  # Blocks forever

	# Occurs on osc message from mididings, client forward message to remote server
    def mididings_handler(this, address, *args):
        print(address + ":" + "{}".format(args))
        #this.client.send_message(address, list(args))
        this.client.send_message(address, "{}".format(args))

    def default_handler(this, address, *args):
        print("DEFAULT " + address + ":" + "{}".format(args))

def main(args=None):

    # Listen mididings 
    local = DeviceInfo("127.0.0.1", 56419)

    # Forward to remote address/port
    remote = DeviceInfo( "192.168.2.25", 55555)

    forwarder = OscForwarder(local, remote)
    forwarder.execute()

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]) or 0)
