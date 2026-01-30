class HALT:
    def __init__(self, cpu):
        self.cpu = cpu

    def instructions_halt(self):
        instructions = {
            0x76: (self.execute_halt, (4))
        }
        return instructions

    def execute_halt(self, ticks):
        self.cpu.is_halted = True
        self.cpu.timer.tick(ticks)
        return ticks
