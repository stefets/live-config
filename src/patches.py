#-----------------------------------------------------------------------------------------------
# PROGRAM CHANGE SECTION
#-----------------------------------------------------------------------------------------------
phantom=Velocity(fixed=0) >> Output('SD90-PART-A', channel=1, program=((96*128),1), volume=0)

# Works great in init_patch
#Chorus=Ctrl(3,1,93,127)
#Reverb =Ctrl(3,1,93,127)

# PORTAMENTO 
portamento_base=Ctrl(1,1,5,50)
portamento_off=Ctrl(1,1,65,0)	# Switch OFF
portamento_on=Ctrl(1,1,65,127)  # Switch ON
portamento_up=(portamento_base // portamento_on)
portamento_off=(portamento_base // portamento_off)

#Pas de resultat encore
#legato=Ctrl(1,1,120,0)

# Simple output patch for testing equipment
#SD90-PART-A= Output('SD90-PART-A', channel=1, program=1, volume=100)
#SD90-PART-A= Output('SD90-PART-A', channel=2, program=1, volume=100)
#SD90-PART-A_drum= Channel(10) >> Transpose(-24) >> Output('SD90-PART-A', channel=10, program=1, volume=100)
d4= Output('SD90-PART-A', channel=10, program=1, volume=100)
d4_tom= Output('SD90-PART-A', channel=11, program=((96*128)+1,118), volume=100)

# FX Section
explosion =  Key(0) >> Velocity(fixed=100) >> Output('SD90-PART-A', channel=1, program=((96*128)+3,128), volume=100)
#--------------------------------------------------------------------
violon = Output('SD90-PART-A', channel=1, program=((96*128),41))
piano_base =  Velocity(fixed=100) >> Output('SD90-PART-A', channel=1, program=((96*128),1))
nf_piano = Output('SD90-PART-A', channel=1, program=((96*128),2), volume=100)
piano =  Output('SD90-PART-A', channel=3, program=((96*128),1), volume=100)
piano2 = Output('SD90-PART-A', channel=2, program=((96*128),2), volume=100)

# Patch Synth
keysynth =  Velocity(fixed=80) >> Output('SD90-PART-A', channel=3, program=((96*128),51), volume=100, ctrls={93:75, 91:75})
#--------------------------------------------------------------------

# Patches for Marathon by Rush

# Accept (B4, B3) and E4 => transformed to a chord 
marathon_intro=(cme>>LatchNotes(False,reset='c5') >> Velocity(fixed=110) >>
	( 
		(KeyFilter('e4') >> Harmonize('e','major',['unison', 'fifth'])) //
		(KeyFilter(notes=[71, 83])) 
	) >> Output('SD90-PART-A', channel=3, program=((96*128),51), volume=110, ctrls={93:75, 91:75}))

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

	) >> Transpose(-24) >> Output('SD90-PART-A', channel=4, program=((96*128)+1,51), volume=100, ctrls={93:75, 91:75}))

marathon_bridge=(cme >>
	(
		(KeyFilter('c2') >> Key('b2') >> Harmonize('b','minor',['unison', 'third', 'fifth'])) //
		(KeyFilter('e2') >> Key('f#3') >> Harmonize('f#','minor',['unison', 'third', 'fifth' ])) //
		(KeyFilter('d2') >> Key('e3') >> Harmonize('e','major',['unison', 'third', 'fifth']))  
	) >> Velocity(fixed=75) >> Output('SD90-PART-A', channel=3, program=((96*128),51), volume=110, ctrls={93:75, 91:75}))

# Solo bridge, lower -12
marathon_bridge_lower=(cme >>
	(
		(KeyFilter('c1') >> Key('b1') >> Harmonize('b','minor',['unison', 'third', 'fifth'])) //
		(KeyFilter('d1') >> Key('e1') >> Harmonize('e','major',['third', 'fifth'])) //
		(KeyFilter('e1') >> Key('f#2') >> Harmonize('f#','minor',['unison', 'third', 'fifth' ]))
	) >> Velocity(fixed=90) >>  Output('SD90-PART-A', channel=4, program=((96*128),51), volume=75, ctrls={93:75, 91:75}))

# You can take the most
marathon_cascade=(cme >> KeyFilter('f3:c#5') >> Transpose(12) >> Velocity(fixed=50) >> Output('SD90-PART-B', channel=11, program=((99*128),99), volume=80))

marathon_bridge_split= KeySplit('f3', marathon_bridge_lower, marathon_cascade)

# Patch Syhth. generique pour lowbase
lowsynth =  Velocity(fixed=100) >> Output('SD90-PART-A', channel=1, program=((96*128),51), volume=100, ctrls={93:75, 91:75})
lowsynth2 =  Velocity(fixed=115) >> Output('SD90-PART-A', channel=1, program=51, volume=115, ctrls={93:75, 91:75})
#--------------------------------------------------------------------

