class JOYPAD:
    def __init__(self):
        self.joyp = 0xC0
        self.dpad = {
            "right": 1,
            "left": 1,
            "up": 1,
            "down": 1
        }
        self.action = {
            "A": 1,
            "B": 1,
            "select": 1,
            "start": 1
        }

    def write(self, value):
        self.joyp = 0xC0 | (value & 0x30)

    def fetch_action_output(self):
        bit0 = self.action["A"]
        bit1 = self.action["B"]
        bit2 = self.action["select"]
        bit3 = self.action["start"]
        return (bit3 << 3) | (bit2 << 2) | (bit1 << 1) | bit0

    def fetch_dpad_output(self):
        bit0 = self.dpad["right"]
        bit1 = self.dpad["left"]
        bit2 = self.dpad["up"]
        bit3 = self.dpad["down"]
        return (bit3 << 3) | (bit2 << 2) | (bit1 << 1) | bit0

    def read(self):
        result = 0xC0
        result |= (self.joyp & 0x30)
        button_state_output = 0x0F
        if not (self.joyp & 0x20):
            button_state_output &= self.fetch_dpad_output()
        if not (self.joyp & 0x10):
            button_state_output &= self.fetch_action_output()
        return result | button_state_output
