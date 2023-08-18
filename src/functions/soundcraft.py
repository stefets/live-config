#
# Helper functions used by the Soundcraft UI patches
#

# 0-127 to 0-1
ratio=0.7874015748 / 100

def ui_cursor(ev):
    return ev.data2 * ratio

def ui_knob(ev):
    return ui_cursor(ev)

def ui_mute(ev):
    return 1 if ev.data2==127 else 0

''' Return the controller value for SendOsc '''
def ui_event(ev, offset=0):
    return ev.ctrl+offset if ev.type == CTRL else -1

''' Wrapper over ui_event '''
def ui_left(ev):
    return ui_event(ev)

''' Wrapper over ui_event '''
def ui_right(ev):
    return ui_event(ev, 1)

