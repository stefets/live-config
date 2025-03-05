import re
from typing import Any
from mididings.engine import output_event
from mididings.event import ProgramEvent, CtrlEvent

target_port = "mpk_midi"    # The output port where the MIDI messages will be sent connected to the MIDI IN of the GT1000
target_channel = 9          # The listen channel configured in the GT1000 

class GT1000Patch():
    '''A callable object that send a Patch Change by name to a GT-1000 
    Usage : Call(GT1000Patch("U09-3"))
    Logic:
        Bank 1 (User U01-U25) → 1 to 125
        Bank 2 (User U26-U50) → 1 to 125 (resets)
        Bank 3 (Preset P01-P25) → 1 to 125 (resets)
        Bank 4 (Preset P26-P50) → 1 to 125 (resets)
    '''
    def __init__(self, key) -> None:
        self.key = key

    
    def __call__(self, ev) -> Any:
        ''' Send the patch change to the GT1000'''
        bank, program = self.get_by_key(self.key)
        self.set_bank(bank)
        self.set_program(program)
    
    
    def set_bank(self, bank) -> Any:
        '''Send a Bank Change to the GT1000'''
        output_event(CtrlEvent(target_port, target_channel, 0, bank))
        output_event(CtrlEvent(target_port, target_channel, 32, bank))
    
    
    def set_program(self, program) -> Any:
        '''Send a Program Change to the GT1000'''
        output_event(ProgramEvent(target_port, target_channel, program))

    
    def get_by_key(self, key: str) -> tuple[int, int]:
        '''Extract bank and program numbers from a GT-1000 patch key'''

        # Normalize input (replace possible separators with a dash)
        key = re.sub(r'[\s/_]', '-', key).upper()

        # Extract components using regex
        match = re.match(r'([UP])(\d{2})-(\d)', key)
        if not match:
            raise ValueError(f"Invalid key format: {key}")

        mode, bank, patch = match.groups()
        bank = int(bank)
        patch = int(patch)

        # Determine which bank group we are in
        if 1 <= bank <= 25:
            bank_id = 0 if mode == 'U' else 2  # Bank 1 (User) or Bank 3 (Preset)
        elif 26 <= bank <= 50:
            bank_id = 1 if mode == 'U' else 3  # Bank 2 (User) or Bank 4 (Preset)
            bank -= 25  # Normalize bank to 1-25
        else:
            raise ValueError(f"Invalid bank number: {bank}")

        # Calculate MIDI program number (1-125)
        program = (bank - 1) * 5 + patch

        return bank_id, program
