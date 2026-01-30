class SUB_A_N:
    def __init__(self, cpu):
        self.cpu = cpu
        self.mmu = self.cpu.mmu
        self.fetch = self.cpu.fetch

    def sub_a_n_instructions(self):
        instructions = {
            0x97: (self.execute_sub_a_n, ("A", 4)),
            0x90: (self.execute_sub_a_n, ("B", 4)),
            0x91: (self.execute_sub_a_n, ("C", 4)),
            0x92: (self.execute_sub_a_n, ("D", 4)),
            0x93: (self.execute_sub_a_n, ("E", 4)),
            0x94: (self.execute_sub_a_n, ("H", 4)),
            0x95: (self.execute_sub_a_n, ("L", 4)),
            0x96: (self.execute_sub_a_n, ("HL", 8)),
            0xD6: (self.execute_sub_a_n, ("#", 8))
        }
        return instructions

    def execute_sub_a_n(self, r, ticks):
        A = self.cpu.registers["A"] & 0xFF
        if r == "HL":
            addrs = (self.cpu.registers["H"] << 8) | self.cpu.registers["L"]
            n = self.mmu.read(addrs)
        elif r == "#":
            n = self.fetch() & 0xFF
        else:
            n = self.cpu.registers[r] & 0xFF

        n &= 0xFF
        sub = A - n

        Z = 1 if sub & 0xFF == 0 else 0
        N = 1
        H = 1 if (A & 0xF) < (n & 0xF) else 0
        C = 1 if A < n else 0

        self.cpu.registers["A"] = sub & 0xFF
        self.cpu.set_flags(Z, N, H, C)
        self.cpu.timer.tick(ticks)
        return ticks
