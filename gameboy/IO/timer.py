class TIMER:
    def __init__(self):
        self.TAC = 0
        self.frequency_selector = 0
        self.timer_status = 1
        self.frequency_map = {
            0b00: {"frequency": 4096,   "selector": 9, "cicle": 1024},
            0b01: {"frequency": 262144, "selector": 3, "cicle": 16},
            0b10: {"frequency": 65536,  "selector": 5, "cicle": 64},
            0b11: {"frequency": 16384,  "selector": 7, "cicle": 256}
        }
        self.regiters_map = {
            0xFF04: "DIV",
            0xFF05: "TIMA",
            0xFF06: "TMA",
            0xFF07: "TAC"
        }

        self.counters = {
            "DIV": 0x00,
            "TIMA": 0x00,
            "TMA": 0x00
        }

        self.internal_counter = 0

        self.interrupt = False
        self.div_state = 0

        self.reload_state = 0
        self.last_value = 0

    def set_tac_configurations(self):
        self.frequency_selector = self.TAC & 0b11
        self.timer_status = (self.TAC >> 2) & 0b1

    def save_last_state(self):
        self.last_value = self.internal_counter

    def check_tima_increment(self):
        if self.timer_status == 0:
            return False
        selector = self.frequency_map[self.frequency_selector]["selector"]
        current_bit = (self.internal_counter >> selector) & 0b1
        last_bit = (self.last_value >> selector) & 0b1
        return True if last_bit == 1 and current_bit == 0 else False

    def update_tima(self):
        if self.check_tima_increment():
            self.counters["TIMA"] += 1

        if self.counters["TIMA"] > 0xFF:
            self.counters["TIMA"] = 0
            self.interrupt = True
            self.reload_state = 4

    def update_div(self):
        if self.internal_counter % 4 == 0:
            self.counters["DIV"] = (self.counters["DIV"] + 1) & 0xFFFF 

    def tick(self, ticks):
        for _ in range(ticks):
            self.save_last_state()
            self.internal_counter = (self.internal_counter + 1) & 0xFFFF
            self.update_div()
            self.update_tima()
            if self.reload_state > 0:
                self.reload_state -= 1
                if self.reload_state == 0:
                    self.counters["TIMA"] = self.counters["TMA"]

    def write(self, addrs, value):
        name = self.regiters_map[addrs]
        if name == "DIV":
            self.internal_counter &= 0x0000
            self.counters["DIV"] &= 0x0000
        elif name == "TIMA":
            self.counters[name] = value
            self.reload_state = 0
        elif name == "TMA":
            self.counters[name] = value
        elif name == "TAC":
            self.TAC = 0xF8 | (value & 0x07)
            self.set_tac_configurations()

    def read(self, addrs):
        name = self.regiters_map[addrs]
        if name == "DIV":
            return (self.counters["DIV"] >> 8)
        if name == "TAC":
            return self.TAC & 0xFF
        return self.counters[name] & 0xFF
