class RAM:
    def __init__(self, size=0x2000):
        self.memory = bytearray(size)

    def write(self, addrs, value):
        offset = addrs & 0x1FFF
        self.memory[offset] = value

    def read(self, addrs):
        return self.memory[addrs & 0x1FFF]


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
