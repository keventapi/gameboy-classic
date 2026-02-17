class SWITCHABLE_RAM:
    def __init__(self, total_banks=4, size=0x2000):
        self.banks = [bytearray(size) for _ in range(total_banks)]
        self.current_bank = 0
        self.bank_size = size

    def read(self, addrs):
        if 0xA000 <= addrs < 0xC000:
            offset = addrs - 0xA000
            return self.banks[self.current_bank][offset]
        return 0xFF

    def read_bank0(self, addrs):
        if 0xA000 <= addrs < 0xC000:
            offset = addrs - 0xA000
            return self.banks[0][offset]
        return 0xFF

    def write(self, addrs, value):
        if 0xA000 <= addrs < 0xC000:
            offset = addrs - 0xA000
            self.banks[self.current_bank][offset] = value

    def switch_bank(self, new_bank):
        if 0 <= new_bank < len(self.banks):
            self.current_bank = new_bank
        else:
            try:
                self.current_bank = new_bank % len(self.banks)
            except:
                self.current_bank = 0

class SWITCHABLE_ROM:
    def __init__(self, rom_bytes, size=0x4000):
        self.banks = [bytes(rom_bytes[i:i+size]) for i in range(0, len(rom_bytes), size)]
        print("number of banks:", len(self.banks))
        self.current_bank = 1
        self.bank_zero = 0
        self.bank_size = size
        self.update_banks()

    def update_banks(self):
        for i, bank in enumerate(self.banks):
            if len(bank) < self.bank_size:
                self.banks[i] += bytes([0xFF] * (self.bank_size - len(bank)))

    def switch_bank(self, new_bank):
        self.current_bank = new_bank % self.num_banks

    def read(self, addrs, mode):
        if 0x0000 <= addrs < 0x4000:
            if mode == 1:
                return self.banks[self.bank_zero % len(self.banks)][addrs]
            else:
                return self.banks[0][addrs]

        elif 0x4000 <= addrs < 0x8000:
            offset = addrs - 0x4000
            return self.banks[self.current_bank][offset]
        return 0xFF
