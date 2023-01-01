# My musical companion with MIDIDINGS as the KERNEL

# Notes
* Entry point is /src/live.sh SCENE (if SCENE is not specified, default is assumed)
* ./live.sh create a complete file for mididings called script.py (in .gitignore)
* Scenes are located in /src/scenes/*
* Example : ./live.sh debug
* You MUST replace tokens in the main.py template with you own logic

# Mididings users
## I maintain two UI for mididings
## Flaskdings 
### It's a UI and a rest API, using websockets and made with Flask
* https://github.com/stefets/flaskdings - Try it and star it !
## Node Red Flow Mididings
### It's a UI made with Node Red. It's a (static and slower) clone of my Flaskdings UI
* https://github.com/stefets/node-red-flow-mididings - Try it and star it !

# Build
* Check the pages on how I build mididings, python, boost and mpg123
* https://github.com/stefets/live-config/wiki

# Mididings ressources
* https://github.com/mididings/mididings (maintained)
* https://github.com/dsacre/mididings (abandonned)
* http://das.nasophon.de/mididings/ (official site)
* http://dsacre.github.io/mididings/doc/ (official documentation)
* https://groups.google.com/g/mididings (official mailing list)
