class LD_A_FF00_C:
    def __init__(self):
        pass

    def ld_a_ff00_c_instructions(self):
        instructions = {
            0xF2: lambda: self.execute_ld_a_FF00_C(True),
            0xE2: lambda: self.execute_ld_a_FF00_C(False)
        }
        return instructions

    def execute_ld_a_FF00_C(self, read_a: bool):
        addrs = 0xFF00 + self.registers["C"]
        if read_a:
            self.registers["A"] = self.mmu.read(addrs)
        else:
            self.mmu.write(addrs, self.registers["A"])
        
        return None