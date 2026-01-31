class ADD_A_N:
    def __init__(self, cpu):
        self.cpu = cpu
        self.pull8 = self.cpu.pull8
        self.fetch = self.cpu.fetch
        self.registers = self.cpu.registers
        self.mmu = self.cpu.mmu

    def add_a_n_instructions(self):
        instructions = {
            0x87: (self.execute_add_a_n, ("A", 4)),
            0x80: (self.execute_add_a_n, ("B", 4)),
            0x81: (self.execute_add_a_n, ("C", 4)),
            0x82: (self.execute_add_a_n, ("D", 4)),
            0x83: (self.execute_add_a_n, ("E", 4)),
            0x84: (self.execute_add_a_n, ("H", 4)),
            0x85: (self.execute_add_a_n, ("L", 4)),
            0x86: (self.execute_add_a_n, ("HL", 8)),
            0xC6: (self.execute_add_a_n, ("#", 8))
        }
        return instructions

    def execute_add_a_n(self, r, ticks):
        if len(r) > 1 or r == "#":
            if r == "#":
                n = self.fetch()
            else:
                addrs = (self.registers[r[0]] << 8) | self.registers[r[1]]
                n = self.mmu.read(addrs)
        else:
            n = self.registers[r]

        sum = n + self.registers["A"]

        Z = 1 if sum & 0xFF == 0 else 0
        N = 0
        H = 1 if ((self.registers["A"] & 0xF) + (n & 0xF)) > 0xF else 0
        C = 1 if sum > 0xFF else 0

        self.registers["A"] = sum & 0xFF
        self.cpu.set_flags(Z, N, H, C)
        self.cpu.timer.tick(ticks)
        return ticks
