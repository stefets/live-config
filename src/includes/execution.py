
# -----------------------------------------------------------------------------------------------
# Execution patches
# -----------------------------------------------------------------------------------------------
# Notes :
# - Ctrl #3 est Undefined selon la documentation du protocole MIDI; donc libre d'utilisation.
# - L'utilisation du Ctrl(3,value) sert a passer le value dans EVENT_VALUE pour l'unité suivante dans une série d'unité
# - Soit pour assigner une valeur au pédales d'expression du POD HD 500
# - Soit pour déterminer la valeur d'une transition pour le chargement d'une scène du Philips HUE
# - Soit pour contrôler Cakewalk
#
# Controller 3 : ref.: https://www.midi.org/specifications-old/item/table-3-control-change-messages-data-bytes-2
# CC      Bin             Hex     Control function    Value       Used as
# 3	00000011	03	Undefined	    0-127	MSB


# Base patches (WIP)
# p_hd500_filter_base = [
#     (KeyFilter(notes=[65]) >> FS1),
#     (KeyFilter(notes=[66]) >> CakePlay),
#     (KeyFilter(notes=[67]) >> FS2),
#     (KeyFilter(notes=[68]) >> CakeStop),
#     (KeyFilter(notes=[69]) >> FS3),
#     (KeyFilter(notes=[70]) >> CakeRecord),
#     (KeyFilter(notes=[71]) >> FS4),
#     (KeyFilter(notes=[71]) >> Discard()),
# ]

p_hue_live = [
    KeyFilter(notes=[61]) >> HueStudioOff,
    KeyFilter(notes=[63]) >> HueNormal,
    KeyFilter(notes=[66]) >> HueGalaxie,
    KeyFilter(notes=[68]) >> HueGalaxieMax,
    KeyFilter(notes=[70]) >> HueDemon,
]

p_base = [
    p_hue_live,
    # p_hd500_filter_base, 
]

p_pk5ctrl_generic = pk5 >> Filter(NOTEON)

# 

akai_pad_nature = [
    ~Filter(PITCHBEND) >> KeyFilter(notes=[109]) >> LatchNotes(polyphonic=True) >> Key(0) >> Rain,
    KeyFilter(notes=[110]) >> Key(12) >> Thunder,
    KeyFilter(notes=[111]) >> Key(48) >> Dog,
    KeyFilter(notes=[112]) >> Key(24) >> BirdTweet,
    KeyFilter(notes=[113]) >> Key(72) >> Screaming,
    KeyFilter(notes=[114]) >> Key(48) >> Velocity(fixed=100) >> Explosion, 
    ~Filter(PITCHBEND) >> KeyFilter(notes=[115]) >> Key(12) >> Wind, 
    ~Filter(PITCHBEND) >> KeyFilter(notes=[116]) >> LatchNotes(polyphonic=True) >> Key(36) >> Applause, 
]

# Patch Synth
keysynth =  Velocity(fixed=80) >> Output(sd90_port_a, channel=3, program=(Classical,51), volume=100, ctrls={93:75, 91:75})
#--------------------------------------------------------------------

# Patches for Marathon by Rush

# Accept (B4, B3) and E4 => transformed to a chord 
marathon_intro=(mpk_a
>>LatchNotes(False,reset='c5') >> Velocity(fixed=110) >>
	( 
		(KeyFilter('e4') >> Harmonize('e','major',['unison', 'fifth'])) //
		(KeyFilter(notes=[71, 83])) 
	) >> Output(sd90_port_a, channel=3, program=(Classical,51), volume=110, ctrls={93:75, 91:75}))

# Note : ChannelFilter 2 - Enable PK5 message only
marathon_chords=(pk5 >> LatchNotes(False, reset='c4') >> Velocity(fixed=80) >>
	(

		# From first to last...
		(KeyFilter('e3') >> Key('b3') >> Harmonize('b','major',['unison', 'third', 'fifth', 'octave'])) //
		(KeyFilter('c3') >> Key('e3') >> Harmonize('e','major',['unison', 'third', 'fifth', 'octave'])) //
		(KeyFilter('d3') >> Key('f#3') >> Harmonize('f#','major',['unison', 'third', 'fifth', 'octave'])) //

		# From first to last 2 frets higher
		(KeyFilter('a3') >> Key('c#4') >> Harmonize('c#','major',['unison', 'third', 'fifth', 'octave'])) //
		(KeyFilter('f3') >> Key('f#3') >> Harmonize('f#','major',['unison', 'third', 'fifth', 'octave'])) //
		(KeyFilter('g3') >> Key('g#3') >> Harmonize('g#','major',['unison', 'third', 'fifth', 'octave'])) // 

        # Isolated note
        (KeyFilter('b3') >> Key('a6'))

	) >> Transpose(-24) >> Output(sd90_port_a, channel=4, program=(Classical+Var1,51), volume=100, ctrls={93:75, 91:75}))

