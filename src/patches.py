'''
Notes :

- L'utilisation du Ctrl(3,value) sert a passer le value dans EVENT_VALUE pour l'unité suivante dans une série d'unité
- Soit pour assigner une valeur au pédales d'expression du POD HD 500
- Soit pour déterminer la valeur d'une transition pour le chargement d'une scène du Philips HUE
- Soit pour contrôler Cakewalk

Controller 3 : ref.: https://www.midi.org/specifications-old/item/table-3-control-change-messages-data-bytes-2
CC      Bin             Hex     Control function    Value       Used as
3	00000011	03	Undefined	    0-127	MSB
'''
# Lighting patches -----------------------------------------------------------------------------
HueOff=Call(HueBlackout(hue_config))
HueNormal=Call(HueScene(hue_config, "Normal"))
HueGalaxie=Call(HueScene(hue_config, "Galaxie"))
HueGalaxieMax=Call(HueScene(hue_config, "GalaxieMax"))
HueDemon=Call(HueScene(hue_config, "Demon"))
HueSoloRed=Call(HueScene(hue_config, "SoloRed"))
HueDetente=Call(HueScene(hue_config, "Détente"))
HueVeilleuse=Call(HueScene(hue_config, "Veilleuse"))
HueLecture=Call(HueScene(hue_config, "Lecture"))

violon = Output('SD90-PART-A', channel=1, program=(Classical,41))

p_hue = Filter(NOTEON) >> [
    KeyFilter(notes=[101]) >> HueNormal, 
    KeyFilter(notes=[102]) >> HueDetente, 
    KeyFilter(notes=[103]) >> HueLecture, 
    KeyFilter(notes=[104]) >> HueVeilleuse, 
    KeyFilter(notes=[105]) >> HueGalaxie, 
    KeyFilter(notes=[106]) >> HueGalaxieMax, 
    KeyFilter(notes=[107]) >> HueDemon, 
    KeyFilter(notes=[108]) >> HueOff, 

]

akai_pad_nature = [
    ~Filter(PITCHBEND) >> KeyFilter(notes=[109]) >> LatchNotes(polyphonic=True) >> Key(0) >> Rain,
    KeyFilter(notes=[110]) >> Key(12) >> Thunder,
    KeyFilter(notes=[111]) >> Key(48) >> Dog,
    KeyFilter(notes=[112]) >> Key(24) >> BirdTweet,
    KeyFilter(notes=[113]) >> Key(72) >> Screaming,
    KeyFilter(notes=[114]) >> Key(48) >> Explosion, 
    ~Filter(PITCHBEND) >> KeyFilter(notes=[115]) >> Key(12) >> Wind, 
    ~Filter(PITCHBEND) >> KeyFilter(notes=[116]) >> LatchNotes(polyphonic=True) >> Key(36) >> Applause, 
]

#-----------------------------------------------------------------------------------------------

# My Cakewalk Generic Control Surface definition -----------------------------------------------
CakeRecord=Ctrl('MPK-MIDI-OUT-3', 1, 119,127)
CakePlay=Ctrl('MPK-MIDI-OUT-3', 1, 118, 127)
CakeStop=Ctrl('MPK-MIDI-OUT-3', 1, 119, 127)
#-----------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------
# Execution patches
#-----------------------------------------------------------------------------------------------


#explosion = Key(0) >> Velocity(fixed=100) >> Output('SD90-PART-A', channel=1, program=(Classical+Var3,128), volume=100)
piano_base =  Velocity(fixed=100) >> Output('SD90-PART-A', channel=1, program=(Classical,1))
nf_piano = Output('SD90-PART-A', channel=1, program=(Classical,2), volume=100)
piano =  Output('SD90-PART-A', channel=3, program=(Classical,1), volume=100)
piano2 = Output('SD90-PART-A', channel=2, program=(Classical,2), volume=100)

# Patch Synth
keysynth =  Velocity(fixed=80) >> Output('SD90-PART-A', channel=3, program=(Classical,51), volume=100, ctrls={93:75, 91:75})
#--------------------------------------------------------------------

# Patches for Marathon by Rush

# Accept (B4, B3) and E4 => transformed to a chord 
marathon_intro=(cme>>LatchNotes(False,reset='c5') >> Velocity(fixed=110) >>
	( 
		(KeyFilter('e4') >> Harmonize('e','major',['unison', 'fifth'])) //
		(KeyFilter(notes=[71, 83])) 
	) >> Output('SD90-PART-A', channel=3, program=(Classical,51), volume=110, ctrls={93:75, 91:75}))

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

	) >> Transpose(-24) >> Output('SD90-PART-A', channel=4, program=(Classical+Var1,51), volume=100, ctrls={93:75, 91:75}))

marathon_bridge=(cme >>
	(
		(KeyFilter('c2') >> Key('b2') >> Harmonize('b','minor',['unison', 'third', 'fifth'])) //
		(KeyFilter('e2') >> Key('f#3') >> Harmonize('f#','minor',['unison', 'third', 'fifth' ])) //
		(KeyFilter('d2') >> Key('e3') >> Harmonize('e','major',['unison', 'third', 'fifth']))  
	) >> Velocity(fixed=75) >> Output('SD90-PART-A', channel=3, program=(Classical,51), volume=110, ctrls={93:75, 91:75}))

