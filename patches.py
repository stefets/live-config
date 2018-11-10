#-----------------------------------------------------------------------------------------------
# PROGRAM CHANGE SECTION
#-----------------------------------------------------------------------------------------------
POD_16A=Program('PODHD500', channel=9, program=61)
POD_16B=Program('PODHD500', channel=9, program=62)
POD_16C=Program('PODHD500', channel=9, program=63)
POD_16D=Program('PODHD500', channel=9, program=64)

# Simple output patch for testing equipment
q49=cf >> Output('Q49', channel=1, program=1, volume=100)
pk5=cf >> Output('PK5', channel=2, program=1, volume=100)
pk5_drum=cf >> Channel(10) >> Transpose(-24) >> Output('PK5', channel=10, program=1, volume=100)
d4=cf >> Output('D4', channel=10, program=1, volume=100)
d4_tom=cf >> Output('D4', channel=11, program=((96*128)+1,118), volume=100)
pod_base=Output('PODHD500', channel=9)

# POD HD500
POD=OutputTemplate('PODHD500',9)
#pod_init=Output('PODHD500', channel=9, program=1)
#pod_init=POD(64)
#pod_init=Init(POD(64))
pod_off=Output('PODHD500', channel=9, ctrls={51:127,52:127,53:127,54:127,})
pod_on=Output('PODHD500', channel=9, ctrls={51:0,52:0,53:0,54:0,})

# FX Section
explosion = cf >> Key(0) >> Velocity(fixed=100) >> Output('PK5', channel=1, program=((96*128)+3,128), volume=100)
#--------------------------------------------------------------------
nf_piano = Output('Q49', channel=1, program=((96*128),2), volume=100)
piano = cf >> Velocity(fixed=80) >> Output('Q49', channel=1, program=((96*128),1), volume=100)
piano2 = Output('PK5', channel=2, program=((96*128),2), volume=100)

# Patch Synth. generique pour Barchetta, FreeWill, Limelight etc...
keysynth = cf >> Velocity(fixed=80) >> Output('PK5', channel=3, program=((96*128),51), volume=100, ctrls={93:75, 91:75})
#--------------------------------------------------------------------

# Patch Marathon (INTRO) - Accept (B4, B3) and E4 => transformed to a chord 
marathon=(cf >> LatchNotes(False,reset='c5') >> Velocity(fixed=110) >>
	( 
		(KeyFilter('e4') >> Harmonize('e','major',['unison', 'fifth'])) //
		(KeyFilter(notes=[71, 83])) 
	) >> Transpose(0) >> Output('PK5', channel=3, program=((96*128),51), volume=110, ctrls={93:75, 91:75}))

marathon_chords=(cf>> LatchNotes(False, reset='b3') >> Velocity(fixed=100) >>
	(

		# From first to last...
		(KeyFilter('e3') >> Key('b3') >> Harmonize('b','major',['unison', 'third', 'fifth', 'octave'])) //
		(KeyFilter('c3') >> Key('e3') >> Harmonize('e','major',['unison', 'third', 'fifth', 'octave'])) //
		(KeyFilter('d3') >> Key('f#3') >> Harmonize('f#','major',['unison', 'third', 'fifth', 'octave'])) //

		# From first to last 2 frets higher
		(KeyFilter('a3') >> Key('c#4') >> Harmonize('c#','major',['unison', 'third', 'fifth', 'octave'])) //
		(KeyFilter('f3') >> Key('f#3') >> Harmonize('f#','major',['unison', 'third', 'fifth', 'octave'])) //
		(KeyFilter('g3') >> Key('g#3') >> Harmonize('g#','major',['unison', 'third', 'fifth', 'octave']))

	) >> Transpose(-12) >> Output('PK5', channel=3, program=((96*128),51), volume=80, ctrls={93:75, 91:75}))

marathon_bridge=(cf >> 
	( 
		(KeyFilter('c3') >> Key('b2') >> Harmonize('b','minor',['unison', 'third', 'fifth'])) //
		(KeyFilter('e3') >> Key('f#3') >> Harmonize('f#','minor',['unison', 'third', 'fifth' ])) //
		(KeyFilter('d3') >> Key('e3') >> Harmonize('e','major',['unison', 'third', 'fifth']))  //
		(KeyFilter('a4'))
	) >> Output('PK5', channel=3, program=((96*128),51), volume=110, ctrls={93:75, 91:75}))

