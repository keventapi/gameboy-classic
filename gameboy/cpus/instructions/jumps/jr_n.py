class JR_N:
    def __init__(self, cpu):
        self.cpu = cpu
        self.registers = self.cpu.registers
        self.mmu = self.cpu.mmu

    def jr_n_instructions(self):
        instructions = {
            0x18: (self.execute_jr_n, (12))
        }
        return instructions

    def execute_jr_n(self, ticks):
        addrs = self.cpu.fetch()
        n = addrs
        if n >= 0x80:
            n -= 0x100
        self.registers["pc"] = (self.registers["pc"] + n) & 0xFFFF
        self.cpu.timer.tick(ticks)
        return ticks
