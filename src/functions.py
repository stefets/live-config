# --------------------------------------------------------------------
# Function and classes called by scenes
# --------------------------------------------------------------------

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
        offset = now - self.prev_time
        if offset >= 0.035:
            # if ev.type == NOTEON:
            #    print "+ " + str(offset)
            r = ev
        else:
            # if ev.type == NOTEON:
            #    print "- " + str(offset)
            r = None
        self.prev_ev = ev
        self.prev_time = now
        return r

# -------------------------------------------------------------------------------------------
'''
Execute un glissando
'''
#def glissando(ev, from_note, to_note, vel, duration, direction, port):
#    note_range = range(from_note,to_note) if direction == 1 else reversed(range(from_note,to_note))
#    for note in note_range:
#        output_event(NoteOnEvent(port, ev.channel, note, vel))
#        sleep(duration)
#        output_event(NoteOffEvent(port, ev.channel, note))

def glissando_process(ev, from_note, to_note, vel, duration, direction, port, on):
    output_event(NoteOnEvent(port, ev.channel, from_note, vel)) if on else output_event(NoteOffEvent(port, ev.channel, from_note))
    if not on:
        from_note += 1
    if from_note < to_note:
        Timer(duration, lambda: glissando_process(ev, from_note, to_note, vel, duration, direction, port, not on)).start()

def glissando(ev, from_note, to_note, vel, duration, direction, port):
    glissando_process(ev, from_note, to_note, vel, duration, direction, port, True)

# -------------------------------------------------------------------------------------------


# Navigate through secenes and subscenes
def NavigateToScene(ev):
    # MIDIDINGS does not wrap in the builtin ScenesSwitch but SubSecenesSwitch yes with the wrap parameter
    # With that function, you can wrap trough Scenes AND SubScenes
    # That function assume that the first SceneNumber is 1
    # TODO field, values = dict(scenes()).items()[0]
    if ev.ctrl == 20:
        nb_scenes = len(scenes())
        cs = current_scene()
        # Scene backward
        if ev.value == 1:
            if cs > 1:
                switch_scene(cs - 1)
            # Scene forward and wrap
        elif ev.value == 2:
            if cs < nb_scenes:
                switch_scene(cs + 1)
            else:
                switch_scene(1)
            # SubScene backward
        elif ev.value == 3:
            css = current_subscene()
            if css > 1:
                switch_subscene(css - 1)
            # SubScene forward and wrap
        elif ev.value == 4:
            css = current_subscene()
            nb_subscenes = len(scenes()[cs][1])
            if nb_subscenes > 0 and css < nb_subscenes:
                switch_subscene(css + 1)
            else:
                switch_subscene(1)


# Stop any audio processing, managed by a simple bash script
def AllAudioOff(ev):
    return "/bin/bash ./kill.sh"


# Audio and midi players suitable for my SD-90
def play_file(filename):
    fname, fext = os.path.splitext(filename)
    if fext == ".mp3":
        path = " /tmp/soundlib/mp3/"
        command = "mpg123 -q"
    elif fext == ".mid":
        path = " /tmp/soundlib/midi/"
        command = "aplaymidi -p 20:1"

    return command + path + filename


# Create a pitchbend from a filter logic
# Params : direction when 1 bend goes UP, when -1 bend goes down
#          dont set direction with other values than 1 or -1 dude !
# NOTES  : On my context, ev.value.min = 0 and ev.value.max = 127
def OnPitchbend(ev, direction):
    if 0 < ev.value <= 126:
        return PitchbendEvent(ev.port, ev.channel, ((ev.value + 1) * 64) * direction)
    elif ev.value == 0:
        return PitchbendEvent(ev.port, ev.channel, 0)
    elif ev.value == 127:
        ev.value = 8191 if direction == 1 else 8192
    return PitchbendEvent(ev.port, ev.channel, ev.value * direction)

# ---------------------------------------------------------------------------------------------------------
