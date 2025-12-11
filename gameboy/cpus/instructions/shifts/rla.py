class RLA:
    def __init__(self, cpu):
        self.cpu = cpu
        self.registers = self.cpu.registers

    def rla_instructions(self):
        instructions = {
            0x17: lambda: self.execute_rla(4)
        }
        return instructions

    def execute_rla(self, ticks):
        flag = self.registers["F"]
        old_C = (flag >> 4) & 1
        C = (self.registers["A"] >> 7) & 1
        value = (self.registers["A"] << 1) & 0xFF
        value = value | old_C
        Z = 0
        N = 0
        H = 0
        self.cpu.set_flags(Z, N, H, C)
        self.registers["A"] = value & 0xFF
        self.cpu.timer.tick(ticks)