marathon_bridge=(mpk_a
 >>
	(
		(KeyFilter('c2') >> Key('b2') >> Harmonize('b','minor',['unison', 'third', 'fifth'])) //
		(KeyFilter('e2') >> Key('f#3') >> Harmonize('f#','minor',['unison', 'third', 'fifth' ])) //
		(KeyFilter('d2') >> Key('e3') >> Harmonize('e','major',['unison', 'third', 'fifth']))  
	) >> Velocity(fixed=75) >> Output(sd90_port_a, channel=3, program=(Classical,51), volume=110, ctrls={93:75, 91:75}))

# Solo bridge, lower -12
marathon_bridge_lower=(mpk_a
 >>
	(
		(KeyFilter('c1') >> Key('b1') >> Harmonize('b','minor',['unison', 'third', 'fifth'])) //
		(KeyFilter('d1') >> Key('e1') >> Harmonize('e','major',['third', 'fifth'])) //
		(KeyFilter('e1') >> Key('f#2') >> Harmonize('f#','minor',['unison', 'third', 'fifth' ]))
	) >> Velocity(fixed=90) >>  Output(sd90_port_a, channel=4, program=(Classical,51), volume=75, ctrls={93:75, 91:75}))

# You can take the most
marathon_cascade=(mpk_a
 >> KeyFilter('f3:c#5') >> Transpose(12) >> Velocity(fixed=50) >> Output(sd90_port_b, channel=11, program=(Enhanced,99), volume=80))

marathon_bridge_split= KeySplit('f3', marathon_bridge_lower, marathon_cascade)

# Patch Syhth. generique pour lowbase
lowsynth2 =  Velocity(fixed=115) >> Output(sd90_port_a, channel=1, program=51, volume=115, ctrls={93:75, 91:75})
#--------------------------------------------------------------------

# Patch Closer to the hearth 
closer_high = Output(sd90_port_a, channel=1, program=(Enhanced,15), volume=100)
closer_base = Velocity(fixed=100) >> Output(sd90_port_a, channel=2, program=(Enhanced,51), volume=100)
closer_main =  KeySplit('c3', closer_base, closer_high)
#--------------------------------------------------------------------

# Patch Time Stand Still
tss_high = Velocity(fixed=90) >> Output(sd90_port_a, channel=3, program=(Enhanced,92), volume=80)
tss_base = Transpose(12) >> Velocity(fixed=90) >> Output(sd90_port_a, channel=3, program=(Enhanced,92), volume=100)
tss_keyboard_main =  KeySplit('c2', tss_base, tss_high)

tss_foot_left = Transpose(-12) >> Velocity(fixed=75) >> Output(sd90_port_a, channel=2, program=(Enhanced,103), volume=100)
tss_foot_right = Transpose(-24) >> Velocity(fixed=75) >> Output(sd90_port_a, channel=2, program=(Enhanced,103), volume=100)
tss_foot_main =  KeySplit('d#3', tss_foot_left, tss_foot_right)

#--------------------------------------------------------------------

# Patch Analog Kid
#analog_pod2=(
#	(Filter(NOTEON) >> (KeyFilter('c3') % Ctrl(51,0)) >> Output('PODHD500',9)) //
#	(Filter(NOTEON) >> (KeyFilter('d3') % Ctrl(51,127)) >> Output('PODHD500',9))
#)
#analog_pod=(Filter(NOTEON) >> (KeyFilter('c3') % Ctrl(51,27)) >> Output('PODHD500',9))

mission= LatchNotes(False,reset='c#3')  >> Transpose(-12) >>Harmonize('c','major',['unison', 'third', 'fifth', 'octave']) >> Output(sd90_port_a,channel=1,program=(Solo,53),volume=100,ctrls={91:75})

analogkid_low= (LatchNotes(False,reset='c#3') >>
	( 
		(KeyFilter('c3:d#3') >> Transpose(-7) >> Harmonize('c','major',['unison', 'third', 'fifth', 'octave'])) //
		(KeyFilter('e3') >> Key('a3')) 
	) >> Output(sd90_port_a,channel=1,program=(Solo,53),volume=100,ctrls={91:75}))
analogkid_high = Output(sd90_port_a, channel=2, program=(Solo,53), volume=100, ctrls={93:75, 91:100})
analogkid_main =  KeySplit('f3', analogkid_low, analogkid_high)

#analogkid_ending =  Key('a1') >> Output(sd90_port_a, channel=5, program=(Special2,68), volume=100)

#--------------------------------------------------------------------

# Patch Limelight
limelight =  Key('d#6') >> Output(sd90_port_a, channel=16, program=(Special1,12), volume=100)

# Band : Moi ----------------------------------------------------

# Song : Centurion 

