class MMU:
    def __init__(self, ram, mbc, timer,
                 hram, joypad, interrupt_controller,
                 ppu):
        self.ram = ram
        self.mbc = mbc
        self.timer = timer
        self.joypad = joypad
        self.hram = hram
        self.ppu = ppu
        self.interrupt_controller = interrupt_controller

    def debug(self, action, addrs, value=None):
        if (addrs == 0xFF0F or addrs == 0xFFFF) and action == "read":
            return
        print("-"*64)
        print(f"action: {action}")
        print(f"addrs: {addrs:04x}")
        if value is not None:
            print(f"value: {value:02x}")
        print("-"*64)

    def read(self, addrs, dma_mode=False):
        #self.debug("read", addrs)
        if self.ppu.dma_block > 0 and dma_mode == False:
            if 0xFF80 <= addrs < 0xFFFF:
                return self.hram.read(addrs)
            return 0xFF

        if 0xC000 <= addrs < 0xFE00:
            return self.ram.read(addrs)
        elif 0x0000 <= addrs < 0x8000 or 0xA000 <= addrs < 0xC000:
            return self.mbc.handle_read(addrs)
        elif 0xFF04 <= addrs < 0xFF08:
            return self.timer.read(addrs)
        elif 0x8000 <= addrs < 0xA000:
            return self.ppu.read_vram(addrs)
        elif 0xFF80 <= addrs < 0xFFFF:
            return self.hram.read(addrs)
        elif addrs == 0xFF00:
            return self.joypad.read()
        elif addrs == 0xFF0F:
            return self.interrupt_controller.read_if()
        elif addrs == 0xFFFF:
            return self.interrupt_controller.read_ie()
        elif 0xFF40 <= addrs < 0xFF4C:
            return self.ppu.read(addrs)
        elif 0xFE00 <= addrs < 0xFEA0:
            return self.ppu.read_oam(addrs)
        else:
            return 0xFF

    def write(self, addrs, value, dma_mode=False):
        #self.debug("write", addrs, value)
        if self.ppu.dma_block > 0 and dma_mode is False:
            if 0xFF80 <= addrs < 0xFFFF:
                self.hram.write(addrs, value)
            return
        if 0xC000 <= addrs < 0xFE00:
            self.ram.write(addrs, value)
        elif 0x0000 <= addrs < 0x8000 or 0xA000 <= addrs < 0xC000:
            self.mbc.handle_write(addrs, value)
        elif 0xFF04 <= addrs < 0xFF08:
            self.timer.write(addrs, value)
        elif 0x8000 <= addrs < 0xA000:
            self.ppu.write_vram(addrs, value)
        elif 0xFF80 <= addrs < 0xFFFF:
            self.hram.write(addrs, value)
        elif addrs == 0xFF00:
            self.joypad.write(value)
        elif addrs == 0xFF0F:
            self.interrupt_controller.write_if(value)
        elif addrs == 0xFFFF:
            self.interrupt_controller.write_ie(value)
        elif 0xFF40 <= addrs < 0xFF4C:
            self.ppu.write(addrs, value)
        elif 0xFE00 <= addrs < 0xFEA0:
            self.ppu.write_oam(addrs, value)
