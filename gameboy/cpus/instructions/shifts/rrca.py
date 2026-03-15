class RRCA:
    def __init__(self, cpu):
        self.cpu = cpu
        

    def rrca_instructions(self):
        instructions = {
            0x0F: (self.execute_rrca, (4))
        }
        return instructions

    def execute_rrca(self, ticks):
        A = self.cpu.registers["A"]
        C = A & 1
        A = (A >> 1) & 0xFF
        A = (C << 7) | A
        Z = 0
        N = 0
        H = 0
        self.cpu.set_flags(Z, N, H, C)
        self.cpu.registers["A"] = A & 0xFF
        self.cpu.timer.tick(ticks)
        return ticks
