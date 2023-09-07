# This is a mididings script builder application
## It build a mididings script with a configuration file and Mako templates

# How it works
* Entry point is /src/app.py and load the app.json configuration file
  * ALSA ports assignation for PCM and MIDI is dynamic
    * Configure an ~/.asoundrc for audio devices with the help of pyalsaaudio
    * Configure the in_ports and out_ports section with the help of alsa_midi
  * Finally, it generate a complete or minimal mididings script called script.py (in .gitignore) by replacing tokens in template.mako with the Mako Template Engine.

# Extensions
  * The scr/extensions direcotry contains callable objects
    * Those extensions allow my mididings configuration to control modules I need like :
      * mpg123 - in remote mode to play audio files
        * I can start an instance of mpg123 for each sound card
      * Spotify - API allow to control a Spotify player
      * Philips Hue - API allow the control of the Hue Bridge
      * Request - requests allow to send HTTP requests
      * VLC Server - Send HTTP requests to VLC server
      * AKAI MIDIMIX - Helper manage the switch state and the LED of the Akai MIDIMIX

# Example
Examples are sometime available in the examples directory

# Dependencies
* mididings, pyliblo, pyinotify
* pyalsaaudio
* alsa_midi
* mpyg321, pexpect
* Mako
* python-vlc-http
* colorama
* argh
* phue
* python-dotenv
* requests
* spotipy

# Flaskdings UI
## I maintain a HTML5 UI for mididings, an alternative of the livedings UI
### It's an API supporting multiple clients and a Rest API, made with Flask and Flask SocketIO
* https://github.com/stefets/flaskdings

# Build mididings
* Check the pages on how I build mididings and boost from scratch
* https://github.com/stefets/live-config/wiki

# mididings ressources
* https://github.com/mididings/mididings (maintained)
* https://groups.google.com/g/mididings  (mailing list)
