import os
import json

"""
This plugin allows communication with mpv player through socket.
"""

class MpvClient():
    def __init__(self, address: str):
        if address is None:
            raise ValueError("IPC socket path must be provided")
        
        self.socket = socket.socket(socket.AF_UNIX)
        self.socket.connect(address)

    def command(self, *args):
        payload = {
            "command": list(args)
        }

        self.socket.sendall(
            (json.dumps(payload) + "\n").encode("utf-8")
        )
        
    def set_property(self, property_name, value):
        self.command("set_property", property_name, value)
        
    def get_property(self, property_name):
        payload = {
            "command": ["get_property", property_name]
        }

        self.socket.sendall(
            (json.dumps(payload) + "\n").encode("utf-8")
        )

        response = self.socket.recv(1024)
        response_data = json.loads(response.decode("utf-8"))
        return response_data.get("data")

    def load(self, filename):
        self.command("loadfile", filename)

    def pause(self):
        self.set_property("pause", True)

    def unpause(self):
        self.set_property("pause", False)
        
    def toggle_pause(self):
        self.set_property("pause", not self.get_property("pause"))
        
    def mute(self):
        self.set_property("mute", True)
        
    def unmute(self):
        self.set_property("mute", False)

    def toggle_mute(self):
        self.set_property("mute", not self.get_property("mute"))

    def forward(self):
        self.on_jump(self.jump_offset)

    def rewind(self):
        self.on_jump(-self.jump_offset)

    def on_jump(self, offset):
        self.command("seek", offset, "relative")

    def set_volume(self, value):
        self.set_property("volume", value)
