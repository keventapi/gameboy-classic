class MBC:
    def __init__(self, ram, rom, mbc_version):
        self.ram = ram
        self.rom = rom
        self.ram_enabled = False
        self.mode = 0
        self.mbc_version = mbc_version
        self.bank_lower_bits = 1
        self.ram_bank = 0
        self.bank_high_bits = 0

    def select_rom_bank(self):
        complete_bank = (self.bank_high_bits << 5) | self.bank_lower_bits
        self.rom.current_bank = complete_bank % len(self.rom.banks)
        if self.mode == 1:
            if self.ram is not None:
                ram_bank = self.bank_high_bits
                self.rom.bank_zero = ram_bank << 5
                self.ram.switch_bank(ram_bank)
        else:
            if self.ram is not None:
                self.ram.switch_bank(0)

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
            raise NotImplementedError(f"mbc version: {self.mbc_version} not implemented yet")
        elif self.mbc_version == 3:
            return self.read_mbc3(addrs)
        elif self.mbc_version == 5:
            raise NotImplementedError(f"mbc version: {self.mbc_version} not implemented yet")
        elif self.mbc_version == 0:
            return self.rom.read(addrs, 0)
        return 0xFF

    def write_mbc1(self, addrs, value):
        if 0x0000 <= addrs < 0x2000:
            self.ram_enabled = (value & 0x0F) == 0x0A

        elif 0x2000 <= addrs < 0x4000:
            bank_lower_bits = value & 0x1F
            self.bank_lower_bits = bank_lower_bits if bank_lower_bits != 0 else 1
            self.select_rom_bank()

        elif 0x4000 <= addrs < 0x6000:
            self.bank_high_bits = value & 0x03
            self.select_rom_bank()
            if self.mode == 1:
                if self.ram is not None:
                    self.ram.switch_bank(self.bank_high_bits)
        elif 0x6000 <= addrs < 0x8000:
            self.mode = value & 0x01
            self.select_rom_bank()
            if self.ram is not None:
                self.ram.switch_bank(self.bank_high_bits if self.mode == 1 else 0)

        if 0xA000 <= addrs < 0xC000:
            if self.ram_enabled:
                self.ram.write(addrs, value)

    def read_mbc1(self, addrs):
        if 0xA000 <= addrs < 0xC000:
            if self.ram_enabled and self.ram is not None:
                return self.ram.read(addrs)
            return 0xFF

        if 0x0000 <= addrs < 0x8000:
            return self.rom.read(addrs, self.mode)

    def write_mbc3(self, addrs, value):
        if 0x2000 <= addrs < 0x4000:
            self.bank = value & 0x7F if value != 0 else 1
            self.rom.switch_bank(self.bank)

        elif 0x0000 <= addrs < 0x2000:
            self.ram_enabled = (value & 0x0F) == 0x0A

        elif 0x4000 <= addrs < 0x6000:
            if value <= 0x07:
                if self.ram is not None:
                    self.ram_bank = value & (len(self.ram.banks) - 1)
                    self.ram.switch_bank(self.ram_bank)
            else:
                raise NotImplementedError("RTC NOT IMPLEMENTED YET")

        elif 0xA000 <= addrs < 0xC000:
            if self.ram_enabled and self.ram is not None:
                self.ram.write(addrs, value)

    def read_mbc3(self, addrs):
        if 0x0000 <= addrs < 0x8000:
            return self.rom.read(addrs, 0)

        elif 0xA000 <= addrs < 0xC000:
            if self.ram_enabled:
                return self.ram.read(addrs)

        return 0xFF
