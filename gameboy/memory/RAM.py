class Ram:
    def __init__(self, size=0x2000):
        self.memory = [0] * size #aloca 8kbs

    def write(self, addrs, value):
        if 0xC000 <= addrs < 0xE000:
            offset = addrs - 0xC000
            self.memory[offset] = value
        elif 0xE000 <= addrs < 0xFE00:
            offset = addrs - 0xE000
            if offset < len(self.memory):
                self.memory[offset] = value

    def read(self, addrs):
        if 0xC000 <= addrs < 0xE000:
            offset = addrs - 0xC000
            return self.memory[offset]
        elif 0xE000 <= addrs < 0xFE00:
            offset = addrs - 0xE000
            if offset < len(self.memory):
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
    
