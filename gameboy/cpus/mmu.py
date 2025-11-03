class MMU:
    def __init__(self, ram, mbc):
        self.ram = ram
        self.mbc = mbc
    
    def read(self, addrs):
        if 0xC000 <= addrs < 0xFE00:
            return self.ram.read(addrs)
        elif 0x0000 <= addrs < 0x8000 or 0xA000 <= addrs < 0xC000:
            return self.mbc.handle_read(addrs)
    
    def write(self, addrs, value):
        if 0xC000 <= addrs < 0xFE00:
            self.ram.write(addrs, value)
        elif 0x0000 <= addrs < 0x8000 or 0xA000 <= addrs < 0xC000:
            self.mbc.handle_write(addrs, value)