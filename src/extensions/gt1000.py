
from typing import Any
from mididings.engine import output_event
from mididings.event import ProgramEvent

'''

'''

target_port = "mpk_midi"    # The output port where the PC will be sent connected to the MIDI IN of the HD500
target_channel = 15         # The listen channel configured in the GT1000 

class GT1000PC():
    '''A callable object that send a Program Change by name to a GT1000 
    Usage : Call(GT1000PC("1A"))
    Notes : 1A=1, 2A=2 etc... to 16D=64 
    '''
    def __init__(self, key) -> None:
        self.key = key

    def __call__(self, ev) -> Any:
        output_event(ProgramEvent(target_port, target_channel, self.get_program_by_key(self.key)))

    
    def get_program_by_key(self, key) -> int:
        '''Return the program number by key'''
        # Extract the number and letter from the key
        num_part = int(key[:-1])  # everything except the last character
        letter_part = key[-1].lower()  # the last character, in lowercase

        # Calculate the value based on the pattern
        # Each number has 4 letters (a=1, b=2, c=3, d=4)
        return (num_part - 1) * 4 + (ord(letter_part) - ord('a') + 1)
