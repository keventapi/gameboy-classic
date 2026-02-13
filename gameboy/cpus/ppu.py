class PPU:
    def __init__(self, vram, interrupter, oam):
        self.vram = vram
        self.interrupter = interrupter
        self.oam = oam
        self.offset_constant = 0xFF40

        self.dma_block = 0
        self.dma_src_addrs = None
        self.registers = [
            0x91,  # LCDC
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

        self.window_counter = 0

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
            self.window_counter = 0

        self.handle_ly_lyc_collision()

        if self.registers[4] >= 144:
            self.set_mode(1)

        if self.registers[4] == 144 and old_ly == 143:
            self.interrupter.request_interrupt(0)
            self.start_render = True

    def handle_white_board(self):
        self.display_buffer = [[0 for _ in range(160)] for _ in range(144)]

    def render_bg(self, render_state, tile_row, global_y, global_x):
        map_selector = (render_state >> 3) & 1
        tile_map = 0x9C00 if map_selector else 0x9800
        tile_col = global_x // 8
        tile_row_start = tile_map + (tile_row * 32)
        tile_id = self.vram.read(tile_row_start + tile_col)

        if not (render_state >> 4) & 1:
            tile_id_signed = tile_id
            if tile_id_signed >= 0x80:
                tile_id_signed -= 0x100
            base_addrs = 0x9000 + (tile_id_signed * 16)
        else:
            base_addrs = 0x8000 + (tile_id * 16)

        y_inside_tile = global_y % 8
        line_addrs = base_addrs + (y_inside_tile * 2)

        low_byte = self.vram.read(line_addrs)
        high_byte = self.vram.read(line_addrs + 1)

        bit_index = 7 - (global_x % 8)

        pixel_color_id = ((high_byte >> bit_index) & 1) << 1
        pixel_color_id |= (low_byte >> bit_index) & 1

        return pixel_color_id

    def render_window(self, render_state, pixel_x):
        map_selector = (render_state >> 6) & 1
        tile_map = 0x9C00 if map_selector else 0x9800

        global_y = self.window_counter
        global_x = pixel_x - (self.registers[11] - 7)

        tile_row = global_y // 8
        tile_col = global_x // 8
        tile_row_start = tile_map + (tile_row * 32)
        tile_id = self.vram.read(tile_row_start + tile_col)

        if not (render_state >> 4) & 1:
            tile_id_signed = tile_id
            if tile_id_signed >= 0x80:
                tile_id_signed -= 0x100
            base_addrs = 0x9000 + (tile_id_signed * 16)
        else:
            base_addrs = 0x8000 + (tile_id * 16)

        y_inside_tile = global_y % 8
        line_addrs = base_addrs + (y_inside_tile * 2)

        low_byte = self.vram.read(line_addrs)
        high_byte = self.vram.read(line_addrs + 1)

        bit_index = 7 - (global_x % 8)

        pixel_color_id = ((high_byte >> bit_index) & 1) << 1
        pixel_color_id |= (low_byte >> bit_index) & 1

        return pixel_color_id

    def handle_8x8_sprite(self, pixel_x, sprite, pixel_color_id):
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
                sprite_color_id = ((sprite_high_byte >> relative_x) & 1) << 1 | (sprite_low_byte >> relative_x) & 1
            else:
                relative_x = (7 - relative_x)
                sprite_color_id = ((sprite_high_byte >> relative_x) & 1) << 1 | (sprite_low_byte >> relative_x) & 1

            if (sprite[3] >> 4) & 1:
                obp1 = self.registers[9]
                id = sprite_color_id * 2
                sprite_color_id = (obp1 >> id) & 0x03
            else:
                obp0 = self.registers[8]
                id = sprite_color_id * 2
                sprite_color_id = (obp0 >> id) & 0x03

            if sprite_color_id == 0:
                return 0

            priority = (sprite[3] >> 7) & 1
            if not priority:
                real_pixel = sprite_color_id
            else:
                real_pixel = sprite_color_id if pixel_color_id == 0 else pixel_color_id
            pixel_id = real_pixel

            return pixel_id
        return 0

    def handle_8x16_sprite(self, pixel_x, sprite, pixel_color_id):
        ly_relative = self.registers[4] - (sprite[0] - 16)
        sprite_pos = None
        flip_y = (sprite[3] >> 6) & 1

        if ly_relative >= 8:
            sprite[2] |= 0x01
            sprite_pos = 1
        else:
            sprite[2] &= 0xFe
            sprite_pos = 0

        if flip_y:
            if sprite_pos == 1:
                sprite[2] &= 0xFE
            else:
                sprite[2] |= 0x01

        return self.handle_8x8_sprite(pixel_x, sprite, pixel_color_id)

    def render_sprite(self, sprite_buffer, render_state, pixel_x, pixel_color_id):
        pixel_id = 0
        obj_type = (render_state >> 2) & 1
        for sprite in sprite_buffer:
            if not obj_type:
                sprite_pixel_id = self.handle_8x8_sprite(pixel_x, sprite, pixel_color_id)
                if sprite_pixel_id != 0:
                    pixel_id = sprite_pixel_id
                    return sprite_pixel_id
            else:
                sprite_pixel_id = self.handle_8x16_sprite(pixel_x, sprite, pixel_color_id)
                if sprite_pixel_id != 0:
                    return sprite_pixel_id

        return pixel_id

    def handle_display_buffer(self, pixel_x, pixel_color):
        self.display_buffer[self.registers[4]][pixel_x] = pixel_color

    def render_scanline(self):
        render_state = self.registers[0]
        bg_n_window_enabled = render_state & 1
        if not bg_n_window_enabled:
            return self.handle_white_board()
        window_enabled = (render_state >> 5) & 1
        sprite_enabled = (render_state >> 1) & 1        
        global_y = (self.registers[4] + self.registers[2]) & 0xFF
        tile_row = global_y // 8
        sprite_buffer = self.get_sprites()

        sprite_buffer.sort(key=lambda s: (s[1], s[4]))

        window_rendered = False

        for pixel_x in range(160):
            global_x = (pixel_x + self.registers[3]) & 0xFF
            pixel_color = 0

            bg_pixel_color = self.render_bg(render_state, tile_row, global_y, global_x)
            if bg_pixel_color:
                pixel_color = bg_pixel_color

            trigger = self.registers[11] - 7
            if window_enabled and self.registers[4] >= self.registers[10] and pixel_x >= trigger:
                window_pixel_color = self.render_window(render_state, pixel_x)
                window_rendered = True
                if window_pixel_color:
                    pixel_color = window_pixel_color

            if sprite_enabled and len(sprite_buffer) > 0:
                sprite_pixel = self.render_sprite(sprite_buffer, render_state, pixel_x, pixel_color)
                if sprite_pixel:
                    pixel_color = sprite_pixel
                if sprite_pixel is None:
                    print(sprite_pixel)
                    continue
            self.handle_display_buffer(pixel_x, pixel_color)

        if window_rendered:
            self.window_counter += 1

    def get_sprites(self):
        ly = self.registers[4]
        sprite_list = []
        mode = 16 if self.registers[0] >> 2 & 1 else 8
        for i in range(40):
            if len(sprite_list) >= 10:
                return sprite_list
            base_addrs = 0xFE00 + (i * 4)
            y_pos = self.oam.read(base_addrs)
            if not (ly + 16 >= y_pos and ly + 16 < y_pos + mode):
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
