## My musical assistant powered by mididings 

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

# Example
Example scripts are available in the examples directory

# Dependencies
* See requirements.txt

# Flaskdings UI
## I maintain a HTML5 UI for mididings, an alternative of the livedings UI
### It's a UI supporting multiple clients and a Rest API, made with Flask and Flask SocketIO
* https://github.com/stefets/flaskdings

# Build mididings
* Check the pages on how I configure mididings, boost and mpg123
* https://github.com/stefets/live-config/wiki

# mididings ressources
* https://github.com/mididings/mididings (maintained)
* https://groups.google.com/g/mididings  (mailing list)
