import os
import json
import socket
import threading
from queue import Queue

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
        self.responses = {}
        
        self._reader_thread = threading.Thread(
            target=self._read_socket,
            daemon=True
        )
        self._reader_thread.start()
        
        self.command("observe_property", 1, "pause")

    def command(self, *args):
        self.request_id += 1
        request_id = self.request_id

        response_queue = Queue()
        self.responses[request_id] = response_queue
            
        payload = {
            "command": list(args),
            "request_id": request_id
        }

        try:
            self.socket.sendall(
                (json.dumps(payload) + "\n").encode("utf-8")
            )
            
            response = response_queue.get()
            return response

        finally:
            del self.responses[request_id]

    def _read_socket(self):
        while True:
            chunk = self.socket.recv(4096)

            if not chunk:
                print("MPV SOCKET CLOSED")
                return

            self._buffer += chunk

            while b"\n" in self._buffer:
                line, self._buffer = self._buffer.split(b"\n", 1)

                if not line:
                    continue

                message = json.loads(line.decode("utf-8"))

                request_id = message.get("request_id")

                if request_id is not None:
                    response_queue = self.responses.get(request_id)

                    if response_queue:
                        response_queue.put(message)

                elif "event" in message:
                    print("MPV EVENT:", message)
    
    def set_property(self, property_name, value):
        self.command("set_property", property_name, value)
        
    def get_property(self, property_name):
        response = self.command("get_property", property_name)
        return response.get("data")                        
    
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
        