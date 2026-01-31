class CPL:
    def __init__(self, cpu):
        self.cpu = cpu
        self.registers = self.cpu.registers

    def instructions_cpl(self):
        instructions = {
            0x2F: (self.execute_cpl, (4))
        }
        return instructions

    def execute_cpl(self, ticks):
        value = (self.registers["A"] & 0xFF) ^ 0xFF
        flag = self.registers["F"]
        Z = (flag >> 7) & 1
        N = 1
        H = 1
        C = (flag >> 4) & 1
        self.cpu.set_flags(Z, N, H, C)
        self.registers["A"] = value & 0xFF
        self.cpu.timer.tick(ticks)
        return ticks
