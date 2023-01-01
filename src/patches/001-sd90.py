#
# The EDIROL SD-90 Studio Canvas sound module definition patches for mididings (not fully implemented)
#

factor = 128

'''
Inst part: 
80(50H) = Special 1 set
81(51H) = Special 2 set
96(60H) = Classical set
97(61H) = Contemporary set
98(62H) = Solo set
99(63H) = Enhanced set
'''
Special1=80*factor
Special2=81*factor
Classical=96*factor
Contemporary=97*factor
Solo=98*factor
Enhanced=99*factor

'''
Drum part: 
104(60H) = Classical set
105(61H) = Contemporary set
106(62H) = Solo set
107(63H) = Enhanced set
'''
ClassicalDrum=104*factor
ContemporaryDrum=105*factor
SoloDrum=106*factor
EnhancedDrum=107*factor

'''
Variation
'''
Var1=1
Var2=2
Var3=3
Var4=4
Var5=5
Var6=6
Var7=7
Var8=8
Var9=9

# Configure PitchBend Sensitivity
# SD-90 Part A - All Channel
#      * RPN MSB/LSB 0 = PitchBendSens ****  //  ****** DataEntry 12 tone *******
PB_A01 = (Ctrl('SD90-PART-A', 1, 100, 0) // Ctrl('SD90-PART-A', 1, 101, 0) // Ctrl('SD90-PART-A', 1, 6, 12) // Ctrl('SD90-PART-A', 1, 38, 0))
PB_A02 = (Ctrl('SD90-PART-A', 2, 100, 0) // Ctrl('SD90-PART-A', 2, 101, 0) // Ctrl('SD90-PART-A', 2, 6, 12) // Ctrl('SD90-PART-A', 2, 38, 0))
PB_A03 = (Ctrl('SD90-PART-A', 3, 100, 0) // Ctrl('SD90-PART-A', 3, 101, 0) // Ctrl('SD90-PART-A', 3, 6, 12) // Ctrl('SD90-PART-A', 3, 38, 0))
PB_A04 = (Ctrl('SD90-PART-A', 4, 100, 0) // Ctrl('SD90-PART-A', 4, 101, 0) // Ctrl('SD90-PART-A', 4, 6, 12) // Ctrl('SD90-PART-A', 4, 38, 0))
PB_A05 = (Ctrl('SD90-PART-A', 5, 100, 0) // Ctrl('SD90-PART-A', 5, 101, 0) // Ctrl('SD90-PART-A', 5, 6, 12) // Ctrl('SD90-PART-A', 5, 38, 0))
PB_A06 = (Ctrl('SD90-PART-A', 6, 100, 0) // Ctrl('SD90-PART-A', 6, 101, 0) // Ctrl('SD90-PART-A', 6, 6, 12) // Ctrl('SD90-PART-A', 6, 38, 0))
PB_A07 = (Ctrl('SD90-PART-A', 7, 100, 0) // Ctrl('SD90-PART-A', 7, 101, 0) // Ctrl('SD90-PART-A', 7, 6, 12) // Ctrl('SD90-PART-A', 7, 38, 0))
PB_A08 = (Ctrl('SD90-PART-A', 8, 100, 0) // Ctrl('SD90-PART-A', 8, 101, 0) // Ctrl('SD90-PART-A', 8, 6, 12) // Ctrl('SD90-PART-A', 8, 38, 0))
PB_A09 = (Ctrl('SD90-PART-A', 9, 100, 0) // Ctrl('SD90-PART-A', 9, 101, 0) // Ctrl('SD90-PART-A', 9, 6, 12) // Ctrl('SD90-PART-A', 9, 38, 0))
PB_A10 = (Ctrl('SD90-PART-A', 10, 100, 0) // Ctrl('SD90-PART-A', 10, 101, 0) // Ctrl('SD90-PART-A', 10, 6, 12) // Ctrl('SD90-PART-A', 10, 38, 0))
PB_A11 = (Ctrl('SD90-PART-A', 11, 100, 0) // Ctrl('SD90-PART-A', 11, 101, 0) // Ctrl('SD90-PART-A', 11, 6, 12) // Ctrl('SD90-PART-A', 11, 38, 0))
PB_A12 = (Ctrl('SD90-PART-A', 12, 100, 0) // Ctrl('SD90-PART-A', 12, 101, 0) // Ctrl('SD90-PART-A', 12, 6, 12) // Ctrl('SD90-PART-A', 12, 38, 0))
PB_A13 = (Ctrl('SD90-PART-A', 13, 100, 0) // Ctrl('SD90-PART-A', 13, 101, 0) // Ctrl('SD90-PART-A', 13, 6, 12) // Ctrl('SD90-PART-A', 13, 38, 0))
PB_A14 = (Ctrl('SD90-PART-A', 14, 100, 0) // Ctrl('SD90-PART-A', 14, 101, 0) // Ctrl('SD90-PART-A', 14, 6, 12) // Ctrl('SD90-PART-A', 14, 38, 0))
PB_A15 = (Ctrl('SD90-PART-A', 15, 100, 0) // Ctrl('SD90-PART-A', 15, 101, 0) // Ctrl('SD90-PART-A', 15, 6, 12) // Ctrl('SD90-PART-A', 15, 38, 0))
PB_A16 = (Ctrl('SD90-PART-A', 16, 100, 0) // Ctrl('SD90-PART-A', 16, 101, 0) // Ctrl('SD90-PART-A', 16, 6, 12) // Ctrl('SD90-PART-A', 16, 38, 0))

# SD-90 Part B - All Channel
PB_B01 = (Ctrl('SD90-PART-B', 1, 100, 0) // Ctrl('SD90-PART-B', 1, 101, 0) // Ctrl('SD90-PART-B', 1, 6, 12) // Ctrl('SD90-PART-B', 1, 38, 0))
PB_B02 = (Ctrl('SD90-PART-B', 2, 100, 0) // Ctrl('SD90-PART-B', 2, 101, 0) // Ctrl('SD90-PART-B', 2, 6, 12) // Ctrl('SD90-PART-B', 2, 38, 0))
PB_B03 = (Ctrl('SD90-PART-B', 3, 100, 0) // Ctrl('SD90-PART-B', 3, 101, 0) // Ctrl('SD90-PART-B', 3, 6, 12) // Ctrl('SD90-PART-B', 3, 38, 0))
PB_B04 = (Ctrl('SD90-PART-B', 4, 100, 0) // Ctrl('SD90-PART-B', 4, 101, 0) // Ctrl('SD90-PART-B', 4, 6, 12) // Ctrl('SD90-PART-B', 4, 38, 0))
PB_B05 = (Ctrl('SD90-PART-B', 5, 100, 0) // Ctrl('SD90-PART-B', 5, 101, 0) // Ctrl('SD90-PART-B', 5, 6, 12) // Ctrl('SD90-PART-B', 5, 38, 0))
PB_B06 = (Ctrl('SD90-PART-B', 6, 100, 0) // Ctrl('SD90-PART-B', 6, 101, 0) // Ctrl('SD90-PART-B', 6, 6, 12) // Ctrl('SD90-PART-B', 6, 38, 0))
PB_B07 = (Ctrl('SD90-PART-B', 7, 100, 0) // Ctrl('SD90-PART-B', 7, 101, 0) // Ctrl('SD90-PART-B', 7, 6, 12) // Ctrl('SD90-PART-B', 7, 38, 0))
PB_B08 = (Ctrl('SD90-PART-B', 8, 100, 0) // Ctrl('SD90-PART-B', 8, 101, 0) // Ctrl('SD90-PART-B', 8, 6, 12) // Ctrl('SD90-PART-B', 8, 38, 0))
PB_B09 = (Ctrl('SD90-PART-B', 9, 100, 0) // Ctrl('SD90-PART-B', 9, 101, 0) // Ctrl('SD90-PART-B', 9, 6, 12) // Ctrl('SD90-PART-B', 9, 38, 0))
PB_B10 = (Ctrl('SD90-PART-B', 10, 100, 0) // Ctrl('SD90-PART-B', 10, 101, 0) // Ctrl('SD90-PART-B', 10, 6, 12) // Ctrl('SD90-PART-B', 10, 38, 0))
PB_B11 = (Ctrl('SD90-PART-B', 11, 100, 0) // Ctrl('SD90-PART-B', 11, 101, 0) // Ctrl('SD90-PART-B', 11, 6, 12) // Ctrl('SD90-PART-B', 11, 38, 0))
PB_B12 = (Ctrl('SD90-PART-B', 12, 100, 0) // Ctrl('SD90-PART-B', 12, 101, 0) // Ctrl('SD90-PART-B', 12, 6, 12) // Ctrl('SD90-PART-B', 12, 38, 0))
PB_B13 = (Ctrl('SD90-PART-B', 13, 100, 0) // Ctrl('SD90-PART-B', 13, 101, 0) // Ctrl('SD90-PART-B', 13, 6, 12) // Ctrl('SD90-PART-B', 13, 38, 0))
PB_B14 = (Ctrl('SD90-PART-B', 14, 100, 0) // Ctrl('SD90-PART-B', 14, 101, 0) // Ctrl('SD90-PART-B', 14, 6, 12) // Ctrl('SD90-PART-B', 14, 38, 0))
PB_B15 = (Ctrl('SD90-PART-B', 15, 100, 0) // Ctrl('SD90-PART-B', 15, 101, 0) // Ctrl('SD90-PART-B', 15, 6, 12) // Ctrl('SD90-PART-B', 15, 38, 0))
PB_B16 = (Ctrl('SD90-PART-B', 16, 100, 0) // Ctrl('SD90-PART-B', 16, 101, 0) // Ctrl('SD90-PART-B', 16, 6, 12) // Ctrl('SD90-PART-B', 16, 38, 0))

InitPitchBend = (
        PB_B01 // PB_B02 // PB_B03 // PB_B04 // PB_B05 // PB_B06 // PB_B07 // PB_B08 //
        PB_B09 // PB_B10 // PB_B11 // PB_B12 // PB_B13 // PB_B14 // PB_B15 // PB_B16 //
        PB_A01 // PB_A02 // PB_A03 // PB_A04 // PB_A05 // PB_A06 // PB_A07 // PB_A08 //
        PB_A09 // PB_A10 // PB_A11 // PB_A12 // PB_A13 // PB_A14 // PB_A15 // PB_A16)

# --------------------------------------------
# SD-90 # DRUM MAPPING
# --------------------------------------------

# Classical Set
StandardSet =  Output('SD90-PART-A', channel=10, program=(ClassicalDrum, 1))
RoomSet =  Output('SD90-PART-A', channel=10, program=(ClassicalDrum, 9))
PowerSet =  Output('SD90-PART-A', channel=10, program=(ClassicalDrum, 17))
ElectricSet =  Output('SD90-PART-A', channel=10, program=(ClassicalDrum, 25))
AnalogSet =  Output('SD90-PART-A', channel=10, program=(ClassicalDrum, 26))
JazzSet =  Output('SD90-PART-A', channel=10, program=(ClassicalDrum, 33))
BrushSet =  Output('SD90-PART-A', channel=10, program=(ClassicalDrum, 41))
OrchestraSet =  Output('SD90-PART-A', channel=10, program=(ClassicalDrum, 49))
SFXSet =  Output('SD90-PART-A', channel=10, program=(ClassicalDrum, 57))

# Contemporary Set
StandardSet2 =  Output('SD90-PART-A', channel=10, program=(ContemporaryDrum, 1))
RoomSet2 =  Output('SD90-PART-A', channel=10, program=(ContemporaryDrum, 9))
PowerSet2 =  Output('SD90-PART-A', channel=10, program=(ContemporaryDrum, 17))
DanceSet =  Output('SD90-PART-A', channel=10, program=(ContemporaryDrum, 25))
RaveSet =  Output('SD90-PART-A', channel=10, program=(ContemporaryDrum, 26))
JazzSet2 =  Output('SD90-PART-A', channel=10, program=(ContemporaryDrum, 33))
BrushSet2 =  Output('SD90-PART-A', channel=10, program=(ContemporaryDrum, 41))

# Solo Set
St_Standard =  Output('SD90-PART-A', channel=10, program=(SoloDrum, 1))
St_Room =  Output('SD90-PART-A', channel=10, program=(SoloDrum, 9))
St_Power =  Output('SD90-PART-A', channel=10, program=(SoloDrum, 17))
RustSet =  Output('SD90-PART-A', channel=10, program=(SoloDrum, 25))
Analog2Set =  Output('SD90-PART-A', channel=10, program=(SoloDrum, 26))
St_Jazz =  Output('SD90-PART-A', channel=10, program=(SoloDrum, 33))
St_Brush =  Output('SD90-PART-A', channel=10, program=(SoloDrum, 41))

# Enhanced Set
Amb_Standard =  Output('SD90-PART-A', channel=10, program=(EnhancedDrum, 1))
Amb_Room =  Output('SD90-PART-A', channel=10, program=(EnhancedDrum, 9))
GatedPower =  Output('SD90-PART-A', channel=10, program=(EnhancedDrum, 17))
TechnoSet =  Output('SD90-PART-A', channel=10, program=(EnhancedDrum, 25))
BullySet =  Output('SD90-PART-A', channel=10, program=(EnhancedDrum, 26))
Amb_Jazz =  Output('SD90-PART-A', channel=10, program=(EnhancedDrum, 33))
Amb_Brush =  Output('SD90-PART-A', channel=10, program=(EnhancedDrum, 41))

# WIP SD-90 Full Patch implementation 
# Special 1 instrument part
DLAPad=Output('SD90-PART-A', channel=1, program=(Special1, 1))
BrushingSaw=Output('SD90-PART-A', channel=1, program=(Special1, 2))
Xtremities=Output('SD90-PART-A', channel=1, program=(Special1, 3))
Atmostrings=Output('SD90-PART-A', channel=1, program=(Special1, 4))
NooTongs=Output('SD90-PART-A', channel=1, program=(Special1, 5))
Mistery=Output('SD90-PART-A', channel=1, program=(Special1, 6))
EastrnEurope=Output('SD90-PART-A', channel=1, program=(Special1, 7))
HarpsiAndStr=Output('SD90-PART-A', channel=1, program=(Special1, 8))
ShoutGt=Output('SD90-PART-A', channel=1, program=(Special1,9))
CleanChorus=Output('SD90-PART-A', channel=1, program=(Special1, 10))
MidBoostGt=Output('SD90-PART-A', channel=1, program=(Special1, 11))
Guitarvibe=Output('SD90-PART-A', channel=1, program=(Special1, 12))
ClusterSect=Output('SD90-PART-A', channel=1, program=(Special1, 13))
MariachiTp=Output('SD90-PART-A', channel=1, program=(Special1, 14))
NYTenor=Output('SD90-PART-A', channel=1, program=(Special1, 15))
JazzClub=Output('SD90-PART-A', channel=1, program=(Special1, 16))
MoodyAlto=Output('SD90-PART-A', channel=1, program=(Special1, 17))
FujiYama=Output('SD90-PART-A', channel=1, program=(Special1, 18))
SDPiano=Output('SD90-PART-A', channel=1, program=(Special1, 19))

# Special 2 instrument part
RichChoir=Output('SD90-PART-A', channel=1, program=(Special2, 18))
OBBorealis=Output('SD90-PART-A', channel=1, program=(Special2, 80))
VintagePhase=Output('SD90-PART-A', channel=1, program=(Special2, 82))
FifthAtmAft=Output('SD90-PART-A', channel=1, program=(Special2, 85))
Borealis=Output('SD90-PART-A', channel=1, program=(Special2, 106))
CircularPad=Output('SD90-PART-A', channel=1, program=(Special2, 107))
Oxigenizer=Output('SD90-PART-A', channel=1, program=(Special2, 108))
Quasar=Output('SD90-PART-A', channel=1, program=(Special2, 109))
HellSection=Output('SD90-PART-A', channel=1, program=(Special2, 111))


# Classical instrument part
BirdTweet=Output('SD90-PART-B', channel=4, program=(Classical, 124))
Applause=Output('SD90-PART-B', channel=8, program=(Classical, 127))

# Classical instrument part - Variation 1
Itopia=Output('SD90-PART-B', channel=1, program=(Classical+Var1, 92))
Kalimba=Output('SD90-PART-B', channel=1, program=(Classical+Var1, 109))
BagPipe=Output('SD90-PART-B', channel=1, program=(Classical+Var1, 110))
Dog=Output('SD90-PART-B', channel=14, program=(Classical+Var1, 124))
Telephone2=Output('SD90-PART-B', channel=1, program=(Classical+Var1, 125))
CarEngine=Output('SD90-PART-B', channel=1, program=(Classical+Var1, 126))
Laughing=Output('SD90-PART-B', channel=1, program=(Classical+Var1, 127))

# Classical instrument part - Variation 2
Screaming=Output('SD90-PART-B', channel=13, program=(Classical+Var2, 127))
DoorCreak=Output('SD90-PART-B', channel=1, program=(Classical+Var2, 125))
Thunder=Output('SD90-PART-B', channel=15, program=(Classical+Var2, 123))

# Classical instrument part - Variation 3
Wind=Output('SD90-PART-B', channel=3, program=(Classical+Var3, 123))
Explosion=Output('SD90-PART-B', channel=7, program=(Classical+Var3, 128))

# Classical instrument part - Variation 4
Stream=Output('SD90-PART-B', channel=12, program=(Classical+Var4, 123))


# Classical instrument part - Variation 5
Siren=Output('SD90-PART-B', channel=5, program=(Classical+Var5, 126))
Bubble=Output('SD90-PART-B', channel=1, program=(Classical+Var5, 123))

# Classical instrument part - Variation 6
Train=Output('SD90-PART-B', channel=6, program=(Classical+Var6, 126))

# Classical instrument part - Variation 7
Jetplane=Output('SD90-PART-B', channel=1, program=(Classical+Var7, 126))

# Classical instrument part - Variation 8
Starship=Output('SD90-PART-B', channel=1, program=(Classical+Var8, 126))

# Contemporary instrument part
Helicpoter=Output('SD90-PART-B', channel=1, program=(Contemporary, 126))
Seashore=Output('SD90-PART-B', channel=2, program=(Contemporary, 123))

# Contemporary instrument part - Variation 1
Rain=Output('SD90-PART-B', channel=1, program=(Contemporary+Var1, 123))


### End SD-90 Patch list
# -------------------------------------------------------------------
# SD Mixer config 
Reset = '\xF0\x41\x10\x00\x48\x12\x00\x00\x00\x00\x00\x00\xF7'
MixToAfx = '\xF0\x41\x10\x00\x48\x12\x02\x10\x10\x00\x06\x58\xF7'
MasterEffect = '\xF0\x41\x10\x00\x48\x12\x02\x10\x20\x00\x78\x56\xF7'

SD90_Initialize = (SysEx(Reset) // SysEx(MixToAfx) // SysEx(MasterEffect) // InitPitchBend)
