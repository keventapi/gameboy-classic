class PUSH:
    def __init__(self, cpu):
        self.cpu = cpu
        self.registers = self.cpu.registers
        self.mmu = self.cpu.mmu

    def push_instructions(self):
        instructions = {
            0xF5: (self.execute_push, ("AF", 16)),
            0xC5: (self.execute_push, ("BC", 16)),
            0xD5: (self.execute_push, ("DE", 16)),
            0xE5: (self.execute_push, ("HL", 16))
        }
        return instructions

    def execute_push(self, r16, ticks):
        high = self.registers[r16[0]]
        low = self.registers[r16[1]]
        addrs = (high << 8) | low
        self.cpu.push16(addrs)
        self.cpu.timer.tick(ticks)
        return ticks
