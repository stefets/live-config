## [unreleased]

### 🚀 Features

- Add MIDI support for Numark Party Mix MKII and Mixxx
- Add new scenes for Fields Of Fire
- *(sd90)* Add audio level controls for DigiLevel, MasterLevel, and RecLevel
- Add new scenes for "PeaceInOurTime" with bass and guitar patches
- Add new scenes and MIDI patch for "Peace in Our Time"
- Update scene names and improve clarity in scene groups

### 🚜 Refactor

- Rename GT1000Patch to GT1KPreset and update references
- *(mp3)* Rename wrapper to mp3_player for clarity and update references
- Add more modularity
- *(soundcraft)* Switch  treble/bass knobs routing configuration
- Finally, make the main template entirely modular
- Remove argh dependency
- Rename rendering functions and update template handling

### 📚 Documentation

- Add initial CHANGELOG.md
- Update CHANGELOG
- Update CHANGELOG and README
- Update CHANGELOG with new scenes and MIDI patch for "Peace in Our Time"
- Update rendered script example

### 🧪 Testing

- Add Party Mix MKII

### ⚙️ Miscellaneous Tasks

- Remove duplicate files
- Update full script example
- Reorder channel check
- Remove HttpClient and related test files
- Update scene
- Update scene name
## [0.0.1] - 2025-11-10

### 🚀 Features

- Add Luminite Graviton MIDI controller
- *(daw)* Wip Rewin/Forward patch
- Add patch to send OSC rectoggle message to Soundcraft UI + Add to a scene group
- Use fcb1010 in control patch for DAW
- Add a callable object for easy bank select for POD HD
- Add GT-1000 MIDI ports to configuration
- Use Boss GT1000 (WIP)
- GT1000 integration (WIP)
- Add GT-1000 patch change by name
- *(control)* Add MASTER volume soundcraft control mapping for Nektar Expression Pedal
- *(soundcraft)* Add MIX auxiliary outputs and control mappings for Soundcraft UI
- *(sd90)* Add variations for Contemporary instrument part in SD-90 patch
- *(scene)* Add new scene 'Restless Natives' and update 'Wonderland' initialization
- *(scene)* Add 'Restless Natives' scene with initialization and patch configuration
- *(sd90)* Add Goblin
- Finish implement  SD90 AFX selectors

### 🐛 Bug Fixes

- Incorrect load_list usage
- *(config)* Incorrect port name
- *(gt1000)* Update target port comment for clarity and correct scene initialization
- *(control)* Update mpk_port_a mapping to use CakewalkController

### 💼 Other

- Set the port for Sysex
- Get NEWS from github, SVN is LOCKED
- Allow switch to scene 1
- Intelligent control patch
- Missing import
- Patch improvement
- *(test)* Add the simplest in/out test possible

### 🚜 Refactor

- *(vlc)* Use composition instead of inherit
- Add mp3 controller patch /  enable audio card
- *(mp3)* Use MPgy123 as property instead of inherit it
- Scene change
- *(mp3)* Add events (wip)
- Stop inherit mpyg123
- *(mp3)* Add managed events
- Use the events callback (WIP)
- Add toggle mute
- *(event)* Use event handler instead of callback
- Add scene
- Use toggle
- Adjust SD90 Sysex SET
- *(cakewalk)* Update routing; add to a scene
- Add control patch for Cakewalk DAW
- Force Channel 1 for DAW
- Abstract GT10B patch
- Abstract HD500 patches
- Patch name
- Remove GT10B patches from runtime patches.
- Decommission the Graviton midi controller
- Drop HD500 usage
- *(gt1000)* Adjusted bank selection patch interval.
- *(soundcraft)* Simplify soundcraft control and enhance key filtering
- *(filters)* Rename filter variables for consistency and clarity
- *(control)* Remove unused FCB1010 control mapping from MPK249 configuration
- Remove Q49 MIDI references from configuration
- *(scene)* Update 'Subdivisions' and 'The Trees' scenes with new initialization patches
- *(control)* Rename control variables for clarity and update references in control patch
- *(scene)* Update 'Grand Designs' scene initialization patch
- Add SD90 control patch for WAVE and INST + better naming for control patches
- *(sd90)* Simplify audio level control definitions and update SD90 controller configuration

### 📚 Documentation

- Update requirements file
- Update ReadMe
- Update example script
- Update readme
- Update readme
- Update readme

### 🧪 Testing

- Add virtual MIDI port

### ⚙️ Miscellaneous Tasks

- Remove useless comments
- Add patch
- Config change
- Patch change
- Scenes update
- Scene update
- Patch change
- Suspend virtual ports
- Patch update
- Control patch update
- *(daw)* Patch update
- Add scenes
- Move helpers outside src to labs
- Simplify file structure by the /include logic
- Patch/Scene update
- Add GT1000 in .asoundrc
- Remove annoying patch
- Update scene
- *(rush)* Patch update
- Update example script
