#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" """
""" This is an OSC forwarder between mididings and a remote """
""" Since mididings notify only to localhost (i think) """
""" Server receives messages from mididings and Client forward the message to a remote """

# import argparse
# import random
# import time
import sys
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
# from pythonosc import osc_message_builder
from pythonosc import udp_client


class DeviceInfo:
    def __init__(self, _ip, _port):
        self.ip = _ip
        self.port = _port


class OscForwarder:
    def __init__(self, _local, _remote):
        self.local = _local
        self.remote = _remote

        # Dispatcher
        self.dispatcher = Dispatcher()

        # mididings
        self.dispatcher.map("/mididings/*", self.mididings_handler)
        # self.dispatcher.map("/futur/*", futur_handler)

        # Fallback
        self.dispatcher.set_default_handler(self.default_handler)

        # Server listen the client
        self.server = BlockingOSCUDPServer((self.local.ip, self.local.port), self.dispatcher)

        # Client forward to remote
        self.client = udp_client.SimpleUDPClient(self.remote.ip, self.remote.port)

    def execute(self):
        self.server.serve_forever()  # Blocks forever

    # Occurs on osc message from mididings, client forward message to remote server
    def mididings_handler(self, address, *args):
        print((address + ":" + "{}".format(args)))
        # self.client.send_message(address, list(args))
        self.client.send_message(address, "{}".format(args))

    def default_handler(self, address, *args):
        print(("DEFAULT " + address + ":" + "{}".format(args)))


def main(args=None):
    # Listen mididings
    local = DeviceInfo("127.0.0.1", 56419)

    # Forward to remote address/port
    remote = DeviceInfo("192.168.2.25", 55555)

    forwarder = OscForwarder(local, remote)
    forwarder.execute()


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]) or 0)
