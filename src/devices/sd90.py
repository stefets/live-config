#
# This is the patches specific for the sound modules configuration
#
# EDIROL SD-90
#
# Reset string
ResetSD90 = SysEx('\xF0\x41\x10\x00\x48\x12\x00\x00\x00\x00\x00\x00\xF7')

# Configure PitchBend Sensitivity
# SD-90 Part A - All Channel
#      * RPN MSB/LSB 0 = PitchBendSens ****  //  ****** DataEntry 12 tone *******
PB_A01 = (Ctrl(1, 1, 100, 0) // Ctrl(1, 1, 101, 0) // Ctrl(1, 1, 6, 12) // Ctrl(1, 1, 38, 0))
PB_A02 = (Ctrl(1, 2, 100, 0) // Ctrl(1, 2, 101, 0) // Ctrl(1, 2, 6, 12) // Ctrl(1, 2, 38, 0))
PB_A03 = (Ctrl(1, 3, 100, 0) // Ctrl(1, 3, 101, 0) // Ctrl(1, 3, 6, 12) // Ctrl(1, 3, 38, 0))
PB_A04 = (Ctrl(1, 4, 100, 0) // Ctrl(1, 4, 101, 0) // Ctrl(1, 4, 6, 12) // Ctrl(1, 4, 38, 0))
PB_A05 = (Ctrl(1, 5, 100, 0) // Ctrl(1, 5, 101, 0) // Ctrl(1, 5, 6, 12) // Ctrl(1, 5, 38, 0))
PB_A06 = (Ctrl(1, 6, 100, 0) // Ctrl(1, 6, 101, 0) // Ctrl(1, 6, 6, 12) // Ctrl(1, 6, 38, 0))
PB_A07 = (Ctrl(1, 7, 100, 0) // Ctrl(1, 7, 101, 0) // Ctrl(1, 7, 6, 12) // Ctrl(1, 7, 38, 0))
PB_A08 = (Ctrl(1, 8, 100, 0) // Ctrl(1, 8, 101, 0) // Ctrl(1, 8, 6, 12) // Ctrl(1, 8, 38, 0))
PB_A09 = (Ctrl(1, 9, 100, 0) // Ctrl(1, 9, 101, 0) // Ctrl(1, 9, 6, 12) // Ctrl(1, 9, 38, 0))
PB_A10 = (Ctrl(1, 10, 100, 0) // Ctrl(1, 10, 101, 0) // Ctrl(1, 10, 6, 12) // Ctrl(1, 10, 38, 0))
PB_A11 = (Ctrl(1, 11, 100, 0) // Ctrl(1, 11, 101, 0) // Ctrl(1, 11, 6, 12) // Ctrl(1, 11, 38, 0))
PB_A12 = (Ctrl(1, 12, 100, 0) // Ctrl(1, 12, 101, 0) // Ctrl(1, 12, 6, 12) // Ctrl(1, 12, 38, 0))
PB_A13 = (Ctrl(1, 13, 100, 0) // Ctrl(1, 13, 101, 0) // Ctrl(1, 13, 6, 12) // Ctrl(1, 13, 38, 0))
PB_A14 = (Ctrl(1, 14, 100, 0) // Ctrl(1, 14, 101, 0) // Ctrl(1, 14, 6, 12) // Ctrl(1, 14, 38, 0))
PB_A15 = (Ctrl(1, 15, 100, 0) // Ctrl(1, 15, 101, 0) // Ctrl(1, 15, 6, 12) // Ctrl(1, 15, 38, 0))
PB_A16 = (Ctrl(1, 16, 100, 0) // Ctrl(1, 16, 101, 0) // Ctrl(1, 16, 6, 12) // Ctrl(1, 16, 38, 0))
# SD-90 Part B - All Channel
PB_B01 = (Ctrl(2, 1, 100, 0) // Ctrl(2, 1, 101, 0) // Ctrl(2, 1, 6, 12) // Ctrl(2, 1, 38, 0))
PB_B02 = (Ctrl(2, 2, 100, 0) // Ctrl(2, 2, 101, 0) // Ctrl(2, 2, 6, 12) // Ctrl(2, 2, 38, 0))
PB_B03 = (Ctrl(2, 3, 100, 0) // Ctrl(2, 3, 101, 0) // Ctrl(2, 3, 6, 12) // Ctrl(2, 3, 38, 0))
PB_B04 = (Ctrl(2, 4, 100, 0) // Ctrl(2, 4, 101, 0) // Ctrl(2, 4, 6, 12) // Ctrl(2, 4, 38, 0))
PB_B05 = (Ctrl(2, 5, 100, 0) // Ctrl(2, 5, 101, 0) // Ctrl(2, 5, 6, 12) // Ctrl(2, 5, 38, 0))
PB_B06 = (Ctrl(2, 6, 100, 0) // Ctrl(2, 6, 101, 0) // Ctrl(2, 6, 6, 12) // Ctrl(2, 6, 38, 0))
PB_B07 = (Ctrl(2, 7, 100, 0) // Ctrl(2, 7, 101, 0) // Ctrl(2, 7, 6, 12) // Ctrl(2, 7, 38, 0))
PB_B08 = (Ctrl(2, 8, 100, 0) // Ctrl(2, 8, 101, 0) // Ctrl(2, 8, 6, 12) // Ctrl(2, 8, 38, 0))
PB_B09 = (Ctrl(2, 9, 100, 0) // Ctrl(2, 9, 101, 0) // Ctrl(2, 9, 6, 12) // Ctrl(2, 9, 38, 0))
PB_B10 = (Ctrl(2, 10, 100, 0) // Ctrl(2, 10, 101, 0) // Ctrl(2, 10, 6, 12) // Ctrl(2, 10, 38, 0))
PB_B11 = (Ctrl(2, 11, 100, 0) // Ctrl(2, 11, 101, 0) // Ctrl(2, 11, 6, 12) // Ctrl(2, 11, 38, 0))
PB_B12 = (Ctrl(2, 12, 100, 0) // Ctrl(2, 12, 101, 0) // Ctrl(2, 12, 6, 12) // Ctrl(2, 12, 38, 0))
PB_B13 = (Ctrl(2, 13, 100, 0) // Ctrl(2, 13, 101, 0) // Ctrl(2, 13, 6, 12) // Ctrl(2, 13, 38, 0))
PB_B14 = (Ctrl(2, 14, 100, 0) // Ctrl(2, 14, 101, 0) // Ctrl(2, 14, 6, 12) // Ctrl(2, 14, 38, 0))
PB_B15 = (Ctrl(2, 15, 100, 0) // Ctrl(2, 15, 101, 0) // Ctrl(2, 15, 6, 12) // Ctrl(2, 15, 38, 0))
PB_B16 = (Ctrl(2, 16, 100, 0) // Ctrl(2, 16, 101, 0) // Ctrl(2, 16, 6, 12) // Ctrl(2, 16, 38, 0))

InitPitchBend = (
        PB_B01 // PB_B02 // PB_B03 // PB_B04 // PB_B05 // PB_B06 // PB_B07 // PB_B08 //
        PB_B09 // PB_B10 // PB_B11 // PB_B12 // PB_B13 // PB_B14 // PB_B15 // PB_B16 //
        PB_A01 // PB_A02 // PB_A03 // PB_A04 // PB_A05 // PB_A06 // PB_A07 // PB_A08 //
        PB_A09 // PB_A10 // PB_A11 // PB_A12 // PB_A13 // PB_A14 // PB_A15 // PB_A16)

# --------------------------------------------
# SD-90 # DRUM MAPPING
# --------------------------------------------
# Classical Set
StandardSet =  Output('SD90-PART-A', channel=10, program=(13312, 1))
RoomSet =  Output('SD90-PART-A', channel=10, program=(13312, 9))
PowerSet =  Output('SD90-PART-A', channel=10, program=(13312, 17))
ElectricSet =  Output('SD90-PART-A', channel=10, program=(13312, 25))
AnalogSet =  Output('SD90-PART-A', channel=10, program=(13312, 26))
JazzSet =  Output('SD90-PART-A', channel=10, program=(13312, 33))
BrushSet =  Output('SD90-PART-A', channel=10, program=(13312, 41))
OrchestraSet =  Output('SD90-PART-A', channel=10, program=(13312, 49))
SFXSet =  Output('SD90-PART-A', channel=10, program=(13312, 57))
# Contemporary Set
StandardSet2 =  Output('SD90-PART-A', channel=10, program=(13440, 1))
RoomSet2 =  Output('SD90-PART-A', channel=10, program=(13440, 9))
PowerSet2 =  Output('SD90-PART-A', channel=10, program=(13440, 17))
DanceSet =  Output('SD90-PART-A', channel=10, program=(13440, 25))
RaveSet =  Output('SD90-PART-A', channel=10, program=(13440, 26))
JazzSet2 =  Output('SD90-PART-A', channel=10, program=(13440, 33))
BrushSet2 =  Output('SD90-PART-A', channel=10, program=(13440, 41))
# Solo Set
St_Standard =  Output('SD90-PART-A', channel=10, program=(13568, 1))
St_Room =  Output('SD90-PART-A', channel=10, program=(13568, 9))
St_Power =  Output('SD90-PART-A', channel=10, program=(13568, 17))
RustSet =  Output('SD90-PART-A', channel=10, program=(13568, 25))
Analog2Set =  Output('SD90-PART-A', channel=10, program=(13568, 26))
St_Jazz =  Output('SD90-PART-A', channel=10, program=(13568, 33))
St_Brush =  Output('SD90-PART-A', channel=10, program=(13568, 41))
# Enhanced Set
Amb_Standard =  Output('SD90-PART-A', channel=10, program=(13696, 1))
Amb_Room =  Output('SD90-PART-A', channel=10, program=(13696, 9))
GatedPower =  Output('SD90-PART-A', channel=10, program=(13696, 17))
TechnoSet =  Output('SD90-PART-A', channel=10, program=(13696, 25))
BullySet =  Output('SD90-PART-A', channel=10, program=(13696, 26))
Amb_Jazz =  Output('SD90-PART-A', channel=10, program=(13696, 33))
Amb_Brush =  Output('SD90-PART-A', channel=10, program=(13696, 41))

### SD-90 Full Patch implementation 
# TODO 
BrushingSaw =  Output('SD90-PART-A', channel=1, program=((80 * 128), 2))
# TODO 
### End SD-90 Patch list
# -------------------------------------------------------------------

InitSoundModule = (ResetSD90 // InitPitchBend)