# Init patch 
i_centurion = [
        Call(Playlist()), 
]

# Execution patch
seq_centurion = (Velocity(fixed=110) >>	
    [
		Output(sd90_port_a, channel=1, program=(Enhanced,96), volume=110, pan=32),
		Output(sd90_port_a, channel=2, program=(Enhanced,82), volume=110, pan=96)
	])

# Filter
p_centurion = (LatchNotes(True, reset='C3') >>
	(
		(KeyFilter('D3') >> Key('D1')) //
		(KeyFilter('E3') >> Key('D2')) //
		(KeyFilter('F3') >> Key('D3')) //
		(KeyFilter('G3') >> Key('D4')) //
		(KeyFilter('A3') >> Key('D5'))
	) >> seq_centurion)


# Band : Big Country ------------------------------------------

# Song : In a big country
i_big_country = Pass()
p_big_country = Pass()

# Song : In a big country - recording
i_big_country_live =  Pass()
p_big_country_live =  Pass()

# Song : Highland Scenery
p_highland_scenery =  Pass()


# Big Country fin de section ------------------------------------------

# Band : Octobre ------------------------------------------

# Init patch (Intro)
i_octobre = []

# Execution patch
p_octobre =  Pass()

# Octobre fin de section ------------------------------------------

# Band : Rush ------------------------------------------

# Default init patch
i_rush =  Pass()

# Default patch - tout en paralelle mais séparé par contexte
p_rush = Pass()

# Subdivisions

# Init patch
i_rush_sub =  Pass()

# Grand Designs

# Init patch
i_rush_gd =  Pass()

# Execution patch
p_rush_gd =  Pass()

# Youtube SoundCraftBridge Demo
p_rush_gd_demo = Pass()

# The Trees

# Init patch
i_rush_trees =  Pass()

# Foot keyboard output
p_rush_trees_foot = Velocity(fixed=110) >> Output(sd90_port_a, channel=1, program=(Classical,51), volume=110, ctrls={93:75, 91:75})

# Execution patch
p_rush_trees=(pk5_filter >>
    [
        # Controle de l'éclairage
        #Filter(NOTEON) >> [
        #    KeyFilter('C3') >> HueGalaxie,
        #    KeyFilter(notes=[71]) >> HueGalaxie,
        #    KeyFilter(notes=[72]) >> HueSoloRed,
        #],
        # Controle du séquenceur 
        # Il faut laisser passer f3 dans un filtre dummy car il sert de Latch
        [
            KeyFilter('C3') >> Key('A0'),
            KeyFilter('D3') >> Key('B0'),
            KeyFilter('E3') >> Key('D1'),
            KeyFilter('f3') >> Pass(),
        ] >> LatchNotes(False, reset='f3') >> p_rush_trees_foot
    ])

# Rush fin de section ------------------------------------------

# Muse Band
p_muse = p_pk5ctrl_generic >> p_base
p_muse_stockholm = pk5 >> [
    KeyFilter(notes=[60]) >> [
        Key('d2') >> Harmonize('d', 'major', ['unison', 'octave']),
        HueDemon
    ],
    KeyFilter(notes=[62]) >> [
        Key('e2') >> Harmonize('e', 'major', ['unison', 'octave']),
        HueGalaxieMax
    ],
    KeyFilter(notes=[64]) >> [
        Key('f2') >> Harmonize('f', 'major', ['unison', 'octave']),
        HueGalaxie
    ],
] >> Velocity(fixed=127) >> Output(sd90_port_b, channel=14, program=(Special2,106), volume=127, ctrls={93:75, 91:75})


p_rush = p_pk5ctrl_generic >> p_base

p_wonderland_init = [
    Ctrl(mpk_port_a, 3, 2, 64) >> ui_standard_stereo_fx,
]
p_wonderland = p_pk5ctrl_generic >> [
     p_base,
     KeyFilter(72) >> NoteOn(9, 127) >> Port(midimix_midi) >> soundcraft_control,
]
p_wonderland_rec = p_pk5ctrl_generic >> [
]

# ---
# Daw + Hue helper for recording
p_transport = (pk5 >> [
            p_hue_live,
            Filter(NOTEON)  >> KeyFilter(notes=[60])    >> [CakePlay],
            Filter(NOTEON)  >> KeyFilter(notes=[62])    >> [CakeRecord],
            Filter(NOTEOFF) >> KeyFilter(notes=[60,62]) >> [HueGalaxieMax], 
        ])

# Interlude patch, between two songs
interlude = mpk_b >> ChannelFilter(16) >> KeyFilter(notes=[0,49]) >> Velocity(fixed=50) >> LatchNotes(reset=0) >> [Oxigenizer]

# Glissando
p_glissando=(Filter(NOTEON) >> Call(glissando, 48, 84, 100, 0.01, -1, sd90_port_a))
