class SUB_A_N:
    def __init__(self, cpu):
        self.cpu = cpu
        self.registers = self.cpu.registers
        self.mmu = self.cpu.mmu
        self.fetch = self.cpu.fetch

    def sub_a_n_instructions(self):
        instructions = {
            0x97: lambda: self.execute_sub_a_n("A"),
            0x90: lambda: self.execute_sub_a_n("B"),
            0x91: lambda: self.execute_sub_a_n("C"),
            0x92: lambda: self.execute_sub_a_n("D"),
            0x93: lambda: self.execute_sub_a_n("E"),
            0x94: lambda: self.execute_sub_a_n("H"),
            0x95: lambda: self.execute_sub_a_n("L"),
            0x96: lambda: self.execute_sub_a_n("HL"),
            0xD6: lambda: self.execute_sub_a_n("#")
        }
        return instructions

    def execute_sub_a_n(self, r):
        A = self.registers["A"]
        if r == "HL":
            addrs = (self.registers["H"] << 8) | self.registers["L"]
            n = self.mmu.read(addrs)
        elif r == "#":
            n = self.fetch()
        else:
            n = self.registers[r]

        n &= 0xFF
        sub = A - n

        # Z
        if sub & 0xFF == 0:
            self.registers["F"] |= 0b10000000
        else:
            self.registers["F"] &= 0b01111111

        # N
        self.registers["F"] |= 0b01000000

        # H
        if (A & 0xF) < (n & 0xF):
            self.registers["F"] |= 0b00100000
        else:
            self.registers["F"] &= 0b11011111

        # C
        if A < n:
            self.registers["F"] |= 0b00010000
        else:
            self.registers["F"] &= 0b11101111

        self.registers["A"] = sub & 0xFF
        self.registers["F"] &= 0xF0
