class CPL:
    def __init__(self, cpu):
        self.cpu = cpu
        

    def instructions_cpl(self):
        instructions = {
            0x2F: (self.execute_cpl, (4))
        }
        return instructions

    def execute_cpl(self, ticks):
        value = (self.cpu.registers["A"] & 0xFF) ^ 0xFF
        flag = self.cpu.registers["F"]
        Z = (flag >> 7) & 1
        N = 1
        H = 1
        C = (flag >> 4) & 1
        self.cpu.set_flags(Z, N, H, C)
        self.cpu.registers["A"] = value & 0xFF
        self.cpu.timer.tick(ticks)
        return ticks
