class Ram:
    def __init__(self, size=0x2000):
        self.memory = [0] * size #aloca 8kbs

    def write(self, addrs, value):
        if 0xC000 <= addrs < 0xE000:
            offset = addrs - 0xC000
            self.memory[offset] = value
        elif 0xE000 <= addrs < 0xFE00:
            offset = addrs - 0xE000
            self.memory[offset] = value

    def read(self, addrs):
        if 0xC000 <= addrs < 0xE000:
            offset = addrs - 0xC000
            return self.memory[offset]
        elif 0xE000 <= addrs < 0xFE00:
            offset = addrs - 0xE000
            return self.memory[offset]
        return 0xFF
    

class Vram:
    def __init__(self, size=0x2000):
        self.memory = [0]*size 
    
    def write(self, addrs, value):
        if 0x8000 <= addrs < 0xA000:
            offset = addrs - 0x8000
            self.memory[offset] = value
    
    def read(self, addrs):
        if 0x8000 <= addrs < 0xA000:
            offset = addrs - 0x8000
            return self.memory[offset]
        return 0xFF
    
class Switchable_RAM:
    def __init__(self, total_banks=4, size=0x2000):
        self.banks = [[0]*size for _ in range(total_banks)]
        self.current_bank = 0
        self.bank_size = size

    def read(self, addrs):
        if 0xA000 <= addrs < 0xC000:
            offset = addrs - 0xA000
            return self.banks[self.current_bank][offset]
        return 0xFF

    def write(self, addrs, value):
        if 0xA000 <= addrs < 0xC000:
            offset = addrs - 0xA000
            self.banks[self.current_bank][offset] = value

    def switch_bank(self, new_bank):
        if 0 <= new_bank < len(self.banks):
            self.current_bank = new_bank
        else:
            self.switch_bank(new_bank % len(self.banks))

class Switchable_ROM:
    def __init__(self, rom_bytes, size=0x4000):
        self.banks = [rom_bytes[i:i+size] for i in range(0, len(rom_bytes), size)]
        self.current_bank = 1
        self.bank_size = size
        self.update_banks()


    def update_banks(self):
        for i, bank in enumerate(self.banks):
            if len(bank) < self.bank_size:
                self.banks[i] += bytes([0xFF] * (self.bank_size - len(bank)))

    def switch_bank(self, new_bank):
        if 0 <= new_bank < len(self.banks):
            self.current_bank = new_bank
        else:
            self.switch_bank(new_bank % len(self.banks))

    def read(self, addrs):
        if 0x0000 <= addrs < 0x4000:
            return self.banks[0][addrs]
        
        elif 0x4000 <= addrs < 0x8000:
            offset = addrs - 0x4000
            return self.banks[self.current_bank][offset]
        return 0xFF


class MBC:
    def __init__(self, ram, rom):
        self.ram = ram 
        self.rom = rom
        self.ram_enabled = False
        self.mode = 0

        self.rom_low_bank = None


    def select_rom_bank(self, value):
        bank = value & 0x1F
        if bank == 0:
            bank = 1
        
        self.rom_low_bank = bank & 0x1F

        self.rom.switch_bank(bank)

    def write(self, addrs, value):

        if 0xA000 <= addrs < 0xC000:
            if self.ram_enabled:
                self.ram.write(addrs, value)

        if 0x0000 <= addrs < 0x2000:
            self.ram_enabled = (value & 0b1111) == 0b1010

        if 0x2000 <= addrs < 0x4000:
            self.select_rom_bank(value)

        if 0x6000 <= addrs < 0x8000:
            self.mode = value & 1
            if self.mode == 0:
                self.ram.switch_bank(0)

        if self.mode == 1:
            if 0x4000 <= addrs < 0x6000:
                bank = value & 0b11
                self.ram.switch_bank(bank)

        elif self.mode == 0:
            if 0x4000 <= addrs < 0x6000:
                high_bank = value & 0b11 
                bank = (high_bank << 5) | self.rom_low_bank
                self.rom.switch_bank(bank)

    def read(self, addrs):
        if 0xA000 <= addrs < 0xC000:
            if self.ram_enabled:
                return self.ram.read(addrs)
            return 0xFF
        
        if 0x0000 <= addrs < 0x8000:
            return self.rom.read(addrs)
