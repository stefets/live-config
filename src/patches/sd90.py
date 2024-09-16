
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
PB_A01 = (Ctrl(sd90_port_a, 1, 100, 0) // Ctrl(sd90_port_a, 1, 101, 0) // Ctrl(sd90_port_a, 1, 6, 12) // Ctrl(sd90_port_a, 1, 38, 0))
PB_A02 = (Ctrl(sd90_port_a, 2, 100, 0) // Ctrl(sd90_port_a, 2, 101, 0) // Ctrl(sd90_port_a, 2, 6, 12) // Ctrl(sd90_port_a, 2, 38, 0))
PB_A03 = (Ctrl(sd90_port_a, 3, 100, 0) // Ctrl(sd90_port_a, 3, 101, 0) // Ctrl(sd90_port_a, 3, 6, 12) // Ctrl(sd90_port_a, 3, 38, 0))
PB_A04 = (Ctrl(sd90_port_a, 4, 100, 0) // Ctrl(sd90_port_a, 4, 101, 0) // Ctrl(sd90_port_a, 4, 6, 12) // Ctrl(sd90_port_a, 4, 38, 0))
PB_A05 = (Ctrl(sd90_port_a, 5, 100, 0) // Ctrl(sd90_port_a, 5, 101, 0) // Ctrl(sd90_port_a, 5, 6, 12) // Ctrl(sd90_port_a, 5, 38, 0))
PB_A06 = (Ctrl(sd90_port_a, 6, 100, 0) // Ctrl(sd90_port_a, 6, 101, 0) // Ctrl(sd90_port_a, 6, 6, 12) // Ctrl(sd90_port_a, 6, 38, 0))
PB_A07 = (Ctrl(sd90_port_a, 7, 100, 0) // Ctrl(sd90_port_a, 7, 101, 0) // Ctrl(sd90_port_a, 7, 6, 12) // Ctrl(sd90_port_a, 7, 38, 0))
PB_A08 = (Ctrl(sd90_port_a, 8, 100, 0) // Ctrl(sd90_port_a, 8, 101, 0) // Ctrl(sd90_port_a, 8, 6, 12) // Ctrl(sd90_port_a, 8, 38, 0))
PB_A09 = (Ctrl(sd90_port_a, 9, 100, 0) // Ctrl(sd90_port_a, 9, 101, 0) // Ctrl(sd90_port_a, 9, 6, 12) // Ctrl(sd90_port_a, 9, 38, 0))
PB_A10 = (Ctrl(sd90_port_a, 10, 100, 0) // Ctrl(sd90_port_a, 10, 101, 0) // Ctrl(sd90_port_a, 10, 6, 12) // Ctrl(sd90_port_a, 10, 38, 0))
PB_A11 = (Ctrl(sd90_port_a, 11, 100, 0) // Ctrl(sd90_port_a, 11, 101, 0) // Ctrl(sd90_port_a, 11, 6, 12) // Ctrl(sd90_port_a, 11, 38, 0))
PB_A12 = (Ctrl(sd90_port_a, 12, 100, 0) // Ctrl(sd90_port_a, 12, 101, 0) // Ctrl(sd90_port_a, 12, 6, 12) // Ctrl(sd90_port_a, 12, 38, 0))
PB_A13 = (Ctrl(sd90_port_a, 13, 100, 0) // Ctrl(sd90_port_a, 13, 101, 0) // Ctrl(sd90_port_a, 13, 6, 12) // Ctrl(sd90_port_a, 13, 38, 0))
PB_A14 = (Ctrl(sd90_port_a, 14, 100, 0) // Ctrl(sd90_port_a, 14, 101, 0) // Ctrl(sd90_port_a, 14, 6, 12) // Ctrl(sd90_port_a, 14, 38, 0))
PB_A15 = (Ctrl(sd90_port_a, 15, 100, 0) // Ctrl(sd90_port_a, 15, 101, 0) // Ctrl(sd90_port_a, 15, 6, 12) // Ctrl(sd90_port_a, 15, 38, 0))
PB_A16 = (Ctrl(sd90_port_a, 16, 100, 0) // Ctrl(sd90_port_a, 16, 101, 0) // Ctrl(sd90_port_a, 16, 6, 12) // Ctrl(sd90_port_a, 16, 38, 0))

# SD-90 Part B - All Channel
PB_B01 = (Ctrl(sd90_port_b, 1, 100, 0) // Ctrl(sd90_port_b, 1, 101, 0) // Ctrl(sd90_port_b, 1, 6, 12) // Ctrl(sd90_port_b, 1, 38, 0))
PB_B02 = (Ctrl(sd90_port_b, 2, 100, 0) // Ctrl(sd90_port_b, 2, 101, 0) // Ctrl(sd90_port_b, 2, 6, 12) // Ctrl(sd90_port_b, 2, 38, 0))
PB_B03 = (Ctrl(sd90_port_b, 3, 100, 0) // Ctrl(sd90_port_b, 3, 101, 0) // Ctrl(sd90_port_b, 3, 6, 12) // Ctrl(sd90_port_b, 3, 38, 0))
PB_B04 = (Ctrl(sd90_port_b, 4, 100, 0) // Ctrl(sd90_port_b, 4, 101, 0) // Ctrl(sd90_port_b, 4, 6, 12) // Ctrl(sd90_port_b, 4, 38, 0))
PB_B05 = (Ctrl(sd90_port_b, 5, 100, 0) // Ctrl(sd90_port_b, 5, 101, 0) // Ctrl(sd90_port_b, 5, 6, 12) // Ctrl(sd90_port_b, 5, 38, 0))
PB_B06 = (Ctrl(sd90_port_b, 6, 100, 0) // Ctrl(sd90_port_b, 6, 101, 0) // Ctrl(sd90_port_b, 6, 6, 12) // Ctrl(sd90_port_b, 6, 38, 0))
PB_B07 = (Ctrl(sd90_port_b, 7, 100, 0) // Ctrl(sd90_port_b, 7, 101, 0) // Ctrl(sd90_port_b, 7, 6, 12) // Ctrl(sd90_port_b, 7, 38, 0))
PB_B08 = (Ctrl(sd90_port_b, 8, 100, 0) // Ctrl(sd90_port_b, 8, 101, 0) // Ctrl(sd90_port_b, 8, 6, 12) // Ctrl(sd90_port_b, 8, 38, 0))
PB_B09 = (Ctrl(sd90_port_b, 9, 100, 0) // Ctrl(sd90_port_b, 9, 101, 0) // Ctrl(sd90_port_b, 9, 6, 12) // Ctrl(sd90_port_b, 9, 38, 0))
PB_B10 = (Ctrl(sd90_port_b, 10, 100, 0) // Ctrl(sd90_port_b, 10, 101, 0) // Ctrl(sd90_port_b, 10, 6, 12) // Ctrl(sd90_port_b, 10, 38, 0))
PB_B11 = (Ctrl(sd90_port_b, 11, 100, 0) // Ctrl(sd90_port_b, 11, 101, 0) // Ctrl(sd90_port_b, 11, 6, 12) // Ctrl(sd90_port_b, 11, 38, 0))
PB_B12 = (Ctrl(sd90_port_b, 12, 100, 0) // Ctrl(sd90_port_b, 12, 101, 0) // Ctrl(sd90_port_b, 12, 6, 12) // Ctrl(sd90_port_b, 12, 38, 0))
PB_B13 = (Ctrl(sd90_port_b, 13, 100, 0) // Ctrl(sd90_port_b, 13, 101, 0) // Ctrl(sd90_port_b, 13, 6, 12) // Ctrl(sd90_port_b, 13, 38, 0))
PB_B14 = (Ctrl(sd90_port_b, 14, 100, 0) // Ctrl(sd90_port_b, 14, 101, 0) // Ctrl(sd90_port_b, 14, 6, 12) // Ctrl(sd90_port_b, 14, 38, 0))
PB_B15 = (Ctrl(sd90_port_b, 15, 100, 0) // Ctrl(sd90_port_b, 15, 101, 0) // Ctrl(sd90_port_b, 15, 6, 12) // Ctrl(sd90_port_b, 15, 38, 0))
PB_B16 = (Ctrl(sd90_port_b, 16, 100, 0) // Ctrl(sd90_port_b, 16, 101, 0) // Ctrl(sd90_port_b, 16, 6, 12) // Ctrl(sd90_port_b, 16, 38, 0))

InitPitchBend = (
        PB_B01 // PB_B02 // PB_B03 // PB_B04 // PB_B05 // PB_B06 // PB_B07 // PB_B08 //
        PB_B09 // PB_B10 // PB_B11 // PB_B12 // PB_B13 // PB_B14 // PB_B15 // PB_B16 //
        PB_A01 // PB_A02 // PB_A03 // PB_A04 // PB_A05 // PB_A06 // PB_A07 // PB_A08 //
        PB_A09 // PB_A10 // PB_A11 // PB_A12 // PB_A13 // PB_A14 // PB_A15 // PB_A16)

# --------------------------------------------
# SD-90 # DRUM MAPPING
# --------------------------------------------

# Generic 
Piano = Output(sd90_port_a, channel=1, program=(1))

# Classical Set
StandardSet =  Output(sd90_port_a, channel=10, program=(ClassicalDrum, 1))
RoomSet =  Output(sd90_port_a, channel=10, program=(ClassicalDrum, 9))
PowerSet =  Output(sd90_port_a, channel=10, program=(ClassicalDrum, 17))
ElectricSet =  Output(sd90_port_a, channel=10, program=(ClassicalDrum, 25))
AnalogSet =  Output(sd90_port_a, channel=10, program=(ClassicalDrum, 26))
JazzSet =  Output(sd90_port_a, channel=10, program=(ClassicalDrum, 33))
BrushSet =  Output(sd90_port_a, channel=10, program=(ClassicalDrum, 41))
OrchestraSet =  Output(sd90_port_a, channel=10, program=(ClassicalDrum, 49))
SFXSet =  Output(sd90_port_a, channel=10, program=(ClassicalDrum, 57))

# Contemporary Set
StandardSet2 =  Output(sd90_port_a, channel=10, program=(ContemporaryDrum, 1))
RoomSet2 =  Output(sd90_port_a, channel=10, program=(ContemporaryDrum, 9))
PowerSet2 =  Output(sd90_port_a, channel=10, program=(ContemporaryDrum, 17))
DanceSet =  Output(sd90_port_a, channel=10, program=(ContemporaryDrum, 25))
RaveSet =  Output(sd90_port_a, channel=10, program=(ContemporaryDrum, 26))
JazzSet2 =  Output(sd90_port_a, channel=10, program=(ContemporaryDrum, 33))
BrushSet2 =  Output(sd90_port_a, channel=10, program=(ContemporaryDrum, 41))

# Solo Set
St_Standard =  Output(sd90_port_a, channel=10, program=(SoloDrum, 1))
St_Room =  Output(sd90_port_a, channel=10, program=(SoloDrum, 9))
St_Power =  Output(sd90_port_a, channel=10, program=(SoloDrum, 17))
RustSet =  Output(sd90_port_a, channel=10, program=(SoloDrum, 25))
Analog2Set =  Output(sd90_port_a, channel=10, program=(SoloDrum, 26))
St_Jazz =  Output(sd90_port_a, channel=10, program=(SoloDrum, 33))
St_Brush =  Output(sd90_port_a, channel=10, program=(SoloDrum, 41))

# Enhanced Set
Amb_Standard =  Output(sd90_port_a, channel=10, program=(EnhancedDrum, 1))
Amb_Room =  Output(sd90_port_a, channel=10, program=(EnhancedDrum, 9))
GatedPower =  Output(sd90_port_a, channel=10, program=(EnhancedDrum, 17))
TechnoSet =  Output(sd90_port_a, channel=10, program=(EnhancedDrum, 25))
BullySet =  Output(sd90_port_a, channel=10, program=(EnhancedDrum, 26))
Amb_Jazz =  Output(sd90_port_a, channel=10, program=(EnhancedDrum, 33))
Amb_Brush =  Output(sd90_port_a, channel=10, program=(EnhancedDrum, 41))

# WIP SD-90 Full Patch implementation 
# Special 1 instrument part
DLAPad=Output(sd90_port_a, channel=1, program=(Special1, 1))
BrushingSaw=Output(sd90_port_a, channel=1, program=(Special1, 2))
Xtremities=Output(sd90_port_a, channel=1, program=(Special1, 3))
Atmostrings=Output(sd90_port_a, channel=1, program=(Special1, 4))
NooTongs=Output(sd90_port_a, channel=1, program=(Special1, 5))
Mistery=Output(sd90_port_a, channel=1, program=(Special1, 6))
EastrnEurope=Output(sd90_port_a, channel=1, program=(Special1, 7))
HarpsiAndStr=Output(sd90_port_a, channel=1, program=(Special1, 8))
ShoutGt=Output(sd90_port_a, channel=1, program=(Special1,9))
CleanChorus=Output(sd90_port_a, channel=1, program=(Special1, 10))
MidBoostGt=Output(sd90_port_a, channel=1, program=(Special1, 11))
Guitarvibe=Output(sd90_port_a, channel=1, program=(Special1, 12))
ClusterSect=Output(sd90_port_a, channel=1, program=(Special1, 13))
MariachiTp=Output(sd90_port_a, channel=1, program=(Special1, 14))
NYTenor=Output(sd90_port_a, channel=1, program=(Special1, 15))
JazzClub=Output(sd90_port_a, channel=1, program=(Special1, 16))
MoodyAlto=Output(sd90_port_a, channel=1, program=(Special1, 17))
FujiYama=Output(sd90_port_a, channel=1, program=(Special1, 18))
SDPiano=Output(sd90_port_a, channel=1, program=(Special1, 19))

# Special 2 instrument part
RichChoir=Output(sd90_port_a, channel=1, program=(Special2, 18))
OBBorealis=Output(sd90_port_a, channel=1, program=(Special2, 80))
VintagePhase=Output(sd90_port_a, channel=1, program=(Special2, 82))
FifthAtmAft=Output(sd90_port_a, channel=1, program=(Special2, 85))
Borealis=Output(sd90_port_a, channel=1, program=(Special2, 106))
CircularPad=Output(sd90_port_a, channel=1, program=(Special2, 107))
Oxigenizer=Output(sd90_port_a, channel=1, program=(Special2, 108))
Quasar=Output(sd90_port_a, channel=1, program=(Special2, 109))
HellSection=Output(sd90_port_a, channel=1, program=(Special2, 111))


# Classical instrument part
BirdTweet=Output(sd90_port_b, channel=4, program=(Classical, 124))
Applause=Output(sd90_port_b, channel=8, program=(Classical, 127))

# Classical instrument part - Variation 1
Itopia=Output(sd90_port_b, channel=1, program=(Classical+Var1, 92))
Kalimba=Output(sd90_port_b, channel=1, program=(Classical+Var1, 109))
BagPipe=Output(sd90_port_b, channel=1, program=(Classical+Var1, 110))
Dog=Output(sd90_port_b, channel=14, program=(Classical+Var1, 124))
Telephone2=Output(sd90_port_b, channel=1, program=(Classical+Var1, 125))
CarEngine=Output(sd90_port_b, channel=1, program=(Classical+Var1, 126))
Laughing=Output(sd90_port_b, channel=1, program=(Classical+Var1, 127))

# Classical instrument part - Variation 2
Screaming=Output(sd90_port_b, channel=13, program=(Classical+Var2, 127))
DoorCreak=Output(sd90_port_b, channel=1, program=(Classical+Var2, 125))
Thunder=Output(sd90_port_b, channel=15, program=(Classical+Var2, 123))

# Classical instrument part - Variation 3
Wind=Output(sd90_port_b, channel=3, program=(Classical+Var3, 123))
Explosion=Output(sd90_port_b, channel=7, volume=100, program=(Classical+Var3, 128))

# Classical instrument part - Variation 4
Stream=Output(sd90_port_b, channel=12, program=(Classical+Var4, 123))


# Classical instrument part - Variation 5
Siren=Output(sd90_port_b, channel=5, program=(Classical+Var5, 126))
Bubble=Output(sd90_port_b, channel=1, program=(Classical+Var5, 123))

# Classical instrument part - Variation 6
Train=Output(sd90_port_b, channel=6, program=(Classical+Var6, 126))

# Classical instrument part - Variation 7
Jetplane=Output(sd90_port_b, channel=1, program=(Classical+Var7, 126))

# Classical instrument part - Variation 8
Starship=Output(sd90_port_b, channel=1, program=(Classical+Var8, 126))

# Contemporary instrument part
Helicpoter=Output(sd90_port_b, channel=1, program=(Contemporary, 126))
Seashore=Output(sd90_port_b, channel=2, program=(Contemporary, 123))

# Contemporary instrument part - Variation 1
Rain=Output(sd90_port_b, channel=1, program=(Contemporary+Var1, 123))


### End SD-90 Patch list
# -------------------------------------------------------------------
# SD Mixer config 

Reset = SysEx(sd90_port_a, "f0,41,10,00,48,12,00,00,00,00,00,00,f7")


# Audio FX
MasteringEffect = SysEx(sd90_port_a,"f0,41,10,00,48,12,02,10,20,00,78,56,f7")
AfxOn  = SysEx(sd90_port_a, "f0,41,10,00,48,12,02,10,11,43,01,19,f7")
AfxOff = SysEx(sd90_port_a, "f0,41,10,00,48,12,02,10,11,43,00,1a,f7")

# Audio Mixer
MixToAfx = SysEx(sd90_port_a, "f0,41,10,00,48,12,02,10,10,00,06,58,f7")

# Audio Level Control
WaveLevel  = Port(sd90_port_a) >> CtrlToSysEx(7, "f0,41,10,00,48,12,02,10,11,20,00,3f,f7", 10, 6)
InstLevel  = Port(sd90_port_a) >> CtrlToSysEx(7, "f0,41,10,00,48,12,02,10,11,30,00,3f,f7", 10, 6)
MicGtLevel = Port(sd90_port_a) >> CtrlToSysEx(7, "f0,41,10,00,48,12,02,10,11,00,00,3f,f7", 10, 6)

# SD-90 Bank Patch
SP1  =   SysEx(sd90_port_a, "f0,41,10,00,48,12,10,00,20,04,50,00,00,7c,f7")
SP2  =   SysEx(sd90_port_a, "f0,41,10,00,48,12,10,00,20,04,51,00,00,7b,f7")
CLASIC = SysEx(sd90_port_a, "f0,41,10,00,48,12,10,00,20,04,60,00,00,6c,f7")
CONTEM = SysEx(sd90_port_a, "f0,41,10,00,48,12,10,00,20,04,61,00,00,6b,f7")
SOLO =   SysEx(sd90_port_a, "f0,41,10,00,48,12,10,00,20,04,62,00,00,6a,f7")
ENHANC = SysEx(sd90_port_a, "f0,41,10,00,48,12,10,00,20,04,63,00,00,69,f7")

SD90_Initialize = [
    Reset, 
    MasteringEffect,
    MixToAfx,
    AfxOn, 
    InitPitchBend, 
]
