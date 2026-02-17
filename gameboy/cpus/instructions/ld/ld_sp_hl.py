class LD_SP_HL:
    def __init__(self, cpu):
        self.cpu = cpu
        self.registers = self.cpu.registers
        self.mmu = self.cpu.mmu

    def ld_sp_hl_instructions(self):
        instructions = {
            0xF9: (self.execute_ld_sp_hl, (8))
        }
        return instructions

    def execute_ld_sp_hl(self, ticks):
        hl = (self.registers["H"] << 8) | self.registers["L"]
        self.registers["sp"] = hl
        self.cpu.timer.tick(ticks)
        return ticks
