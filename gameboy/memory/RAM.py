class RAM:
    def __init__(self, size=0x2000):
        self.memory = bytearray(size)

    def write(self, addrs, value):
        if 0xC000 <= addrs < 0xE000:
            offset = addrs - 0xC000
            self.memory[offset] = value
        else:
            offset = addrs - 0xE000
            self.memory[offset] = value

    def read(self, addrs):
        if 0xC000 <= addrs < 0xE000:
            offset = addrs - 0xC000
            return self.memory[offset]
        else:
            offset = addrs - 0xE000
            return self.memory[offset]


class HRAM:
    def __init__(self, size=0x7F):
        self.memory = bytearray(size)

    def write(self, addrs, value):
        if 0xFF80 <= addrs < 0xFFFF:
            offset = addrs - 0xFF80
            self.memory[offset] = value

    def read(self, addrs):
        if 0xFF80 <= addrs < 0xFFFF:
            offset = addrs - 0xFF80
            return self.memory[offset]
        return 0xFF


class VRAM:
    def __init__(self, size=0x2000):
        self.memory = bytearray(size)

    def write(self, addrs, value):
        if 0x8000 <= addrs < 0xA000:
            offset = addrs - 0x8000
            self.memory[offset] = value

    def read(self, addrs):
        if 0x8000 <= addrs < 0xA000:
            offset = addrs - 0x8000
            return self.memory[offset]
        return 0xFF
