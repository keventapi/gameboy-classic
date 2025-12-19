class NOP:
    def __init__(self, cpu):
        self.cpu = cpu

    def intructions_nop(self):
        instructions = {
            0x00: lambda: self.execute_nop(4)
        }
        return instructions

    def execute_nop(self, ticks):
        self.cpu.timer.tick(ticks)
        return ticks
