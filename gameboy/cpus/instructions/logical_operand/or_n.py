class OR_N:
    def __init__(self, cpu):
        self.cpu = cpu
        self.registers = cpu.registers
        self.fetch = self.cpu.fetch
        self.mmu = self.cpu.mmu

    def or_n_instructions(self):
        instructions = {
            0xB7: lambda: self.execute_or_n("A", 4),
            0xB0: lambda: self.execute_or_n("B", 4),
            0xB1: lambda: self.execute_or_n("C", 4),
            0xB2: lambda: self.execute_or_n("D", 4),
            0xB3: lambda: self.execute_or_n("E", 4),
            0xB4: lambda: self.execute_or_n("H", 4),
            0xB5: lambda: self.execute_or_n("L", 4),
            0xB6: lambda: self.execute_or_n("HL", 8),
            0xF6: lambda: self.execute_or_n("#", 8)
        }
        return instructions

    def execute_or_n(self, r, ticks):
        result = self.registers["A"]
        if len(r) > 1:
            addrs = (self.registers[r[0]] << 8) | self.registers[r[1]]
            result |= self.mmu.read(addrs)
        elif r == "#":
            imediate = self.fetch()
            result |= imediate
        else:
            result |= self.registers[r]

        self.registers["F"] = 0x00

        if (result & 0xFF) == 0:
            self.registers["F"] |= 0b10000000

        self.registers["A"] = result & 0xFF
        self.registers["F"] &= 0xF0
        self.cpu.timer.tick(ticks)
