class POP:
    def __init__(self, cpu):
        self.cpu = cpu
        self.pull8 = self.cpu.pull8
        self.registers = self.cpu.registers
        self.mmu = self.cpu.mmu

    def pop_instructions(self):
        instructions = {
            0xF1: (self.execute_pop, ("AF", 12)),
            0xC1: (self.execute_pop, ("BC", 12)),
            0xD1: (self.execute_pop, ("DE", 12)),
            0xE1: (self.execute_pop, ("HL", 12))
        }
        return instructions

    def execute_pop(self, r16, ticks):
        high = r16[0]
        low = r16[1]
        val_low = self.pull8()
        val_high = self.pull8()
        if low == "F":
            self.registers[low] = val_low & 0xF0
        else:
            self.registers[low] = val_low
        self.registers[high] = val_high
        self.cpu.timer.tick(ticks)
        return ticks