# Solo bridge, lower -12
marathon_bridge_lower=(cme >>
	(
		(KeyFilter('c1') >> Key('b1') >> Harmonize('b','minor',['unison', 'third', 'fifth'])) //
		(KeyFilter('d1') >> Key('e1') >> Harmonize('e','major',['third', 'fifth'])) //
		(KeyFilter('e1') >> Key('f#2') >> Harmonize('f#','minor',['unison', 'third', 'fifth' ]))
	) >> Velocity(fixed=90) >>  Output('SD90-PART-A', channel=4, program=(Classical,51), volume=75, ctrls={93:75, 91:75}))

# You can take the most
marathon_cascade=(cme >> KeyFilter('f3:c#5') >> Transpose(12) >> Velocity(fixed=50) >> Output('SD90-PART-B', channel=11, program=(Enhanced,99), volume=80))

marathon_bridge_split= KeySplit('f3', marathon_bridge_lower, marathon_cascade)

# Patch Syhth. generique pour lowbase
lowsynth2 =  Velocity(fixed=115) >> Output('SD90-PART-A', channel=1, program=51, volume=115, ctrls={93:75, 91:75})
#--------------------------------------------------------------------

# Patch Closer to the hearth 
closer_high = Output('SD90-PART-A', channel=1, program=(Enhanced,15), volume=100)
closer_base = Velocity(fixed=100) >> Output('SD90-PART-A', channel=2, program=(Enhanced,51), volume=100)
closer_main =  KeySplit('c3', closer_base, closer_high)
#--------------------------------------------------------------------

# Patch Time Stand Still
tss_high = Velocity(fixed=90) >> Output('SD90-PART-A', channel=3, program=(Enhanced,92), volume=80)
tss_base = Transpose(12) >> Velocity(fixed=90) >> Output('SD90-PART-A', channel=3, program=(Enhanced,92), volume=100)
tss_keyboard_main =  KeySplit('c2', tss_base, tss_high)

tss_foot_left = Transpose(-12) >> Velocity(fixed=75) >> Output('SD90-PART-A', channel=2, program=(Enhanced,103), volume=100)
tss_foot_right = Transpose(-24) >> Velocity(fixed=75) >> Output('SD90-PART-A', channel=2, program=(Enhanced,103), volume=100)
tss_foot_main =  KeySplit('d#3', tss_foot_left, tss_foot_right)

#--------------------------------------------------------------------

# Patch Analog Kid
#analog_pod2=(
#	(Filter(NOTEON) >> (KeyFilter('c3') % Ctrl(51,0)) >> Output('PODHD500',9)) //
#	(Filter(NOTEON) >> (KeyFilter('d3') % Ctrl(51,127)) >> Output('PODHD500',9))
#)
#analog_pod=(Filter(NOTEON) >> (KeyFilter('c3') % Ctrl(51,27)) >> Output('PODHD500',9))

mission= LatchNotes(False,reset='c#3')  >> Transpose(-12) >>Harmonize('c','major',['unison', 'third', 'fifth', 'octave']) >> Output('SD90-PART-A',channel=1,program=(Solo,53),volume=100,ctrls={91:75})

analogkid_low= (LatchNotes(False,reset='c#3') >>
	( 
		(KeyFilter('c3:d#3') >> Transpose(-7) >> Harmonize('c','major',['unison', 'third', 'fifth', 'octave'])) //
		(KeyFilter('e3') >> Key('a3')) 
	) >> Output('SD90-PART-A',channel=1,program=(Solo,53),volume=100,ctrls={91:75}))
analogkid_high = Output('SD90-PART-A', channel=2, program=(Solo,53), volume=100, ctrls={93:75, 91:100})
analogkid_main =  KeySplit('f3', analogkid_low, analogkid_high)

#analogkid_ending =  Key('a1') >> Output('SD90-PART-A', channel=5, program=(Special2,68), volume=100)

#--------------------------------------------------------------------

# Patch Limelight
limelight =  Key('d#6') >> Output('SD90-PART-A', channel=16, program=(Special1,12), volume=100)

# Band : Moi ----------------------------------------------------

# Song : Centurion 

# Init patch 
i_centurion = [
        Call(Playlist(playlist_config)), 
        P02A, Ctrl(3,40) >> Expr1, Ctrl(3,127) >> Expr2
]

