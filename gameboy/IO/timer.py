class TIMER:
    def __init__(self, ppu):
        self.ppu = ppu

        self.TAC = 0
        self.frequency_selector = 0
        self.timer_status = 0
        self.frequency_map = [9, 3, 5, 7]

        self.offset_const = 0xFF04

        self.counters = [
            0,
            0,
            0
        ]

        self.internal_counter = 0

        self.div_state = 0

        self.reload_state = 0
        self.last_value = 0

    def set_tac_configurations(self):
        self.frequency_selector = self.TAC & 0b11
        self.timer_status = (self.TAC >> 2) & 0b1

    def save_last_state(self):
        self.last_value = self.internal_counter

    def check_tima_increment(self):
        selector = self.frequency_map[self.frequency_selector]

        current_signal = ((self.internal_counter >> selector) & 1) & self.timer_status
        last_signal = ((self.last_value >> selector) & 1) & self.timer_status

        return last_signal == 1 and current_signal == 0

    def update_tima(self):
        if self.check_tima_increment():
            self.counters[1] += 1

        if self.counters[1] > 0xFF:
            self.counters[1] = 0
            self.reload_state = 4
            # self.interrupter.request_interrupt(2)

    def dma_handler(self, ticks):
        for _ in range(ticks):
            if self.ppu.dma_block > 0 and self.ppu.dma_src_addrs is not None:
                addrs = self.ppu.dma_src_addrs + (160 - self.ppu.dma_block)
                data = self.mmu.read(addrs, True)
                self.ppu.oam.write(0xFE00 + (160 - self.ppu.dma_block), data)
                self.ppu.dma_block -= 1
            elif self.ppu.dma_src_addrs is not None:
                self.ppu.dma_src_addrs = None

    def tick(self, ticks):
        self.save_last_state()
        self.internal_counter = (self.internal_counter + ticks) & 0xFFFF

        self.update_tima()
        self.ppu.tick(ticks)
        # self.dma_handler(ticks)

        if self.reload_state > 0:
            self.reload_state -= ticks
            if self.reload_state <= 0:
                self.counters[1] = self.counters[2]
                self.reload_state = 0
                self.interrupter.request_interrupt(2)

    def write(self, addrs, value):
        offset = addrs - self.offset_const
        if offset == 0:
            self.internal_counter &= 0x0000
            self.counters[0] &= 0x0000
        elif offset == 1:
            self.counters[offset] = value
            self.reload_state = 0
        elif offset == 2:
            self.counters[offset] = value
        elif offset == 3:
            self.TAC = 0xF8 | (value & 0x07)
            self.set_tac_configurations()

    def read(self, addrs):
        offset = addrs - self.offset_const
        if offset == 0:
            return (self.internal_counter >> 8) & 0xFF
        if offset == 3:
            return self.TAC & 0xFF
        return self.counters[offset] & 0xFF
