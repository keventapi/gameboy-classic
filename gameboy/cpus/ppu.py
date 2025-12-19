class PPU:
    def __init__(self, vram, interrupter):
        self.vram = vram
        self.interrupter = interrupter
        self.registers_map = {
            0xFF40: "LCDC",
            0xFF41: "STAT",
            0xFF42: "SCY",
            0xFF43: "SCX",
            0xFF44: "LY",
            0xFF45: "LYC",
            0xFF46: "DMA",
            0xFF47: "BGP",
            0xFF48: "OBP0",
            0xFF49: "OBP1",
            0xFF4A: "WY",
            0xFF4B: "WX"
        }
        self.registers = {
            "LY": 0x00,
            "STAT": 0x00,
            "LYC": 0x00,
            "LCDC": 0x91,
            "WX": 0x00,
            "WY": 0x00,
            "OBP1": 0x00,
            "OBP0": 0x00,
            "BGP": 0x00,
            "DMA": 0x00,
            "SCX": 0x00,
            "SCY": 0x00
        }
        self.counter = 0
        self.lcdc_last_state = 1

    def trigger_mode_interruption(self, mode):
        if mode == 1:
            self.interrupter.request_interrupt(0)
        if mode == 1 and ((self.registers["STAT"] >> 4) & 1) == 1:
            self.interrupter.request_interrupt(1)
        elif mode == 2 and ((self.registers["STAT"] >> 5) & 1) == 1:
            self.interrupter.request_interrupt(1)
        elif mode == 2 and ((self.registers["STAT"] >> 3) & 1) == 1:
            self.interrupter.request_interrupt(1)
        elif mode == 0 and ((self.registers["STAT"] >> 3) & 1) == 1:
            self.interrupter.request_interrupt(1)

    def trigger_lyc_ly_interruption(self):
        if ((self.registers["STAT"] >> 6) & 1) == 1:
            self.interrupter.request_interrupt(1)

    def set_mode(self, mode):
        current = self.registers["STAT"] & 0x03
        if current == mode:
            return
        self.registers["STAT"] = (self.registers["STAT"] & 0xFC) | (mode & 0x03)
        self.trigger_mode_interruption(mode)

    def reset_ppu_state(self):
        self.registers["LY"] = 0x00
        self.set_mode(2)
        self.counter = 0

    def set_stat_checkflag(self, set):
        if set:
            self.registers["STAT"] = self.registers["STAT"] | (1 << 2)
        else:
            self.registers["STAT"] = self.registers["STAT"] & ~(1 << 2)

    def increment_ly(self):
        self.registers["LY"] += 1

        if self.registers["LY"] > 153:
            self.registers["LY"] = 0

        ly = self.registers["LY"]
        lyc = self.registers["LYC"]

        if lyc == ly:
            self.set_stat_checkflag(True)
            self.trigger_lyc_ly_interruption()
        else:
            self.set_stat_checkflag(False)
        print(f"LY: {self.registers["LY"]}")

    def tick(self, cycles):
        lcd_mode = (self.registers["LCDC"] >> 7) & 1
        if lcd_mode:
            self.counter += cycles

            if self.registers["LY"] < 144:
                if self.counter < 80:
                    self.set_mode(2)
                elif self.counter < 252:
                    self.set_mode(3)
                else:
                    self.set_mode(0)
            else:
                self.set_mode(1)

            if self.counter >= 456:
                self.counter -= 456
                self.increment_ly()

    def write(self, addrs, value):
        name = self.registers_map[addrs]

        if name == "LCDC":
            self.registers[name] = value
            lcd_status = (value >> 7) & 1
            if lcd_status == 0 and self.lcdc_last_state == 1:
                self.reset_ppu_state()
            elif lcd_status == 1 and self.lcdc_last_state == 0:
                self.registers["LY"] = 0x00
                self.set_mode(2)
                self.counter = 0
            self.lcdc_last_state = (value >> 7) & 1

        elif name == "LY":
            return

        elif name == "STAT":
            current = self.registers[name] & 0x07
            new_value = value & 0x78
            self.registers[name] = 0x80 | new_value | current

        else:
            self.registers[name] = value

    def read(self, addrs):
        name = self.registers_map[addrs]
        return self.registers[name]

    def get_mode(self):
        return self.registers["STAT"] & 0x03

    def read_vram(self, addrs):
        if self.get_mode() != 3:
            return self.vram.read(addrs)
        return 0xFF

    def write_vram(self, addrs, value):
        if self.get_mode() != 3:
            self.vram.write(addrs, value)
