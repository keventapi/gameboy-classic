class INTERRUPT_CONTROLLER:
    def __init__(self):
        self.IF = 0xE0
        self.IE = 0x00

    def read_if(self):
        return self.IF | 0xE0

    def write_if(self, value):
        self.IF = (value & 0x1F) | 0xE0

    def read_ie(self):
        return self.IE

    def write_ie(self, value):
        self.IE = value & 0x1F

    def request_interrupt(self, selector):
        self.IF = (self.IF | (1 << selector)) & 0xFF