# Patch Closer to the hearth 
closer_high = Output('SD90-PART-A', channel=1, program=((99*128),15), volume=100)
closer_base = Velocity(fixed=100) >> Output('SD90-PART-A', channel=2, program=((99*128),51), volume=100)
closer_main =  KeySplit('c3', closer_base, closer_high)
#--------------------------------------------------------------------

# Patch Time Stand Still
tss_high = Velocity(fixed=90) >> Output('SD90-PART-A', channel=3, program=((99*128),92), volume=80)
tss_base = Transpose(12) >> Velocity(fixed=90) >> Output('SD90-PART-A', channel=3, program=((99*128),92), volume=100)
tss_keyboard_main =  KeySplit('c2', tss_base, tss_high)

tss_foot_left = Transpose(-12) >> Velocity(fixed=75) >> Output('SD90-PART-A', channel=2, program=((99*128),103), volume=100)
tss_foot_right = Transpose(-24) >> Velocity(fixed=75) >> Output('SD90-PART-A', channel=2, program=((99*128),103), volume=100)
tss_foot_main =  KeySplit('d#3', tss_foot_left, tss_foot_right)

#--------------------------------------------------------------------

# Patch Analog Kid
#analog_pod2=(
#	(Filter(NOTEON) >> (KeyFilter('c3') % Ctrl(51,0)) >> Output('PODHD500',9)) //
#	(Filter(NOTEON) >> (KeyFilter('d3') % Ctrl(51,127)) >> Output('PODHD500',9))
#)
#analog_pod=(Filter(NOTEON) >> (KeyFilter('c3') % Ctrl(51,27)) >> Output('PODHD500',9))

mission= LatchNotes(False,reset='c#3')  >> Transpose(-12) >>Harmonize('c','major',['unison', 'third', 'fifth', 'octave']) >> Output('SD90-PART-A',channel=1,program=((98*128),53),volume=100,ctrls={91:75})

analogkid_low= (LatchNotes(False,reset='c#3') >>
	( 
		(KeyFilter('c3:d#3') >> Transpose(-7) >> Harmonize('c','major',['unison', 'third', 'fifth', 'octave'])) //
		(KeyFilter('e3') >> Key('a3')) 
	) >> Output('SD90-PART-A',channel=1,program=((98*128),53),volume=100,ctrls={91:75}))
analogkid_high = Output('SD90-PART-A', channel=2, program=((98*128),53), volume=100, ctrls={93:75, 91:100})
analogkid_main =  KeySplit('f3', analogkid_low, analogkid_high)

#analogkid_ending =  Key('a1') >> Output('SD90-PART-A', channel=5, program=((81*128),68), volume=100)

#--------------------------------------------------------------------

# Patch Limelight
limelight =  Key('d#6') >> Output('SD90-PART-A', channel=16, program=((80*128),12), volume=100)

# Patch Centurion
centurion_synth = (Velocity(fixed=110) >>
	(
		Output('SD90-PART-A', channel=1, program=((99*128),96), volume=110) // 
		Output('SD90-PART-A', channel=2, program=((99*128),82), volume=110)
	))

# Patch Centurion Video
# TODO Ajouter vp.sh dans la configuration json
centurion_video=( System('./vp.sh /mnt/flash/live/video/centurion_silent.avi') )

# Patch Centurion Hack 
centurion_patch=( LatchNotes(True,reset='C3') >>
	(
		(KeyFilter('D3') >> Key('D1')) //
		(KeyFilter('E3') >> Key('D2')) //
		(KeyFilter('F3') >> Key('D3')) //
		(KeyFilter('G3') >> Key('D4')) //
		(KeyFilter('A3') >> Key('D5'))
	) >> centurion_synth)

# PAD SECTION --------------------------------------------------------------------------------------------------

# Hack SD90-PART-A - Closer to the heart
closer_celesta_d4 =Velocity(fixed=100) >> Output('SD90-PART-A', channel=1, program=((98*128),11), volume=110)
#closer_celesta_d4 = (
#	(
#		Velocity(fixed=100) >> Output('SD90-PART-A', channel=1, program=((98*128),11), volume=110) //
#		(Velocity(fixed=100) >> Transpose(-72) >> Output('SD90-PART-A', channel=2, program=((99*128),96), volume=80))
#	))

closer_patch_celesta_d4=(
    (
		(~KeyFilter(notes=[36,38,40,41,43,45])) //
        (KeyFilter('C1') >> Key('A5')) //
        (KeyFilter('D1') >> Key('B5')) //
        (KeyFilter('E1') >> Key('G5')) //
        (KeyFilter('F1') >> Key('D6')) //
        (KeyFilter('G1') >> Key('F5')) //
        (KeyFilter('A1') >> Key('C#6'))
   ) >> closer_celesta_d4)


