class XOR_N:
    def __init__(self, cpu):
        self.cpu = cpu
        self.fetch = self.cpu.fetch
        self.mmu = self.cpu.mmu
        

    def xor_n_instructions(self):
        instructions = {
            0xAF: (self.execute_xor_n, ("A", 4)),
            0xA8: (self.execute_xor_n, ("B", 4)),
            0xA9: (self.execute_xor_n, ("C", 4)),
            0xAA: (self.execute_xor_n, ("D", 4)),
            0xAB: (self.execute_xor_n, ("E", 4)),
            0xAC: (self.execute_xor_n, ("H", 4)),
            0xAD: (self.execute_xor_n, ("L", 4)),
            0xAE: (self.execute_xor_n, ("HL", 8)),
            0xEE: (self.execute_xor_n, ("#", 8))
        }
        return instructions

    def execute_xor_n(self, r, ticks):
        result = self.cpu.registers["A"]
        if len(r) > 1:
            addrs = (self.cpu.registers[r[0]] << 8) | self.cpu.registers[r[1]]
            result ^= self.mmu.read(addrs & 0xFFFF)
        elif r == "#":
            imediate = self.fetch()
            result ^= imediate
        else:
            result ^= self.cpu.registers[r]

        Z = 1 if (result & 0xFF) == 0 else 0

        self.cpu.set_flags(Z, 0, 0, 0)
        self.cpu.registers["A"] = result & 0xFF
        self.cpu.timer.tick(ticks)
        return ticks
