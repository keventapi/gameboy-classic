class PPU:
    def __init__(self, vram, interrupter, oam):
        self.vram = vram
        self.interrupter = interrupter
        self.oam = oam
        self.offset_constant = 0xFF40

        self.dma_block = 0
        self.dma_src_addrs = None
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
        self.stat_line = False
        self.last_display_reset = True

    def disable_display(self):
        mode = ~(1 << 7)
        self.registers[0] &= mode

    def update_stat_interrupt(self):
        stat = self.registers[1]
        mode = self.get_mode()
        ly = self.registers[4]
        lyc = self.registers[5]

        lyc_int = (stat & (1 << 6)) and (ly == lyc)
        mode0_int = (stat & (1 << 3)) and (mode == 0)
        mode1_int = (stat & (1 << 4)) and (mode == 1)
        mode2_int = (stat & (1 << 5)) and (mode == 2)

        current_signal = lyc_int or mode0_int or mode1_int or mode2_int

        if current_signal and not self.stat_line:
            self.interrupter.request_interrupt(1)

        self.stat_line = current_signal

    def set_mode(self, mode):
        current = self.registers[1] & 0x03
        if current == mode:
            return
        self.registers[1] = (self.registers[1] & 0xFC) | (mode & 0x03)

    def reset_ppu_state(self):
        self.registers[4] = 0x00
        self.set_mode(2)
        self.display_buffer = [[0 for _ in range(160)] for _ in range(144)]
        self.counter = 0
        self.last_display_reset = True

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
            self.update_stat_interrupt()
        else:
            self.set_stat_checkflag(False)

    def increment_ly(self):
        old_ly = self.registers[4]

        self.registers[4] += 1

        if self.registers[4] > 153:
            self.registers[4] = 0

        self.handle_ly_lyc_collision()

        if self.registers[4] >= 144:
            self.set_mode(1)

        if self.registers[4] == 144 and old_ly == 143:
            self.interrupter.request_interrupt(0)
            self.start_render = True

    def handle_white_board(self):
        self.display_buffer = [[0 for _ in range(160)] for _ in range(144)]

    def render_scanline(self):
        is_unsigned = (self.registers[0] >> 4) & 1

        background_enable = self.registers[0] & 1
        if background_enable == 0:
            self.handle_white_board()

        tile_map = 0x9C00 if (self.registers[0] >> 3) & 1 else 0x9800

        global_y = (self.registers[4] + self.registers[2]) & 0xFF

        tile_row = global_y // 8

        map_row_start = tile_map + (tile_row * 32)

        sprites = self.get_sprites()
        sprites.sort(key=lambda s: (s[1], s[4]))

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
            if len(sprites) > 0:
                for sprite in sprites:
                    relative_x = pixel_x - (sprite[1] - 8)
                    if 0 <= relative_x < 8:
                        sprite_tile = 0x8000 + (sprite[2] * 16)
                        sprite_y_tile = (self.registers[4] - (sprite[0] - 16)) % 8
                        flip_y = (sprite[3] >> 6) & 1
                        if flip_y:
                            sprite_y_tile = 7 - sprite_y_tile

                        addrs_line = sprite_tile + (sprite_y_tile * 2)

                        sprite_low_byte = self.vram.read(addrs_line)
                        sprite_high_byte = self.vram.read(addrs_line+1)
                        flip_x = (sprite[3] >> 5) & 1
                        if flip_x:
                            sprite_color_id = ((sprite_high_byte >> (7 - relative_x)) & 1) << 1 | sprite_low_byte >> relative_x & 1
                        else:  
                            sprite_color_id = ((sprite_high_byte >> relative_x) & 1) << 1 | sprite_low_byte >> relative_x & 1
                        if sprite_color_id == 0:
                            self.display_buffer[self.registers[4]][pixel_x] = pixel_color_id
                            continue
                        priority = (sprite[3] >> 7) & 1
                        if not priority:
                            real_pixel = sprite_color_id
                        else:
                            real_pixel = sprite_color_id if pixel_color_id == 0 else pixel_color_id
                        self.display_buffer[self.registers[4]][pixel_x] = real_pixel 
            else:
                self.display_buffer[self.registers[4]][pixel_x] = pixel_color_id

    def get_sprites(self):
        ly = self.registers[4]
        sprite_list = []
        
        for i in range(40):
            if len(sprite_list) >= 10:
                return sprite_list
            base_addrs = 0xFE00 + (i * 4)
            y_pos = self.oam.read(base_addrs)
            if not (ly + 16 >= y_pos and ly + 16 < y_pos + 8):
                continue
            byte1_addrs = base_addrs + 1
            x_pos = self.oam.read(byte1_addrs)
            byte2_addrs = base_addrs + 2
            tile_pointer = self.oam.read(byte2_addrs)
            byte3_addrs = base_addrs + 3
            attributes = self.oam.read(byte3_addrs)
            sprite_data = [y_pos, x_pos, tile_pointer, attributes, i]
            sprite_list.append(sprite_data)
        return sprite_list
    
    def tick(self, cycles):
        lcd_mode = (self.registers[0] >> 7) & 1

        if not lcd_mode and not self.last_display_reset:
            self.reset_ppu_state()

        if lcd_mode:
            self.last_display_reset = False
            self.counter += cycles

            if self.counter >= 456:
                self.counter -= 456
                self.increment_ly()

            if self.registers[4] < 144:
                if self.counter < 80:
                    self.set_mode(2)
                elif self.counter < 252:
                    self.set_mode(3)
                else:
                    if self.get_mode() != 0:
                        self.render_scanline()
                    self.set_mode(0)

            self.update_stat_interrupt()
    
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
        elif offset == 6:
            self.dma_block = 164
            self.dma_src_addrs = value << 8
        else:
            self.registers[offset] = value

    def read(self, addrs):
        offset = addrs - self.offset_constant
        return self.registers[offset]

    def get_mode(self):
        return self.registers[1] & 0x03

    def read_vram(self, addrs):
        lcd_mode = (self.registers[0] >> 7) & 1
        if self.get_mode() != 3 or not lcd_mode:
            return self.vram.read(addrs)
        return 0xFF

    def write_vram(self, addrs, value):
        lcd_mode = (self.registers[0] >> 7) & 1
        if self.get_mode() != 3 or not lcd_mode:
            self.vram.write(addrs, value)

    def read_oam(self, addrs):
        lcd_mode = (self.registers[0] >> 7) & 1
        if self.get_mode() < 2 or not lcd_mode:
            return self.oam.read(addrs)
        return 0xFF

    def write_oam(self, addrs, value):
        lcd_mode = (self.registers[0] >> 7) & 1
        if self.get_mode() < 2 or not lcd_mode:
            self.oam.write(addrs, value)