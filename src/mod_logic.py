# --------------------------------------------------------------------
# Helper functions
# --------------------------------------------------------------------

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

def NavigateToScene(ev):
    ''' 
    Navigate through Scenes and Sub-Scenes
    
    MIDIDINGS does not wrap in the builtin ScenesSwitch but SubSecenesSwitch yes with the wrap parameter
    
    With that function, you can wrap trough Scenes AND SubScenes
    
    That function assume that the first SceneNumber is 1
    '''
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

'''
    Convert data2 value to 0-1 range for the Soundcraft UI Mixer
'''
def data2_to_zero_one_range(ev):    
    return ev.data2 * 0.7874015748 / 100

def data2_to_mute(ev):
    return 1 if ev.data2==127 else 0

''' Set or overwrite an environment variable '''
def setenv(ev, key, value):
    os.environ[key] = value

''' Soundcraft input '''
def sc_input(ev, offset=-1):
    return ev.ctrl+offset if ev.type == CTRL else -1

def set_input(ev, offset):
    ev.ctrl = ev.ctrl + offset
    return ev

def debug(ev):
    print(ev)

