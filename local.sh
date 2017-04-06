#!/bin/bash

# Connect an Edirol SD-90 with a keyboard

aconnect -x

#KEYBOARD MIDI OUT TO SD-90 PART-A
aconnect 24:0 20:0

aconnect -l