# Execution patch
seq_centurion = (Velocity(fixed=110) >>	
    [
		Output('SD90-PART-A', channel=1, program=(Enhanced,96), volume=110, pan=32),
		Output('SD90-PART-A', channel=2, program=(Enhanced,82), volume=110, pan=96)
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

# Init patch
i_big_country = [U01_A, P14A, FS1, FS3, Ctrl(3,40) >> Expr1 , Ctrl(3,127) >> Expr2]

# Execution patch

i_big_country_live = [P14D, FS1, FS3, FS4, Ctrl(3,45) >> Expr1 , Ctrl(3,85) >> Expr2]
p_big_country_live = (pk5 >> KeyFilter(notes=[60]) >> 
        [
            Filter(NOTEON) >> [CakePlay],
            Filter(NOTEOFF) >> HueGalaxieMax, 
        ])

p_big_country = (pk5 >> Filter(NOTEON) >>
         [
             (KeyFilter(notes=[69]) >> FS4),
             (KeyFilter(notes=[71]) >> [HueGalaxie, FS2, Ctrl(3,85) >> Expr2]),
             (KeyFilter(notes=[72]) >> [HueSoloRed, FS2, Ctrl(3,127) >> Expr2])
         ])

# Big Country fin de section ------------------------------------------

# Band : Rush ------------------------------------------

# Default init patch
i_rush = [P02A, Ctrl(3,50) >> Expr1, Ctrl(3,100) >> Expr2]

# Default patch - tout en paralelle mais séparé par contexte
p_rush = (pk5 >> Filter(NOTEON) >>
    [
        [
            KeyFilter(notes=[60]) >> HueOff,
            KeyFilter(notes=[62]) >> HueGalaxie,
            KeyFilter(notes=[64]) >> HueSoloRed
        ],                
        [
            KeyFilter(notes=[69]) >> FS4,
            KeyFilter(notes=[71]) >> [FS1, FS4, Ctrl(3,100) >> Expr2, HueGalaxie],
            KeyFilter(notes=[72]) >> [FS1, FS4, Ctrl(3,120) >> Expr2, HueSoloRed]
        ]
    ])

# Subdivisions

# Init patch
i_rush_sub=[P02A, FS3, Ctrl(3,40) >> Expr1, Ctrl(3,100) >> Expr2]

# Grand Designs

# Init patch
i_rush_gd = [P02A, FS1, FS3, Ctrl(3,40) >> Expr1, Ctrl(3,127) >> Expr2] 

# Execution patch
p_rush_gd = (pk5 >> 
    [
        Filter(NOTEON) >> [
                [ 
                    KeyFilter(notes=[60]) >> HueOff,
                    KeyFilter(notes=[61]) >> Ctrl(3, 1) >> HueDemon,
                    KeyFilter(notes=[62]) >> Ctrl(3, 50) >> HueGalaxie,
                    KeyFilter(notes=[64, 72]) >> Ctrl(3, 1) >> HueSoloRed,
                ],
                [
                    KeyFilter(notes=[67]) >> FS4,
                    KeyFilter(notes=[69]) >> [Ctrl(3, 100) >> Expr2, FS4],
                    KeyFilter(notes=[71]) >> [Ctrl(3, 127) >> Expr2, FS4],
                    KeyFilter(notes=[72]) >>  Ctrl(3, 127) >> Expr2
                ],
            ],
        Filter(NOTEOFF) >> [
                [
                    KeyFilter(notes=[72]) >> Ctrl(3, 1) >> HueGalaxie
                ],
                [
                    KeyFilter(notes=[72]) >> Ctrl(3, 100) >> Expr2
                ]
            ],
    ])

# The Trees

# Init patch
i_rush_trees = [P02A, FS3, Ctrl(3,40) >> Expr1, Ctrl(3,100) >> Expr2] 

# Foot keyboard output
p_rush_trees_foot = Velocity(fixed=110) >> Output('SD90-PART-A', channel=1, program=(Classical,51), volume=110, ctrls={93:75, 91:75})

# Execution patch
p_rush_trees=(pk5 >>
    [
        # Controle de l'éclairage
        Filter(NOTEON) >> [
            KeyFilter('C3') >> HueGalaxie,
            KeyFilter(notes=[71]) >> HueGalaxie,
            KeyFilter(notes=[72]) >> HueSoloRed,
        ],
        # Controle du POD HD500 
        Filter(NOTEON) >> [
            KeyFilter(notes=[69]) >> FS4,
            KeyFilter(notes=[71]) >> [FS1, Ctrl(3,100) >> Expr2],
            KeyFilter(notes=[72]) >> [FS1, Ctrl(3,120) >> Expr2],
        ],
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

# ---
# Helpers
p_recorder = (pk5 >> 
        [
            Filter(NOTEON) >> KeyFilter(notes=[60]) >> [CakePlay],
            Filter(NOTEON) >> KeyFilter(notes=[62]) >> [CakeRecord],
            Filter(NOTEOFF) >> HueGalaxieMax, 
        ])
# ---

# FUTUR TESTS

# Glissando
p_glissando=(Filter(NOTEON) >> Call(glissando, 48, 84, 100, 0.01, -1, 'SD90-PART-A'))

# PORTAMENTO 
#portamento_base=Ctrl(1,1,5,50)
#portamento_off=Ctrl(1,1,65,0)	# Switch OFF
#portamento_on=Ctrl(1,1,65,127)  # Switch ON
#portamento_up=(portamento_base // portamento_on)
#portamento_off=(portamento_base // portamento_off)
#legato=Ctrl(1,1,120,0)
