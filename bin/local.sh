#!/bin/bash

# SD-90 Specific
# Connect my keyboard with sd-90 part-a (usb mode)
#KEYBOARD MIDI OUT TO SD-90 PART-A
aconnect -x
aconnect 24:0 20:0
aconnect -l
