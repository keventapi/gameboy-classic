class RC_N:
    def __init__(self, cpu):
        self.cpu = cpu
        self.registers = self.cpu.registers
        self.mmu = self.cpu.mmu

    def rc_n_instructions(self):
        instructions = {
            0x1F: lambda: self.execute_rc_n("A", 8),
            0x18: lambda: self.execute_rc_n("B", 8),
            0x19: lambda: self.execute_rc_n("C", 8),
            0x1A: lambda: self.execute_rc_n("D", 8),
            0x1B: lambda: self.execute_rc_n("E", 8),
            0x1C: lambda: self.execute_rc_n("H", 8),
            0x1D: lambda: self.execute_rc_n("L", 8),
            0x1E: lambda: self.execute_rc_n("HL", 16)
        }
        return instructions

    def execute_rc_n(self, r, ticks):
        flag = self.registers["F"]
        if r == "HL":
            addrs = (self.registers["H"] << 8) | self.registers["L"]
            value = self.mmu.read(addrs)
        else:
            value = self.registers[r]
        old_C = (flag >> 4) & 1
        C = value & 1
        value = (value >> 1) | (old_C << 7)
        value &= 0xFF
        Z = 1 if value == 0 else 0
        H = 0
        N = 0
        self.cpu.set_flags(Z, N, H, C)
        if r == "HL":
            self.mmu.write(addrs, value)
        else:
            self.registers[r] = value
        self.cpu.timer.tick(ticks)
