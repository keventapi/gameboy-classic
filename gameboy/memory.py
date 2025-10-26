class Ram:
    def __init__(self, size=0x2000):
        self.memory = [0] * size #aloca 8kbs

    def write(self, addrs, value):
        if 0xC000 <= addrs < 0xE000:
            offset = addrs - 0xC000
            self.memory[offset] = value
    
    def read(self, addrs):
        return self.memory[addrs]
    
class Vram:
    def __init__(self, size=0x2000):
        self.memory = [0]*size 
    
