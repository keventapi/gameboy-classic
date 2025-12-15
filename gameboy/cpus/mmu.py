class MMU:
    def __init__(self, ram, mbc, timer, vram, hram):
        self.ram = ram
        self.mbc = mbc
        self.timer = timer
        self.vram = vram
        self.hram = hram

    def debug(self, action, addrs, value=None):
        print("-"*64)
        print(f"action: {action}")
        print(f"addrs: {addrs:04x}")
        if value is not None:
            print(f"value: {value:02x}")
        print("-"*64)

    def read(self, addrs):
        self.debug("read", addrs)
        if 0xC000 <= addrs < 0xFE00:
            return self.ram.read(addrs)
        elif 0x0000 <= addrs < 0x8000 or 0xA000 <= addrs < 0xC000:
            return self.mbc.handle_read(addrs)
        elif 0xFF04 <= addrs < 0xFF08:
            return self.timer.read(addrs)
        elif 0x8000 <= addrs < 0xA000:
            return self.vram.read(addrs)
        elif 0xFF80 <= addrs < 0xFFFF:
            return self.hram.read(addrs)
        else:
            return 0xFF

    def write(self, addrs, value):
        self.debug("write", addrs, value)
        if 0xC000 <= addrs < 0xFE00:
            self.ram.write(addrs, value)
        elif 0x0000 <= addrs < 0x8000 or 0xA000 <= addrs < 0xC000:
            self.mbc.handle_write(addrs, value)
        elif 0xFF04 <= addrs < 0xFF08:
            self.timer.write(addrs, value)
        elif 0x8000 <= addrs < 0xA000:
            self.vram.write(addrs, value)
        elif 0xFF80 <= addrs < 0xFFFF:
            self.hram.write(addrs, value)
