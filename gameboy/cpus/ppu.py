class PPU:
    def __init__(self, vram, interrupter, oam):
        self.vram = vram
        self.interrupter = interrupter
        self.oam = oam
        self.offset_constant = 0xFF40

        self.registers = [0x91,  # LCDC
                            0,  # STAT
                            0,  # SCY
                            0,  # SCX
                            0,  # LY
                            0,  # LYC
                            0,  # DMA
                            0,  # BGP
                            0,  # OBP0
                            0,  # OBP1
                            0,  # WY
                            0   # WX
                        ]

        self.counter = 0
        self.lcdc_last_state = 1

        self.display_buffer = [[0 for _ in range(160)] for _ in range(144)]
        self.start_render = False

    def trigger_mode_interruption(self, mode):  # fix necessario depois implementar por mudança de borda 0 / 1
        stat = self.registers[1]
        should_interrupt = False
        if mode == 1:
            self.interrupter.request_interrupt(0)

        if mode == 0 and (stat & (1 << 3)):
            should_interrupt = True
        elif mode == 1 and (stat & (1 << 4)):
            should_interrupt = True
        elif mode == 2 and (stat & (1 << 5)):
            should_interrupt = True

        if should_interrupt:
            self.interrupter.request_interrupt(1)

    def trigger_lyc_ly_interruption(self):
        if ((self.registers[1] >> 6) & 1) == 1:
            self.interrupter.request_interrupt(1)

    def set_mode(self, mode):
        current = self.registers[1] & 0x03
        if current == mode:
            return
        self.registers[1] = (self.registers[1] & 0xFC) | (mode & 0x03)
        self.trigger_mode_interruption(mode)

    def reset_ppu_state(self):
        self.registers[4] = 0x00
        self.set_mode(2)
        self.counter = 0

    def set_stat_checkflag(self, set):
        if set:
            self.registers[1] = self.registers[1] | (1 << 2)
        else:
            self.registers[1] = self.registers[1] & ~(1 << 2)

    def handle_ly_lyc_collision(self):
        ly = self.registers[4]
        lyc = self.registers[5]

        if lyc == ly:
            self.set_stat_checkflag(True)
            self.trigger_lyc_ly_interruption()
        else:
            self.set_stat_checkflag(False)

    def increment_ly(self):
        self.registers[4] += 1

        if self.registers[4] > 153:
            self.registers[4] = 0

        self.handle_ly_lyc_collision()

    def render_scanline(self):
        is_unsigned = (self.registers[0] >> 4) & 1

        background_enable = self.registers[0] & 1 # um handler para preencher linha branca caso background enable seja 0 ou lcd seja 0

        tile_map = 0x9C00 if (self.registers[0] >> 3) & 1 else 0x9800

        global_y = (self.registers[4] + self.registers[2]) & 0xFF

        tile_row = global_y // 8

        map_row_start = tile_map + (tile_row * 32)

        for pixel_x in range(160):
            global_x = (pixel_x + self.registers[3]) & 0xFF
            tile_col = global_x // 8

            addrs = map_row_start + tile_col
            tile_id = self.vram.read(addrs)

            if is_unsigned:
                base_addrs = 0x8000 + (tile_id * 16)
            else:
                tile_id_signed = tile_id if tile_id < 128 else tile_id - 256
                base_addrs = 0x9000 + (tile_id_signed * 16)

            y_inside_tile = global_y % 8
            line_addrs = base_addrs + (y_inside_tile * 2)

            byte_low = self.vram.read(line_addrs)
            byte_high = self.vram.read(line_addrs + 1)

            bit_index = 7 - (global_x % 8)

            pixel_color_id = ((byte_high >> bit_index) & 1) << 1
            pixel_color_id |= (byte_low >> bit_index) & 1
            self.display_buffer[self.registers[4]][pixel_x] = pixel_color_id

    def tick(self, cycles):
        lcd_mode = (self.registers[0] >> 7) & 1
        if lcd_mode:
            self.counter += cycles

            if self.registers[4] == 144:
                self.start_render = True

            if self.registers[4] < 144:
                if self.counter < 80:
                    self.set_mode(2)
                elif self.counter < 252:
                    self.set_mode(3)
                else:
                    self.render_scanline()
                    self.set_mode(0)
            else:
                self.set_mode(1)

            if self.counter >= 456:
                self.counter -= 456
                self.increment_ly()

    def write(self, addrs, value):
        offset = addrs - self.offset_constant
        if offset == 0:
            self.registers[offset] = value
            lcd_status = (value >> 7) & 1
            if lcd_status == 0 and self.lcdc_last_state == 1:
                self.reset_ppu_state()
            elif lcd_status == 1 and self.lcdc_last_state == 0:
                self.registers[4] = 0x00
                self.set_mode(2)
                self.counter = 0
            self.lcdc_last_state = (value >> 7) & 1

        elif offset == 4:
            return

        elif offset == 1:
            current = self.registers[offset] & 0x07
            new_value = value & 0x78
            self.registers[offset] = 0x80 | new_value | current

        elif offset == 5:
            self.registers[offset] = value
            self.handle_ly_lyc_collision()
        else:
            self.registers[offset] = value

    def read(self, addrs):
        offset = addrs - self.offset_constant
        return self.registers[offset]

    def get_mode(self):
        return self.registers[1] & 0x03

    def read_vram(self, addrs):
        if self.get_mode() != 3:
            return self.vram.read(addrs)
        return 0xFF

    def write_vram(self, addrs, value):
        if self.get_mode() != 3:
            self.vram.write(addrs, value)

    def read_oam(self, addrs):
        if self.get_mode() < 2:
            return self.oam.read(addrs)
        return 0xFF

    def write_oam(self, addrs, value):
        if self.get_mode() < 2:
            self.oam.write(addrs, value)
