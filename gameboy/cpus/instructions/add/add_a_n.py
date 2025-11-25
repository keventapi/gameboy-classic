class ADD_A_N:
    def __init__(self, cpu):
        self.cpu = cpu
        self.pull8 = self.cpu.pull8
        self.fetch = self.cpu.fetch
        self.registers = self.cpu.registers
        self.mmu = self.cpu.mmu

    def add_a_n_instructions(self):
        instructions = {
            0x87: lambda: self.execute_add_a_n("A"),
            0x80: lambda: self.execute_add_a_n("B"),
            0x81: lambda: self.execute_add_a_n("C"),
            0x82: lambda: self.execute_add_a_n("D"),
            0x83: lambda: self.execute_add_a_n("E"),
            0x84: lambda: self.execute_add_a_n("H"),
            0x85: lambda: self.execute_add_a_n("L"),
            0x86: lambda: self.execute_add_a_n("HL"),
            0xC6: lambda: self.execute_add_a_n("#")
        }
        return instructions

    def execute_add_a_n(self, r):
        if len(r) > 1 or r == "#":
            if r == "#":
                n = self.fetch()
            else:
                addrs = (self.registers[r[0]] << 8) | self.registers[r[1]]
                n = self.mmu.read(addrs)
        else:
            n = self.registers[r]

        sum = n + self.registers["A"]

        # Z
        if sum & 0xFF == 0:
            self.registers["F"] |= 0b10000000
        else:
            self.registers["F"] &= 0b01111111

        # N
        self.registers["F"] &= 0b10111111

        # H
        if ((self.registers["A"] & 0xF) + (n & 0xF)) > 0xF:
            self.registers["F"] |= 0b00100000
        else:
            self.registers["F"] &= 0b11011111
        # C
        if sum > 0xFF:
            self.registers["F"] |= 0b00010000
        else:
            self.registers["F"] &= 0b11101111
        self.registers["A"] = sum & 0xFF

        self.registers["F"] &= 0xF0
