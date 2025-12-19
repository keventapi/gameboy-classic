class XOR_N:
    def __init__(self, cpu):
        self.cpu = cpu
        self.fetch = self.cpu.fetch
        self.mmu = self.cpu.mmu
        self.registers = self.cpu.registers

    def xor_n_instructions(self):
        instructions = {
            0xAF: lambda: self.execute_xor_n("A", 4),
            0xA8: lambda: self.execute_xor_n("B", 4),
            0xA9: lambda: self.execute_xor_n("C", 4),
            0xAA: lambda: self.execute_xor_n("D", 4),
            0xAB: lambda: self.execute_xor_n("E", 4),
            0xAC: lambda: self.execute_xor_n("H", 4),
            0xAD: lambda: self.execute_xor_n("L", 4),
            0xAE: lambda: self.execute_xor_n("HL", 8),
            0xEE: lambda: self.execute_xor_n("#", 8)
        }
        return instructions

    def execute_xor_n(self, r, ticks):
        result = self.registers["A"]
        if len(r) > 1:
            addrs = (self.registers[r[0]] << 8) | self.registers[r[1]]
            result ^= self.mmu.read(addrs)
        elif r == "#":
            imediate = self.fetch()
            result ^= imediate
        else:
            result ^= self.registers[r]

        Z = 1 if (result & 0xFF) == 0 else 0

        self.cpu.set_flags(Z, 0, 0, 0)
        self.registers["A"] = result & 0xFF
        self.cpu.timer.tick(ticks)
        return ticks
