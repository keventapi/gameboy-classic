class RRA:
    def __init__(self, cpu):
        self.cpu = cpu
        self.registers = self.cpu.registers

    def rra_instructions(self):
        instructions = {
            0x1F: lambda: self.execute_rra(4)
        }
        return instructions

    def execute_rra(self, ticks):
        value = self.registers["A"]
        flag = self.registers["F"]
        old_C = (flag >> 4) & 1
        bit0 = value & 1
        value = (value >> 1) | (old_C << 7)
        value &= 0xFF
        C = bit0
        Z = 0
        N = 0
        H = 0
        self.registers["A"] = value
        self.cpu.set_flags(Z, N, H, C)
        self.cpu.timer.tick(ticks)
