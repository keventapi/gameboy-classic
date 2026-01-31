class LD_A_FF00_C:
    def __init__(self, cpu):
        self.cpu = cpu
        self.registers = self.cpu.registers
        self.mmu = self.cpu.mmu

    def ld_a_ff00_c_instructions(self):
        instructions = {
            0xF2: (self.execute_ld_a_FF00_C, (True, 8)),
            0xE2: (self.execute_ld_a_FF00_C, (False, 8))
        }
        return instructions

    def execute_ld_a_FF00_C(self, read_a: bool, ticks):
        addrs = 0xFF00 + self.registers["C"]
        if read_a:
            self.registers["A"] = self.mmu.read(addrs)
        else:
            self.mmu.write(addrs & 0xFFFF, self.registers["A"])
        self.cpu.timer.tick(ticks)
        return ticks
