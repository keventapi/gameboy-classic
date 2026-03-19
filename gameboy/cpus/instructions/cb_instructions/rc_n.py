class RC_N:
    def __init__(self, cpu):
        self.cpu = cpu
        self.mmu = self.cpu.mmu

    def rc_n_instructions(self):
        instructions = {
            0x1F: (self.execute_rc_n, ("A", 8)),
            0x18: (self.execute_rc_n, ("B", 8)),
            0x19: (self.execute_rc_n, ("C", 8)),
            0x1A: (self.execute_rc_n, ("D", 8)),
            0x1B: (self.execute_rc_n, ("E", 8)),
            0x1C: (self.execute_rc_n, ("H", 8)),
            0x1D: (self.execute_rc_n, ("L", 8)),
            0x1E: (self.execute_rc_n, ("HL", 16))
        }
        return instructions

    def execute_rc_n(self, r, ticks):
        self.cpu.timer.tick(4)
        flag = self.cpu.registers["F"]
        if r == "HL":
            addrs = (self.cpu.registers["H"] << 8) | self.cpu.registers["L"]
            value = self.mmu.read(addrs)
            self.cpu.timer.tick(4)
        else:
            value = self.cpu.registers[r]
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
            self.cpu.timer.tick(4)
        else:
            self.cpu.registers[r] = value
        self.cpu.timer.tick(4)
        return ticks
