class RLCA:
    def __init__(self, cpu):
        self.cpu = cpu
        self.registers = self.cpu.registers

    def rlca_instructions(self):
        instructions = {
            0x07: lambda: self.execute_rlca(4)
        }
        return instructions

    def execute_rlca(self, ticks):
        bit7 = (self.registers["A"] >> 7) & 1
        value = (self.registers["A"] << 1) & 0xFF
        value = (value | bit7) & 0XFF
        Z = 0
        N = 0
        H = 0
        C = bit7
        self.cpu.set_flags(Z, N, H, C)
        self.registers["A"] = value
        self.cpu.timer.tick(ticks)
        return ticks
