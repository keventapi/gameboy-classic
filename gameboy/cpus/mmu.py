class MMU:
    def __init__(self, ram, mbc, timer, vram):
        self.ram = ram
        self.mbc = mbc
        self.timer = timer
        self.vram = vram

        self.sb = 0x00
        self.sc = 0x00

    def read(self, addrs):
        if 0xC000 <= addrs < 0xFE00:
            return self.ram.read(addrs)
        elif 0x0000 <= addrs < 0x8000 or 0xA000 <= addrs < 0xC000:
            return self.mbc.handle_read(addrs)
        elif 0xFF04 <= addrs < 0xFF08:
            return self.timer.read(addrs)
        elif 0x8000 <= addrs < 0xA000:
            return self.vram.read(addrs)
        else:
            return 0xFF
            print(f"addrs: {addrs:02x}")

    def write(self, addrs, value):
        self.debug(addrs, value)
        if 0xC000 <= addrs < 0xFE00:
            self.ram.write(addrs, value)
        elif 0x0000 <= addrs < 0x8000 or 0xA000 <= addrs < 0xC000:
            self.mbc.handle_write(addrs, value)
        elif 0xFF04 <= addrs < 0xFF08:
            self.timer.write(addrs, value)
        elif 0x8000 <= addrs < 0xA000:
            self.vram.write(addrs, value)
        else:
            print(f"addrs: {addrs:02x} \n value: {value:02x}")
