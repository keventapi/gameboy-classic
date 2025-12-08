class SBC_A_N:
    def __init__(self, cpu):
        self.cpu = cpu
        self.registers = self.cpu.registers
        self.mmu = self.cpu.mmu
        self.fetch = self.cpu.fetch

    def sbc_a_n_intructions(self):
        instructions = {
            0x9F: lambda: self.execute_sbc_a_n("A", 4),
            0x98: lambda: self.execute_sbc_a_n("B", 4),
            0x99: lambda: self.execute_sbc_a_n("C", 4),
            0x9A: lambda: self.execute_sbc_a_n("D", 4),
            0x9B: lambda: self.execute_sbc_a_n("E", 4),
            0x9C: lambda: self.execute_sbc_a_n("H", 4),
            0x9D: lambda: self.execute_sbc_a_n("L", 4),
            0x9E: lambda: self.execute_sbc_a_n("HL", 8)
        }
        return instructions

    def execute_sbc_a_n(self, r, ticks):
        A = self.registers["A"]
        if r == "HL":
            addrs = (self.registers["H"] << 8) | self.registers["L"]
            n = self.mmu.read(addrs)
        else:
            n = self.registers[r]

        n &= 0xFF
        carry_flag = (self.registers["F"] >> 4) & 1

        sub = A - (n + carry_flag)

        # Z
        if (sub & 0xFF) == 0:
            self.registers["F"] |= 0b10000000
        else:
            self.registers["F"] &= 0b01111111

        # N
        self.registers["F"] |= 0b01000000

        # H
        if (A & 0xF) < ((n & 0xF) + carry_flag):
            self.registers["F"] |= 0b00100000
        else:
            self.registers["F"] &= 0b11011111

        # C
        if A < (n + carry_flag):
            self.registers["F"] |= 0b00010000
        else:
            self.registers["F"] &= 0b11101111

        self.registers["A"] = sub & 0xFF
        self.registers["F"] &= 0xF0

        self.cpu.timer.tick(ticks)
