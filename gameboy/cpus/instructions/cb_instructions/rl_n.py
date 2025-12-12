class RL_N:
    def __init__(self, cpu):
        self.cpu = cpu
        self.registers = self.cpu.registers
        self.mmu = self.cpu.mmu

    def rl_n_instructions(self):
        instructions = {
            0x17: lambda: self.execute_rl_n("A", 8),
            0x10: lambda: self.execute_rl_n("B", 8),
            0x11: lambda: self.execute_rl_n("C", 8),
            0x12: lambda: self.execute_rl_n("D", 8),
            0x13: lambda: self.execute_rl_n("E", 8),
            0x14: lambda: self.execute_rl_n("H", 8),
            0x15: lambda: self.execute_rl_n("L", 8),
            0x16: lambda: self.execute_rl_n("HL", 16)
        }
        return instructions

    def execute_rl_n(self, r, ticks):
        flag = self.registers["F"]

        if r == "HL":
            addrs = (self.registers["H"] << 8) | self.registers["L"]
            value = self.mmu.read(addrs)
        else:
            value = self.registers[r]

        old_C = (flag >> 4) & 1
        C = (value >> 7) & 1
        value = (value << 1) | old_C
        value &= 0xFF
        Z = 1 if value == 0 else 0
        N = 0
        H = 0
        if r == "HL":
            self.mmu.write(addrs, value)
        else:
            self.registers[r] = value
        self.cpu.set_flags(Z, N, H, C)
        self.cpu.timer.tick(ticks)
