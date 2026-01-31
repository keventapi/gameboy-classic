class LD_A_FF00_N:
    def __init__(self, cpu):
        self.cpu = cpu
        self.fetch = self.cpu.fetch
        self.registers = self.cpu.registers
        self.mmu = self.cpu.mmu

    def ld_a_ff00_n_instructions(self):
        instructions = {
            0xE0: (self.execute_ld_a_ff00_n, (False, 12)),
            0xF0: (self.execute_ld_a_ff00_n, (True, 12))
        }
        return instructions

    def execute_ld_a_ff00_n(self, update_a, ticks):
        value = self.fetch()
        if update_a:
            self.registers["A"] = self.mmu.read((value+0xFF00) & 0xFFFF)
        else:
            self.mmu.write((value+0xFF00) & 0xFFFF, self.registers["A"])
        self.cpu.timer.tick(ticks)
        return ticks
