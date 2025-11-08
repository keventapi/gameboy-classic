class LD_A_FF00_N:
    def __init__(self):
        pass

    def ld_a_ff00_n_instructions(self):
        instructions = {
            0xE0: lambda: self.execute_ld_a_ff00_n(False),
            0xF0: lambda: self.execute_ld_a_ff00_n(True)
        }
        return instructions
    
    def execute_ld_a_ff00_n(self, update_a):
        value = self.fetch()
        if update_a:
            self.registers["A"] = self.mmu.read(0xFF00 + value)
        else:
            self.mmu.write(value+0xFF00, self.registers["A"])