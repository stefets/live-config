#!/bin/bash

mpv --idle --input-ipc-server=/tmp/sd90a.sock --audio-device=alsa/SD90 &
mpv --idle --input-ipc-server=/tmp/sd90b.sock --audio-device=alsa/SD90 &
mpv --idle --input-ipc-server=/tmp/u192k.sock --audio-device=alsa/U192k &