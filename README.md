# A mididings script builder, created for my needs but adaptable
## It build my complex mididings script from a configuration file (src/config.json) and a Mako template (app.mako, asoundrc.mako)

# How it works
* Entry point is /src/app.py and load the configuration file
  * Because ALSA ports assignation for PCM is dynamic the script script builder take care of this:
    * Configure an ~/.asoundrc for audio devices with the help of pyalsaaudio
  * Then, it render to stdout a mididings script by replacing tokens in all Mako templates

# Extensions
  * The scr/extensions directory contains callable objects
    * Those extensions allow my mididings configuration to control modules I need like :
      * mpg123 - in remote mode to play MP3 audio files
        * It can start an instance of mpg123 for each sound card, each instance of mpg123 can play multiple audio files in parallel, this is possible with an asoundrc configuration that sets my PCM devices as dmix type
      * Philips Hue - API allow the send requests to a Philips Hue Bridge
      * Spotify - call their API to control a player
      * Request - send HTTP requests to any API
      * VLC Server - Send HTTP requests to a VLC server
      * AKAI MIDIMIX - Helper to manage the switch state and the LED of the Akai MIDIMIX

# Dependencies
* mididings, pyliblo, pyinotify
* vlc and python-vlc-http
* mpg123 and mpyg321
* python-dotenv
* pyalsaaudio
* colorama
* requests
* spotipy
* Mako
* phue
* argh

# Build mididings
* Check the pages on how I build mididings and boost from scratch
* https://github.com/stefets/live-config/wiki

# mididings ressources
* https://github.com/mididings/mididings (maintained)
* https://groups.google.com/g/mididings  (mailing list)

# Flaskdings UI
## I maintain a HTML5 UI for mididings, an alternative of the livedings UI
### It's an API supporting multiple clients and a Rest API, made with Flask and Flask SocketIO
* https://github.com/stefets/flaskdings
