from .switchable_memory import SWITCHABLE_RAM, SWITCHABLE_ROM
from .MBC import MBC


class CARTRIDGE:
    def __init__(self, rom_bytes):
        self.rom = SWITCHABLE_ROM(rom_bytes)
        header_byte = rom_bytes[0x0147]
        print("header_byte:", header_byte)

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
        # Mapa oficial do Game Boy
        size_map = {
            0x00: 0,
            0x01: 2048,    # 2 KB (raro, mas existe)
            0x02: 8192,    # 8 KB (1 banco)
            0x03: 32768,   # 32 KB (4 bancos)
            0x04: 131072,  # 128 KB (16 bancos)
            0x05: 65536,   # 64 KB (8 bancos)
        }
        
        total_size = size_map.get(ram_size_code, 0)
        if total_size == 0:
            return None # Mas trate isso no MBC para não dar crash!
        
        # Crie bytes zerados para a RAM
        ram_bytes = total_size
        return SWITCHABLE_RAM(ram_bytes, 0x2000) # Reutilizando sua lógica de fatiar bancos

    def read(self, addrs):
        return self.mbc.handle_read(addrs)

    def write(self, addrs, value):
        self.mbc.handle_write(addrs, value)
