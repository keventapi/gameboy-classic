from .switchable_memory import SWITCHABLE_RAM, SWITCHABLE_ROM
from .MBC import MBC


class CARTRIDGE:
    def __init__(self, rom_bytes):
        self.rom = SWITCHABLE_ROM(rom_bytes)
        header_byte = rom_bytes[0x0147]
        print("header_byte:", f"{header_byte:02x}")

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
        ram_size_code = rom_bytes[0x0149]
        size_map = {
            0x00: 0,
            0x02: 0x2000,   # 8 KiB (1 banco)
            0x03: 0x8000,   # 32 KiB (4 bancos)
            0x04: 0x20000,  # 128 KiB (16 bancos)
            0x05: 0x10000,  # 64 KiB (8 bancos)
        }
        total_size = size_map.get(ram_size_code, 0)
        if total_size == 0: return None

        num_banks = total_size // 0x2000

        return SWITCHABLE_RAM(total_banks=num_banks, size=0x2000)

    def read(self, addrs):
        return self.mbc.handle_read(addrs)

    def write(self, addrs, value):
        self.mbc.handle_write(addrs, value)
