
import os
import sys
import json
from time import sleep
from threading import Timer

from mididings import engine
from mididings.extra import *
from mididings.extra.osc import *
from mididings.extra.inotify import *
from mididings.event import PitchbendEvent, MidiEvent, NoteOnEvent, NoteOffEvent, CtrlEvent, ProgramEvent, SysExEvent
from mididings.engine import scenes, current_scene, switch_scene, current_subscene, switch_subscene, output_event

# Setup path
sys.path.append(os.path.realpath('.'))
# Environment
from dotenv import load_dotenv
load_dotenv()

# Extensions
from adapters.mpv import MpvAdapter
from extensions.vlc import *
from extensions.philips import *
from extensions.spotify import *
from extensions.midimix import *
from extensions.gt1000 import GT1KPreset