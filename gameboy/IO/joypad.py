class JOYPAD:
    def __init__(self):
        self.joyp = 0xC0
        self.dpad = 0xF
        self.action = 0xF

    def handle_key_press(self, bit, map):
        if map == "dpad":
            not_pressed = (self.dpad >> bit) & 1
            if not_pressed:
                self.dpad ^ (1 << bit)
            else:
                self.dpad | (1 << bit)
        else:
            not_pressed = (self.action >> bit) & 1
            if not_pressed:
                self.action ^ (1 << bit)     
            else:
                self.action | (1 << bit)

    def write(self, value):
        self.joyp = 0xC0 | (value & 0x30)

    def fetch_buttons(self, map):
        if map == "action":
            return (self.joyp & 0xF0) | self.action
        else:
            return (self.joyp & 0xF0) | self.dpad

    def read(self):
        result = self.joyp
        if not (self.joyp & 0x10):
            result = self.fetch_buttons("action")
        elif not (self.joyp & 0x20):
            result = self.fetch_buttons("dpad")

        return result