# Solo bridge, lower -12
marathon_bridge2=(cf >> 
	( 
		(KeyFilter('c3') >> Key('b2') >> Harmonize('b','minor',['unison', 'third', 'fifth'])) //
		(KeyFilter('d3') >> Key('e2') >> Harmonize('e','major',['unison', 'third', 'fifth'])) 
	) >> Transpose(-12) >> Output('PK5', channel=3, program=((96*128),51), volume=110, ctrls={93:75, 91:75}))

#marathon_main_out=Output('PK5', channel=3, program=((96*128),51), volume=80, ctrls={93:75, 91:75}))

# Patch Syhth. generique pour lowbase
lowsynth = cf >> Velocity(fixed=100) >> Output('PK5', channel=1, program=((96*128),51), volume=100, ctrls={93:75, 91:75})
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
analog_pod2=(
	(Filter(NOTEON) >> (KeyFilter('c3') % Ctrl(51,0)) >> Output('PODHD500',9)) //
	(Filter(NOTEON) >> (KeyFilter('d3') % Ctrl(51,127)) >> Output('PODHD500',9))
)
analog_pod=(Filter(NOTEON) >> (KeyFilter('c3') % Ctrl(51,27)) >> Output('PODHD500',9))

mission= LatchNotes(False,reset='c#3')  >> Transpose(-12) >>Harmonize('c','major',['unison', 'third', 'fifth', 'octave']) >> Output('PK5',channel=1,program=((98*128),53),volume=100,ctrls={91:75})

analogkid_low= (LatchNotes(False,reset='c#3') >>
	( 
		(KeyFilter('c3:d#3') >> Transpose(-7) >> Harmonize('c','major',['unison', 'third', 'fifth', 'octave'])) //
		(KeyFilter('e3') >> Key('a3')) 
	) >> Output('PK5',channel=1,program=((98*128),53),volume=100,ctrls={91:75}))
analogkid_high = Output('PK5', channel=2, program=((98*128),53), volume=100, ctrls={93:75, 91:100})
analogkid_main = cf >> KeySplit('f3', analogkid_low, analogkid_high)

#analogkid_ending = cf >> Key('a1') >> Output('PK5', channel=5, program=((81*128),68), volume=100)

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

# PAD SECTION --------------------------------------------------------------------------------------------------

# Hack D4 - Closer to the heart
closer_celesta_d4 =Velocity(fixed=100) >> Output('D4', channel=1, program=((98*128),11), volume=110)
#closer_celesta_d4 = (
#	(
#		Velocity(fixed=100) >> Output('D4', channel=1, program=((98*128),11), volume=110) //
#		(Velocity(fixed=100) >> Transpose(-72) >> Output('PK5', channel=2, program=((99*128),96), volume=80))
#	))

closer_patch_celesta_d4=(cf >> 
    (
		(~KeyFilter(notes=[36,38,40,41,43,45])) //
    	(KeyFilter('C1') >> Key('A5')) //
    	(KeyFilter('D1') >> Key('B5')) //
    	(KeyFilter('E1') >> Key('G5')) //
    	(KeyFilter('F1') >> Key('D6')) //
    	(KeyFilter('G1') >> Key('F5')) //
    	(KeyFilter('A1') >> Key('C#6')) 
   ) >> closer_celesta_d4)

#closer_patch_celesta_d4=(cf >> 
#    (
#		(~KeyFilter(notes=[36,38,40,41,43,45])) //
#    	(KeyFilter('C1') >> Key('A5')) //
#    	(KeyFilter('D1') >> Key('G5')) //
#    	(KeyFilter('E1') >> Key('D6')) //
#    	(KeyFilter('F1') >> Key('F5')) //
#    	(KeyFilter('G1') >> Key('B5')) //
#    	(KeyFilter('A1') >> Key('C#6')) 
#   ) >> closer_celesta_d4)

