# Simple output patch for testing equipment
q49=cf >> Output('D4', channel=1, program=1, volume=100)
pk5=cf >> Output('PK5', channel=2, program=1, volume=100)
d4=cf >> Output('Q49', channel=10, program=1, volume=100)

# FX Section
explosion = cf >> Key(0) >> Velocity(fixed=100) >> Output('PK5', channel=1, program=((96*128)+3,128), volume=100)
#--------------------------------------------------------------------

# Patch Synth. generique pour Barchetta, FreeWill, Limelight etc...
keysynth = cf >> Velocity(fixed=80) >> Output('PK5', channel=3, program=((96*128),51), volume=100, ctrls={93:75, 91:75})
#--------------------------------------------------------------------

# Patch Syhth. generique pour lowbase
lowsynth = cf >> Velocity(fixed=100) >> Output('PK5', channel=1, program=51, volume=100, ctrls={93:75, 91:75})
lowsynth2 = cf >> Velocity(fixed=115) >> Output('PK5', channel=1, program=51, volume=115, ctrls={93:75, 91:75})
#--------------------------------------------------------------------

# Patch Closer to the hearth 
closer_high = Output('Q49', channel=1, program=((99*128),15), volume=100)
closer_base = Velocity(fixed=100) >> Output('PK5', channel=2, program=((99*128),51), volume=100)
closer_main = cf >> KeySplit('c3', closer_base, closer_high)
#--------------------------------------------------------------------

# Patch Time Stand Still
tss_high = Velocity(fixed=90) >> Output('Q49', channel=3, program=((99*128),92), volume=80)
tss_base = Transpose(12) >> Velocity(fixed=90) >> Output('Q49', channel=3, program=((99*128),92), volume=100)
tss_keyboard_main = cf >> KeySplit('c2', tss_base, tss_high)

tss_foot_left = Transpose(-12) >> Velocity(fixed=75) >> Output('PK5', channel=2, program=((99*128),103), volume=100)
tss_foot_right = Transpose(-24) >> Velocity(fixed=75) >> Output('PK5', channel=2, program=((99*128),103), volume=100)
tss_foot_main = cf >> KeySplit('d#3', tss_foot_left, tss_foot_right)
#--------------------------------------------------------------------

# Patch Analog Kid
#analogkid = cf >> Transpose(-12) >> Harmonize('c', 'major', ['unison', 'third', 'fifth', 'octave']) >> Velocity(fixed=100) >> Output('PK5', channel=1, program=((99*128),50), volume=100)
analogkid = cf >> Transpose(-12) >> Harmonize('c', 'major', ['unison', 'third', 'fifth', 'octave']) >> Output('PK5', channel=1, program=((98*128),53), volume=100)
analogkid_ending = cf >> Key('a1') >> Output('PK5', channel=5, program=((81*128),68), volume=100)
#--------------------------------------------------------------------

# Patch Limelight
limelight = cf >> Key('d#6') >> Output('PK5', channel=16, program=((80*128),12), volume=100)

# Patch Centurion
centurion_synth = (Velocity(fixed=110) >> 
	(
		Output('PK5', channel=1, program=((99*128),96), volume=110) // 
		Output('PK5', channel=2, program=((99*128),82), volume=110)
	))

# Patch Centurion Video
centurion_video=( System('./vp.sh /mnt/flash/live/video/centurion_silent.avi') )

# Patch Centurion Hack 
centurion_patch=(cf >> LatchNotes(True,reset='C3') >>
	(
		(KeyFilter('D3') >> Key('D1')) // 
		(KeyFilter('E3') >> Key('D2')) // 
		(KeyFilter('F3') >> Key('D3')) //
		(KeyFilter('G3') >> Key('D4')) //
		(KeyFilter('A3') >> Key('D5'))
	) >> centurion_synth)

# Hack D4 - Closer to the heart
closer_celesta_d4 = (
	(
		Velocity(fixed=100) >> Output('D4', channel=1, program=((98*128),9), volume=110) //
		(Velocity(fixed=80) >> Transpose(-72) >> Output('PK5', channel=2, program=((99*128)+1,92), volume=50))
	))

closer_patch_celesta_d4=(cf >> 
    (
		(~KeyFilter(notes=[36,38,40,41,43,45])) //
    	(KeyFilter('C1') >> Key('A6')) //
    	(KeyFilter('D1') >> Key('G6')) //
    	(KeyFilter('E1') >> Key('D7')) //
    	(KeyFilter('F1') >> Key('F6')) //
    	(KeyFilter('G1') >> Key('B6')) //
    	(KeyFilter('A1') >> Key('C#7')) 
   ) >> closer_celesta_d4)

closer_bell_d4 = Velocity(fixed=100) >> Output('D4', channel=1, program=((99*128),15), volume=100)
closer_patch_d4=(cf >> 
    (
		(~KeyFilter(notes=[36,38,40,41,43,45])) //
    	(KeyFilter('C1') >> Key('D4')) //
    	(KeyFilter('D1') >> Key('A3')) //
    	(KeyFilter('E1') >> Key('G3')) //
    	(KeyFilter('F1') >> Key('F#3')) 
   ) >> closer_bell_d4)
