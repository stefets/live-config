## My musical companion with MIDIDINGS as the KERNEL

# How it works
* Entry point is /src/live.sh SCENE (if SCENE is not specified, default is assumed)
* live.sh creates a complete file for mididings called script.py (in .gitignore) by replacing tokens in template.py
* User must configure in/out ports in template.py
* scr/scenes contains scenes
* src/patches contains patches
* src/modules contains callable functions
* scr/plugins contains callable objects
** Plugins are wrappers over mpg123, Spotify, Philips Hue, Request

# Dependencies
* See requirements.txt
* Optional: alsalist to configure the in/out ports in template.py

# Flaskdings 
## I maintain a HTML5 UI for mididings
### It's a UI and a rest API, using websockets and made with Flask
* https://github.com/stefets/flaskdings

# Build
* Check the pages on how I build mididings, python, boost and mpg123
* https://github.com/stefets/live-config/wiki

# Mididings ressources
* https://github.com/mididings/mididings (maintained)
* https://github.com/dsacre/mididings (abandonned)
* http://das.nasophon.de/mididings/ (official site)
* http://dsacre.github.io/mididings/doc/ (official documentation)
* https://groups.google.com/g/mididings (official mailing list)
