import os
import json
import sys
import requests

class Hue():
    def __init__(self, sid):
        self.sid = sid

    def __call__(self, ev):
        try:
            response = requests.get("http://192.168.1.146:5002/scenes/" + self.sid)
        except:
            print("Hue plugin error: Request failed")

    
