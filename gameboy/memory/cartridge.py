from .switchable_memory import Switchable_RAM, Switchable_ROM
from .MBC import MBC


class Cartridge:
    def __init__(self, rom_bytes):
        self.rom = Switchable_ROM(rom_bytes)
        header_byte = rom_bytes[0x0147]

        self.ram = self.create_ram(rom_bytes)
        self.mbc_version = self.get_mbc(header_byte)

        self.mbc = MBC(self.ram, self.rom, self.mbc_version)

    def get_mbc(self, header_byte):
        if header_byte in [0x01, 0x02, 0x03]:
            return 1
        elif header_byte in [0x05, 0x06]:
            return 2
        elif header_byte in [0x0F, 0x10, 0x11, 0x12, 0x13]:
            return 3
        elif header_byte in [0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x1E]:
            return 5
        elif header_byte == 0x00:
            return 0

    def create_ram(self, rom_bytes):
        ram_size = rom_bytes[0x0149]
        if ram_size == 0:
            return None
        size_map = {
            0x00: (0, 0),       # sem RAM
            0x01: (1, 0x0800),  # 2 KB
            0x02: (1, 0x2000),  # 8 KB
            0x03: (4, 0x2000),  # 32 KB
            0x04: (16, 0x2000),  # 128 KB
            0x05: (8, 0x2000),  # 64 KB
        }
        total_banks, bank_size = size_map.get(ram_size, (1, 0x2000))
        return Switchable_RAM(total_banks, bank_size)

    def read(self, addrs):
        return self.mbc.handle_read(addrs)

    def write(self, addrs, value):
        self.mbc.handle_write(addrs, value)