closer_bell_d4 = Velocity(fixed=100) >> Output('D4', channel=1, program=((99*128),15), volume=100)
closer_patch_d4=(cf >> 
    (
		(~KeyFilter(notes=[36,38,40,41,43,45])) //
    	(KeyFilter('C1') >> Key('D4')) //
    	(KeyFilter('E1') >> Key('A3')) //
    	(KeyFilter('G1') >> Key('G3')) //
    	(KeyFilter('D1') >> Key('F#3')) 
   ) >> closer_bell_d4)

# YYZ
yyz_bell=Output('D4', channel=10, program=1, volume=100)
yyz=(cf >>
	(
		(KeyFilter('A1') >> Key('A4')) //
		(KeyFilter('F1') >> Key('G#4')) 
	) >> yyz_bell)

# Time Stand Steel
# Instruments
d4_melo_tom=Velocity(fixed=100) >> Output('D4', channel=11, program=((99*128)+1,118), volume=100)
d4_castanet=Velocity(fixed=100) >> Output('D4', channel=12, program=((99*128)+1,116), volume=100)
d4_808_tom=Velocity(fixed=80) >> Output('D4', channel=13, program=((99*128)+1,119), volume=100)

# Sons 1 et 2
tss_d4_melo_tom_A=cf >>KeyFilter('E1') >> Key('E6') >> d4_melo_tom

# Son 3
tss_d4_castanet=cf >>KeyFilter('G1') >> Key('a#2') >> d4_castanet

# Son 4
tss_d4_melo_tom_B=cf >>KeyFilter('F1') >> Key('a4') >> d4_808_tom

# Son 5
tss_d4_808_tom=cf >>KeyFilter('A1') >> Key('f#5') >> d4_808_tom

#--------------------------------------------
# SD-90 # DRUM MAPPING
#--------------------------------------------
# Classical Set
StandardSet=cf>>Output('PK5',channel=10,program=(13312,1))
RoomSet=cf>>Output('PK5',channel=10,program=(13312,9))
PowerSet=cf>>Output('PK5',channel=10,program=(13312,17))
ElectricSet=cf>>Output('PK5',channel=10,program=(13312,25))
AnalogSet=cf>>Output('PK5',channel=10,program=(13312,26))
JazzSet=cf>>Output('PK5',channel=10,program=(13312,33))
BrushSet=cf>>Output('PK5',channel=10,program=(13312,41))
OrchestraSet=cf>>Output('PK5',channel=10,program=(13312,49))
SFXSet=cf>>Output('PK5',channel=10,program=(13312,57))
# Contemporary Set
StandardSet2=cf>>Output('PK5',channel=10,program=(13440,1))
RoomSet2=cf>>Output('PK5',channel=10,program=(13440,9))
PowerSet2=cf>>Output('PK5',channel=10,program=(13440,17))
DanceSet=cf>>Output('PK5',channel=10,program=(13440,25))
RaveSet=cf>>Output('PK5',channel=10,program=(13440,26))
JazzSet2=cf>>Output('PK5',channel=10,program=(13440,33))
BrushSet2=cf>>Output('PK5',channel=10,program=(13440,41))
# Solo Set
St_Standard=cf>>Output('PK5',channel=10,program=(13568,1))
St_Room=cf>>Output('PK5',channel=10,program=(13568,9))
St_Power=cf>>Output('PK5',channel=10,program=(13568,17))
RustSet=cf>>Output('PK5',channel=10,program=(13568,25))
Analog2Set=cf>>Output('PK5',channel=10,program=(13568,26))
St_Jazz=cf>>Output('PK5',channel=10,program=(13568,33))
St_Brush=cf>>Output('PK5',channel=10,program=(13568,41))
# Enhanced Set
Amb_Standard=cf>>Output('PK5',channel=10,program=(13696,1))
Amb_Room=cf>>Output('PK5',channel=10,program=(13696,9))
GatedPower=cf>>Output('PK5',channel=10,program=(13696,17))
TechnoSet=cf>>Output('PK5',channel=10,program=(13696,25))
BullySet=cf>>Output('PK5',channel=10,program=(13696,26))
Amb_Jazz=cf>>Output('PK5',channel=10,program=(13696,33))
Amb_Brush=cf>>Output('PK5',channel=10,program=(13696,41))
#-------------------------------------------------------------------
