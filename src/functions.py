# ----------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------
# Function and classes called by scenes
#--------------------------------------------------------------------
#
# This class control mpg123 in remote mode with a keyboard (or any other midi devices of your choice)
# when NOTON or CTRL event is received in the __call__ function
#
# It's inspired of the 'song trigger keyboard' of the Quebec TV Show 'Tout le monde en parle'
#
class MPG123():
    def __init__(self):
        self.mpg123 = Popen(['mpg123', '-a', configuration['hw'], '--quiet', '--remote'], stdin=PIPE)
        self.write('silence')
        self.listing = configuration['listing']

    def __del__(self):
        self.mpg123.terminate()

    def __call__(self, ev):
        self.handle_note(ev) if ev.type == NOTEON else self.handle_control_change(ev)

    # 
    # Write a command to the mpg123 process
    #
    def write(self, cmd):
        self.mpg123.stdin.write(cmd + '\n')

    #
    # Note to remote command
    # Convert note number to switch scene or send a remote command to mpg123
    #
    def handle_note(self, ev):

        if ev.data1 >= 12:
            self.write('l {}{}.mp3'.format(configuration['symlinks'],ev.data1))
        # Reserved 0 to 11
        elif ev.data1 == 0:
            switch_scene(current_scene()-1)
        elif ev.data1 == 1:
            switch_subscene(current_subscene()-1)
        # TODO Free
        elif ev.data1 == 2:
            pass
        elif ev.data1 == 3:
            switch_subscene(current_subscene()+1)
        elif ev.data1 == 4:
            switch_scene(current_scene()+1)
        # TODO Do better
        elif ev.data1 == 5:
            self.write('j -5 s')
        elif ev.data1 == 6:
            self.write('p') # Pause mpg123
        elif ev.data1 == 7:
            self.write('j +5 s')
        elif ev.data1 == 11:
            Popen([self.listing], shell=True)  # ls -l
        else:
            # Fallback
            self.write('l /tmp/' + str(ev.data1) + '.mp3')

        ev.data2 = 0

        return ev

    # Convert a MIDI CC to a remote command
    def handle_control_change(self, ev):
        # MIDI volume to MPG123 volume
        if ev.data1==7 and ev.data2 <= 100:
            self.write('v ' + str(ev.data2))
        # MIDI modulation to mpg123 pitch resolution 
        # TODO Check hardware to set maximum pitch
        # On RPI, I can pitch 3% before hardware limitation is reached
        #elif ev.data1==1 and ev.data2 <= 100:
        #    self.write('pitch ' + str(float(ev.data2)/100))

# END MPG123() CLASS

#
# This class remove duplicate midi message by taking care of an offset logic
# NOT STABLE SUSPECT OVERFLOW 
class RemoveDuplicates:
    def __init__(self, _wait=0):
        self.wait = _wait
        self.prev_ev = None
        self.prev_time = 0

    def __call__(self, ev):
        if ev.type == NOTEOFF:
            sleep(self.wait)
            return ev
        now = engine.time()
        offset=now-self.prev_time
        if offset >= 0.035:
            #if ev.type == NOTEON:
            #    print "+ " + str(offset)
            r = ev
        else:
            #if ev.type == NOTEON:
            #    print "- " + str(offset)
            r = None
        self.prev_ev = ev
        self.prev_time = now
        return r

#--------------------------------------------------------------------
# Generate a chord prototype test
# Better to use the mididings builtin object Hamonize
def Chord(ev, trigger_notes=(41, 43), chord_offsets=(0, 4, 7)):
    if ev.type in (NOTEON, NOTEOFF):
        if ev.data1 in trigger_notes:
            evcls = NoteOnEvent if ev.type == NOTEON else NoteOffEvent
            return [evcls(ev.port, ev.channel, ev.note + i, ev.velocity)
                    for i in chord_offsets]
    return ev
#--------------------------------------------------------------------

# WIP: Glissando
def gliss_function(note, note_max, port, chan, vel):
    output_event(MidiEvent(NOTEOFF if note % 2 else NOTEON, port, chan, note / 2, vel))
    note += 1
    if note < note_max:
        Timer(.01, lambda: gliss_function(note, note_max, port, chan, vel)).start()

def gliss_exec(e):
    gliss_function(120, 168, e.port, e.channel, 100)

# WIP : Arpeggiator
def arpeggiator_function(current, max,note, port, chan, vel):
    output_event(MidiEvent(NOTEOFF if note % 2 else NOTEON, port, chan, note / 2, vel))
    current += 1
    if current < max:
        Timer(.15, lambda: arpeggiator_function(current, max, note,  port, chan, vel)).start()

def arpeggiator_exec(e):
    arpeggiator_function(0,16, 50,  e.port, e.channel, 100)

#-------------------------------------------------------------------------------------------

# Navigate through secenes and subscenes
def NavigateToScene(ev):
    # MIDIDINGS does not wrap in the builtin ScenesSwitch but SubSecenesSwitch yes with the wrap parameter
    # With that function, you can wrap trough Scenes AND SubScenes
    # That function assume that the first SceneNumber is 1
	#TODO field, values = dict(scenes()).items()[0]
    if ev.ctrl == 20:
        nb_scenes = len(scenes())
        cs=current_scene()
		# Scene backward
        if ev.value == 1:
            if cs > 1:
                switch_scene(cs-1)
		# Scene forward and wrap
        elif ev.value == 2:
            if cs < nb_scenes:
                switch_scene(cs+1)
            else:
                switch_scene(1)
		# SubScene backward
        elif ev.value == 3:
            css=current_subscene()
            if css > 1:
                switch_subscene(css-1)
		# SubScene forward and wrap
        elif ev.value == 4:
            css=current_subscene()
            nb_subscenes = len(scenes()[cs][1])
            if nb_subscenes > 0 and css < nb_subscenes:
                switch_subscene(css+1)
            else:
                switch_subscene(1)

# Stop any audio processing, managed by a simple bash script
def AllAudioOff(ev):
    return "/bin/bash ./kill.sh"

# Audio and midi players suitable for my SD-90
def play_file(filename):
    fname, fext = os.path.splitext(filename)
    if fext == ".mp3":
        path=" /tmp/soundlib/mp3/"
        command="mpg123 -q"
    elif fext == ".mid":
        path=" /tmp/soundlib/midi/"
        command="aplaymidi -p 20:1"

    return command + path + filename

# Create a pitchbend from a filter logic
# Params : direction when 1 bend goes UP, when -1 bend goes down
#          dont set direction with other values than 1 or -1 dude !
# NOTES  : On my context, ev.value.min = 0 and ev.value.max = 127
def OnPitchbend(ev, direction):
    if 0 < ev.value <= 126:
        return PitchbendEvent(ev.port, ev.channel, ((ev.value + 1) * 64)*direction)
    elif ev.value == 0:
        return PitchbendEvent(ev.port, ev.channel, 0)
    elif ev.value == 127:
        ev.value = 8191 if direction == 1 else 8192
    return PitchbendEvent(ev.port, ev.channel, ev.value*direction)

#---------------------------------------------------------------------------------------------------------
