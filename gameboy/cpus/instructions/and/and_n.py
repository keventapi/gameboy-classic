class AND_N:
    def __init__(self, cpu):
        self.cpu = cpu
        self.registers = self.cpu.registers
        self.mmu = self.cpu.mmu
        self.fetch = self.cpu.fetch

    def and_n_instructions(self):
        instructions = {
            0xA7: lambda: self.execute_and_n("A", 4),
            0xA0: lambda: self.execute_and_n("B", 4),
            0xA1: lambda: self.execute_and_n("C", 4),
            0xA2: lambda: self.execute_and_n("D", 4),
            0xA3: lambda: self.execute_and_n("E", 4),
            0xA4: lambda: self.execute_and_n("H", 4),
            0xA5: lambda: self.execute_and_n("L", 4),
            0xA6: lambda: self.execute_and_n("HL", 8),
            0xE6: lambda: self.execute_and_n("#", 8),
        }
        return instructions

    def execute_and_n(self, r, ticks):
        result = self.registers["A"]
        if len(r) > 1:
            addrs = (self.registers[r[0]] << 8) | self.registers[r[1]]
            result &= self.mmu.read(addrs)
        elif r == "#":
            imediate = self.cpu.fetch()
            result &= imediate
        else:
            result &= self.registers[r]

        # reset flags
        self.registers["F"] = 0x00

        # Z
        if (result & 0xFF) == 0:
            self.registers["F"] |= 0b10000000

        # H
        self.registers["F"] |= 0b00100000

        self.registers["F"] &= 0xF0
        self.registers["A"] = result & 0xFF
        self.cpu.timer.tick(ticks)
