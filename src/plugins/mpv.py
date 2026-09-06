import os
import json
import socket

"""
This plugin allows communication with mpv player through socket.
"""

class MpvClient():
    def __init__(self, address: str):
        if address is None:
            raise ValueError("IPC socket path must be provided")
        
        self.socket = socket.socket(socket.AF_UNIX)
        self.socket.connect(address)
        
        self.request_id = 0
        self._buffer = b""

    def command(self, *args):
        self.request_id += 1
        payload = {
            "command": list(args),
            "request_id": self.request_id
        }

        self.socket.sendall(
            (json.dumps(payload) + "\n").encode("utf-8")
        )

        return self._read_response(self.request_id)
        
    def set_property(self, property_name, value):
        self.command("set_property", property_name, value)
        
    def get_property(self, property_name):
        response = self.command("get_property", property_name)
        return response.get("data")

    def _read_response(self, request_id):
        while True:

            # On a peut-être déjà plusieurs messages dans le buffer
            while b"\n" in self._buffer:
                line, self._buffer = self._buffer.split(b"\n", 1)

                if not line:
                    continue

                message = json.loads(line.decode("utf-8"))

                print("MPV MESSAGE:", message)

                if message.get("request_id") == request_id:
                    return message

            # Pas encore trouvé notre réponse : on lit davantage
            chunk = self.socket.recv(4096)

            if not chunk:
                raise ConnectionError("MPV IPC socket closed")

            self._buffer += chunk
            
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

    def seek(self, offset):
        self.command("seek", offset, "relative")

    def volume(self, value):
        self.set_property("volume", value)
