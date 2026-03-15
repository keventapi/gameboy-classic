class SCF:  # Flags podem ser otimizadas para nn precisar tocar no Z
    def __init__(self, cpu):
        self.cpu = cpu
        

    def instructions_scf(self):
        instructions = {
            0x37: (self.execute_scf, (4))
        }
        return instructions

    def execute_scf(self, ticks):
        flag = self.cpu.registers["F"]
        Z = (flag >> 7) & 1
        N = 0
        H = 0
        C = 1
        self.cpu.set_flags(Z, N, H, C)
        self.cpu.timer.tick(ticks)
        return ticks
