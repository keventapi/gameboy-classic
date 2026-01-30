class CCF:
    def __init__(self, cpu):
        self.cpu = cpu
        self.registers = self.cpu.registers

    def instructions_ccf(self):
        instructions = {
            0x3F: (self.execute_ccf, (4))
        }
        return instructions

    def execute_ccf(self, ticks):
        flag = self.registers["F"]
        Z = (flag >> 7) & 1
        N = 0
        H = (flag >> 4) & 1
        C = ((flag >> 4) ^ 1) & 1
        self.cpu.set_flags(Z, N, H, C)
        self.cpu.timer.tick(ticks)
        return ticks
