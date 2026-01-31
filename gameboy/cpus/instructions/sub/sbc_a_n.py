class SBC_A_N:
    def __init__(self, cpu):
        self.cpu = cpu
        self.registers = self.cpu.registers
        self.mmu = self.cpu.mmu
        self.fetch = self.cpu.fetch

    def sbc_a_n_intructions(self):
        instructions = {
            0x9F: (self.execute_sbc_a_n, ("A", 4)),
            0x98: (self.execute_sbc_a_n, ("B", 4)),
            0x99: (self.execute_sbc_a_n, ("C", 4)),
            0x9A: (self.execute_sbc_a_n, ("D", 4)),
            0x9B: (self.execute_sbc_a_n, ("E", 4)),
            0x9C: (self.execute_sbc_a_n, ("H", 4)),
            0x9D: (self.execute_sbc_a_n, ("L", 4)),
            0x9E: (self.execute_sbc_a_n, ("HL", 8)),
            0xDE: (self.execute_sbc_a_n, ("#", 8))
        }
        return instructions

    def execute_sbc_a_n(self, r, ticks):
        A = self.registers["A"] & 0xFF
        if r == "HL":
            addrs = (self.registers["H"] << 8) | self.registers["L"]
            n = self.mmu.read(addrs)
        elif r == "#":
            n = self.cpu.fetch()
        else:
            n = self.registers[r]

        n &= 0xFF
        carry_flag = ((self.registers["F"] & 0xF0) >> 4) & 1

        sub = A - n - carry_flag

        Z = 1 if (sub & 0xFF) == 0 else 0
        N = 1
        H = 1 if (A & 0xF) - (n & 0xF) - carry_flag < 0 else 0
        C = 1 if sub < 0 else 0

        self.registers["A"] = sub & 0xFF
        self.cpu.set_flags(Z, N, H, C)
        self.cpu.timer.tick(ticks)
        return ticks
