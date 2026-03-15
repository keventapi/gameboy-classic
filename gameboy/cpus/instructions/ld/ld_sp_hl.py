class LD_SP_HL:
    def __init__(self, cpu):
        self.cpu = cpu
        
        self.mmu = self.cpu.mmu

    def ld_sp_hl_instructions(self):
        instructions = {
            0xF9: (self.execute_ld_sp_hl, (8))
        }
        return instructions

    def execute_ld_sp_hl(self, ticks):
        hl = (self.cpu.registers["H"] << 8) | self.cpu.registers["L"]
        self.cpu.registers["sp"] = hl
        self.cpu.timer.tick(ticks)
        return ticks
