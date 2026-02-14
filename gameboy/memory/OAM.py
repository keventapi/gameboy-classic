class OAM:
    def __init__(self):
        self.memory = [0] * 0xA0

    def write(self, addrs, value):
        if 0xFE00 <= addrs < 0xFEA0:
            offset = addrs - 0xFE00
            self.memory[offset] = value

    def read(self, addrs):
        if 0xFE00 <= addrs < 0xFEA0:
            offset = addrs - 0xFE00
            return self.memory[offset]
        return 0xFF
