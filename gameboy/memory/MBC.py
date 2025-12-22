class MBC:
    def __init__(self, ram, rom, mbc_version):
        self.ram = ram
        self.rom = rom
        self.ram_enabled = False
        self.mode = 0
        self.mbc_version = mbc_version
        self.mbc1_output_pins = [0, 0]
        self.mbc5_lower = 0
        self.mbc5_upper = 0
        self.rom_low_bank = None

    def select_rom_bank(self, bank):
        if bank == 0:
            bank = 1
        self.rom_low_bank = bank
        self.rom.switch_bank(bank)

    def check_output(self):
        return (self.mode == 1
                and len(self.rom) <= 512 * 1024
                and len(self.ram) <= 8 * 1024)

    def handle_mdc1_output(self, value):
        self.mbc1_output_pins[0] = value & 0x01
        self.mbc1_output_pins[1] = (value >> 1) & 0x01

    def handle_write(self, addrs, value):
        if self.mbc_version == 1:
            self.write_mbc1(addrs, value)
        elif self.mbc_version == 2:
            self.write_mbc2(addrs, value)
        elif self.mbc_version == 3:
            self.write_mbc3(addrs, value)
        elif self.mbc_version == 5:
            self.write_mbc5(addrs, value)

    def handle_read(self, addrs):
        if self.mbc_version == 1:
            return self.read_mbc1(addrs)
        elif self.mbc_version == 2:
            return self.read_mbc2(addrs)
        elif self.mbc_version == 3:
            return self.read_mbc3(addrs)
        elif self.mbc_version == 5:
            return self.read_mbc5(addrs)
        elif self.mbc_version == 0:
            return self.rom.read(addrs)
        return 0xFF

    def write_mbc1(self, addrs, value):
        if 0xA000 <= addrs < 0xC000:
            if self.ram_enabled:
                self.ram.write(addrs, value)

        if 0x0000 <= addrs < 0x2000:
            self.ram_enabled = (value & 0b1111) == 0b1010

        if 0x2000 <= addrs < 0x4000:
            bank = value & 0x1F
            self.select_rom_bank(bank)

        if 0x4000 <= addrs < 0x6000 and self.check_output():
            self.handle_mdc1_output(value)

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

    def write_mbc2(self, addrs, value):
        if 0x0000 <= addrs < 0x1FFF and (addrs & 0x0100) == 0:
            self.ram_enabled = not self.ram_enabled

        elif 0x2000 <= addrs < 0x4000 and (addrs & 0x0100) != 0:
            bank = value & 0x0F
            self.select_rom_bank(bank)

        if 0xA000 <= addrs < 0xA200:
            if self.ram_enabled:
                self.ram.write(addrs, value & 0x0F)

    def write_mbc3(self, addrs, value):
        if 0xA000 <= addrs < 0xC000:
            if self.ram_enabled:
                self.ram.write(addrs, value)

        if 0x4000 <= addrs < 0x6000:
            raise NotImplementedError("rtc clock não foi implementado ainda")

        if 0x0000 <= addrs < 0x2000:
            self.ram_enabled = (value & 0b1111) == 0b1010

        if 0x2000 <= addrs < 0x4000:
            self.select_rom_bank(value & 0b01111111)

    def write_mbc5(self, addrs, value):
        if 0x2000 <= addrs < 0x3000:
            self.mbc5_lower = value & 0xFF
        if 0x3000 <= addrs < 0x4000:
            self.mbc5_upper = value & 0b1
            bank = (self.mbc5_upper << 8) | self.mbc5_lower
            self.select_rom_bank(bank)

        if (0x4000 <= addrs < 0x6000
                and self.ram is not None
                and self.ram_enabled):
            bank = value & 0xFF
            self.ram.switch_bank(bank)

        if (0xA000 <= addrs < 0xC000
                and self.ram_enabled
                and self.ram is not None):
            self.ram.write(addrs, value)

    def read_mbc1(self, addrs):
        if 0xA000 <= addrs < 0xC000:
            if self.ram_enabled and self.ram is not None:
                return self.ram.read(addrs)
            return 0xFF

        if 0x0000 <= addrs < 0x8000:
            return self.rom.read(addrs)

    def read_mbc2(self, addrs):
        if 0xA000 <= addrs < 0xA200:
            if self.ram_enabled and self.ram is not None:
                return self.ram.read(addrs)
            return 0xFF

        if 0x0000 <= addrs < 0x8000:
            return self.rom.read(addrs)

    def read_mbc3(self, addrs):
        return self.read_mbc1(addrs)

    def read_mbc5(self, addrs):
        return self.read_mbc1(addrs)
