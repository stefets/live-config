## My musical assistant powered by mididings 

# How it works
* Entry point is /src/app.py 
  * It configure an ~/.asoundrc for audio devices
  * It conand it creates a complete file for mididings called script.py (in .gitignore) by replacing tokens in template.mako with the Mako Template Engine.
* scr/extensions contains callable objects
  * Those extensions allow mididings to do great stuff like :
    * mpg123 - in remote mode to play audio files
    * Spotify - API allow to control a Spotify player
    * Philips Hue - API allow the control of the Hue Bridge
    * Request - requests allow to send HTTP requestion
    * VLC Server - API
    * AKAI MIDIMIX - Helper manage the switch state and the LED of the Akai MIDIMIX

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