closer_bell_d4 = Velocity(fixed=100) >> Output('SD90-PART-A', channel=1, program=((99*128),15), volume=100)
closer_patch_d4=(
    (
		(~KeyFilter(notes=[36,38,40,41,43,45])) //
        (KeyFilter('C1') >> Key('D4')) //
        (KeyFilter('E1') >> Key('A3')) //
        (KeyFilter('G1') >> Key('G3')) //
        (KeyFilter('D1') >> Key('F#3'))
   ) >> closer_bell_d4)

# YYZ
yyz_bell=Output('SD90-PART-A', channel=10, program=1, volume=100)
yyz=(
	(
		(KeyFilter('A1') >> Key('A4')) //
		(KeyFilter('F1') >> Key('G#4')) 
	) >> yyz_bell)

# Time Stand Steel
# Instruments
d4_melo_tom=Velocity(fixed=100) >> Output('SD90-PART-A', channel=11, program=((99*128)+1,118), volume=100)
d4_castanet=Velocity(fixed=100) >> Output('SD90-PART-A', channel=12, program=((99*128)+1,116), volume=100)
d4_808_tom=Velocity(fixed=80) >> Output('SD90-PART-A', channel=13, program=((99*128)+1,119), volume=100)

# Sons 1 et 2
tss_d4_melo_tom_A=KeyFilter('E1') >> Key('E6') >> d4_melo_tom

# Son 3
tss_d4_castanet=KeyFilter('G1') >> Key('a#2') >> d4_castanet

# Son 4
tss_d4_melo_tom_B=KeyFilter('F1') >> Key('a4') >> d4_808_tom

# Son 5
tss_d4_808_tom=KeyFilter('A1') >> Key('f#5') >> d4_808_tom

# Band : Big Country ------------------------------------------
# Pour : In a big country
# Init patch
i_big_country = (
        U01_A // P14A // 
        Ctrl(hd500_port, hd500_channel, 1, 40) //
        Ctrl(hd500_port, hd500_channel, 2, 127))

# Execution patch
p_big_country = (pk5 >> Filter(NOTEON) >>
         (
             (KeyFilter(notes=[67]) >> Ctrl(hd500_port, hd500_channel, 2, 100)) //
             (KeyFilter(notes=[69]) >> Ctrl(hd500_port, hd500_channel, 54, 64)) //
             (KeyFilter(notes=[71]) >> (Ctrl(hd500_port, hd500_channel, 52, 64) // Ctrl(hd500_port, hd500_channel,2,100))) //
             (KeyFilter(notes=[72]) >> (Ctrl(hd500_port, hd500_channel, 52, 64) // Ctrl(hd500_port, hd500_channel,2,127)))
         ) >> Port('SD90-MIDI-OUT-1'))
# Big Country fin de section ------------------------------------------

# Band : Rush ------------------------------------------
# Pour : Subdivisions, The Trees
# Init patch
i_rush = (
        P02A // 
        Ctrl(hd500_port,hd500_channel, 1, 40))

# Execution patch
p_rush = (pk5 >> Filter(NOTEON) >>
         (
             (KeyFilter(notes=[69]) >> Ctrl(3,9,54, 64)) //
             (KeyFilter(notes=[71]) >> (Ctrl(3,9,51, 64) // Ctrl(3,9,54, 64) // Ctrl(3,9,2,100))) //
             (KeyFilter(notes=[72]) >> (Ctrl(3,9,51, 64) // Ctrl(3,9,54, 64) // Ctrl(3,9,2,120)))
         ) >> Port('SD90-MIDI-OUT-1'))

# Rush Grand Designs guitar patch
# notes=[67]=Toggle delay
# notes=[69]=Disto a 100, toggle delay
# notes=[71]=Disto a 127, toggle delay
# notes=[72]=On NOTEON disto = 127 else disto = 100
p_rush_gd = (ChannelFilter(pk5_channel) >> 
         [
            (Filter(NOTEON) >> (
                (KeyFilter(notes=[67]) >> Ctrl(3, 9, 54, 64)) //
                (KeyFilter(notes=[69]) >> [Ctrl(3, 9, 2, 100), Ctrl(3, 9, 54, 64)]) //
                (KeyFilter(notes=[71]) >> [Ctrl(3, 9, 2, 127), Ctrl(3, 9, 54, 64)]) //
                (KeyFilter(notes=[72]) >> [Ctrl(3, 9, 2, 127), Call(Hue(configuration['hue'], "GrandDesignsRed"))])
            )),
            (Filter(NOTEOFF) >> (
                (KeyFilter(notes=[72]) >> [Ctrl(3, 9, 2, 120), Call(Hue(configuration['hue'], "Galaxie"))])
            )),
        ] >> Port('SD90-MIDI-OUT-1'))


p_glissando=(Filter(NOTEON) >> Call(glissando, 24, 100, 100, 0.0125))

p_hue=Filter(NOTEON|NOTEOFF) >> Call(Hue(configuration['hue']))
