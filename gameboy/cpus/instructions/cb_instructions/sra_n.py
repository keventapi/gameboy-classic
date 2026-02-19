class SRA_N:
    def __init__(self, cpu):
        self.cpu = cpu
        self.registers = self.cpu.registers
        self.mmu = self.cpu.mmu

    def sra_n_instructions(self):
        instructions = {
            0x2F: (self.execute_sra_n, ("A", 8)),
            0x28: (self.execute_sra_n, ("B", 8)),
            0x29: (self.execute_sra_n, ("C", 8)),
            0x2A: (self.execute_sra_n, ("D", 8)),
            0x2B: (self.execute_sra_n, ("E", 8)),
            0x2C: (self.execute_sra_n, ("H", 8)),
            0x2D: (self.execute_sra_n, ("L", 8)),
            0x2E: (self.execute_sra_n, ("HL", 16))
        }
        return instructions

    def execute_sra_n(self, r, ticks):
        self.cpu.timer.tick(4)
        if r == "HL":
            addrs = (self.registers["H"] << 8) | self.registers["L"]
            value = self.mmu.read(addrs)
            self.cpu.timer.tick(4)
        else:
            value = self.registers[r]
        bit7 = (value >> 7) & 1
        C = value & 1
        value = (value >> 1) & 0xFF
        value = value | (bit7 << 7)
        Z = 1 if value == 0 else 0
        H = 0
        N = 0
        self.cpu.set_flags(Z, N, H, C)

        if r == "HL":
            self.mmu.write(addrs, value)
            self.cpu.timer.tick(4)
        else:
            self.registers[r] = value

        self.cpu.timer.tick(4)
        return ticks
