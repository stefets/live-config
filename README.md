## My musical companion with MIDIDINGS as the KERNEL

# How it works
* Entry point is /src/live.sh SCENE (if SCENE is not specified, default is assumed)
* live.sh creates a complete file for mididings called script.py (in .gitignore) by replacing tokens in template.py
* User must configure in/out ports in template.py
* scr/scenes  contains your scenes
* src/patches contains your patches
* src/modules contains your callable functions
* scr/plugins contains your callable objects
  * Optionnal plugins are wrappers or helpers
    * mpg123 - remote mode
    * Spotify - API
    * Philips Hue - API
    * Request - requests
    * VLC Server - API
    * AKAI MIDIMIX - Helper to control the LED of the Akai MIDIMIX

# Dependencies
* See requirements.txt
* alsalist to configure the in/out ports in template.py

# Flaskdings 
## I maintain a HTML5 UI for mididings, an alternative of the livedings UI
### It's a UI supporting multiple clients and a Rest API, made with Flask and Flask SocketIO
* https://github.com/stefets/flaskdings

# Build
* Check the pages on how I configure mididings, boost and mpg123
* https://github.com/stefets/live-config/wiki

# Mididings ressources
* https://github.com/mididings/mididings (maintained)
* https://groups.google.com/g/mididings  (mailing list)
