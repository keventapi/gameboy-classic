class SRL_N:
    def __init__(self, cpu):
        self.cpu = cpu
        self.registers = self.cpu.registers
        self.mmu = self.cpu.mmu

    def srl_n_instructions(self):
        instructions = {
            0x3F: lambda: self.execute_srl_n("A", 8),
            0x38: lambda: self.execute_srl_n("B", 8),
            0x39: lambda: self.execute_srl_n("C", 8),
            0x3A: lambda: self.execute_srl_n("D", 8),
            0x3B: lambda: self.execute_srl_n("E", 8),
            0x3C: lambda: self.execute_srl_n("H", 8),
            0x3D: lambda: self.execute_srl_n("L", 8),
            0x3E: lambda: self.execute_srl_n("HL", 16),
        }
        return instructions

    def execute_srl_n(self, r, ticks):
        if r == "HL":
            addrs = (self.registers["H"] << 8) | self.registers["L"]
            value = self.mmu.read(addrs)
        else:
            value = self.registers[r]

        C = value & 1
        value = (value >> 1) & 0xFF
        Z = 1 if value == 0 else 0
        H = 0
        N = 0
        self.cpu.set_flags(Z, N, H, C)

        if r == "HL":
            self.mmu.write(addrs, value)
        else:
            self.registers[r] = value
        self.cpu.timer.tick(ticks)
        return ticks
