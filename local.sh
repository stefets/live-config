#!/bin/bash

# Connect my keyboard with sd-90 part-a (usb mode)

aconnect -x

#KEYBOARD MIDI OUT TO SD-90 PART-A
aconnect 24:0 20:0

aconnect -l
