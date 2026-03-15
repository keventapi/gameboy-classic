class RLA:
    def __init__(self, cpu):
        self.cpu = cpu
        

    def rla_instructions(self):
        instructions = {
            0x17: (self.execute_rla, (4))
        }
        return instructions

    def execute_rla(self, ticks):
        flag = self.cpu.registers["F"]
        old_C = (flag >> 4) & 1
        C = (self.cpu.registers["A"] >> 7) & 1
        value = (self.cpu.registers["A"] << 1) & 0xFF
        value = value | old_C
        Z = 0
        N = 0
        H = 0
        self.cpu.set_flags(Z, N, H, C)
        self.cpu.registers["A"] = value & 0xFF
        self.cpu.timer.tick(ticks)
        return ticks
