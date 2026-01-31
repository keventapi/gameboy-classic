class RRC_N:
    def __init__(self, cpu):
        self.cpu = cpu
        self.registers = self.cpu.registers
        self.mmu = self.cpu.mmu

    def rrc_n_instructions(self):
        instructions = {
            0x0F: (self.execute_rrc_n, ("A", 8)),
            0x08: (self.execute_rrc_n, ("B", 8)),
            0x09: (self.execute_rrc_n, ("C", 8)),
            0x0A: (self.execute_rrc_n, ("D", 8)),
            0x0B: (self.execute_rrc_n, ("E", 8)),
            0x0C: (self.execute_rrc_n, ("H", 8)),
            0x0D: (self.execute_rrc_n, ("L", 8)),
            0x0E: (self.execute_rrc_n, ("HL", 16))
        }
        return instructions

    def execute_rrc_n(self, r, ticks):
        if r == "HL":
            addrs = (self.registers["H"] << 8) | self.registers["L"]
            value = self.mmu.read(addrs)
        else:
            value = self.registers[r]
        C = value & 1
        value = (value >> 1) | (C << 7)
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
        return ticks
