# ----------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------
# Function and classes called by scenes
#--------------------------------------------------------------------
#
# This class control mpg123 in remote mode with a keyboard (or any other midi devices of your choice)
# when (actually) NOTEON or CTRL event type is received in the __call__ function
#
# It's inspired of the 'song trigger keyboard' of the Quebec TV Show 'Tout le monde en parle'
#
class MPG123():
    def __init__(self):
        self.mpg123 = Popen(['mpg123', '--audiodevice', configuration['hw'], '--quiet', '--remote'], stdin=PIPE)
        self.write('silence')
        self.ctrl_mapping = {
            7 : self.volume,
        }
        self.note_mapping = {
            0 : self.prev_scene,
            1 : self.prev_subscene,
            2 : self.free,
            3 : self.next_subscene,
            4 : self.next_scene,
            5 : self.rewind,
            6 : self.pause,
            7 : self.forward,
            8 : self.free,
            9 : self.free,
            10 : self.free,
            11 : self.list_files,
        }

    def __del__(self):
        self.mpg123.terminate()

    def __call__(self, ev):
        self.handle_control_change(ev) if ev.type == CTRL else self.handle_note(ev)

    # 
    # Write a command to the mpg123 process
    #
    def write(self, cmd):
        self.mpg123.stdin.write(cmd + '\n')

    #
    # Play a file or invoke a method defined in a dict
    #
    def handle_note(self, ev):
        self.play(ev.data1) if ev.data1 >= 12 else self.note_mapping[ev.data1]()

    #
    # Convert a MIDI CC to a remote command defined in a dict
    #
    def handle_control_change(self, ev):
        self.ctrl_mapping[ev.data1](ev.data2)

    #
    # dict values command functions
    #
    def free(self):
        pass

    # Scenes navigation
    def next_scene(self):
        ns = current_scene()+1
        switch_scene(ns)
        source = configuration['albums'] + scenes()[ns][0]
        target = configuration['symlink-target']
        check_call(['./create-symlinks.sh', source, target]) 

    def prev_scene(self):
        switch_scene(current_scene()-1)

    def next_subscene(self):
        switch_subscene(current_subscene()+1)
    def prev_subscene(self):
        switch_subscene(current_subscene()-1)

    # Mpg 123 remote call
    def play(self, id):
        self.write('l {}{}.mp3'.format(configuration['symlink-target'],id))
    def pause(self):
        self.write('p') # Pause mpg123
    def forward(self):
        self.jump('+5 s')
    def rewind(self):
        self.jump('-5 s')
    def jump(self, offset):
        self.write('j ' + offset)
    def volume(self, value):
        self.write('v {}'.format(value))

    # Tools
    def list_files(self):
        Popen([configuration['listing']], shell=True)  # ls -l

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
