#!/bin/bash

rm -f /tmp/sd90a.sock /tmp/sd90b.sock /tmp/u192k.sock
rm -f /tmp/mvp-sd90a.log /tmp/mvp-sd90b.log /tmp/mvp-u192k.log

mpv --idle=yes --keep-open=yes --no-video --no-terminal --input-ipc-server=/tmp/sd90a.sock --audio-device=alsa/SD90 --log-file=/tmp/mvp-sd90a.log --msg-level=all=info  &
mpv --idle=yes --keep-open=yes --no-video --no-terminal --input-ipc-server=/tmp/sd90b.sock --audio-device=alsa/SD90 --log-file=/tmp/mvp-sd90b.log --msg-level=all=info  &
mpv --idle=yes --keep-open=yes --no-video --no-terminal --input-ipc-server=/tmp/u192k.sock --audio-device=alsa/U192k --log-file=/tmp/mvp-u192k.log --msg-level=all=info &