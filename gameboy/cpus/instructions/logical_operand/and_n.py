class AND_N:
    def __init__(self, cpu):
        self.cpu = cpu
        self.registers = self.cpu.registers
        self.mmu = self.cpu.mmu
        self.fetch = self.cpu.fetch

    def and_n_instructions(self):
        instructions = {
            0xA7: (self.execute_and_n, ("A", 4)),
            0xA0: (self.execute_and_n, ("B", 4)),
            0xA1: (self.execute_and_n, ("C", 4)),
            0xA2: (self.execute_and_n, ("D", 4)),
            0xA3: (self.execute_and_n, ("E", 4)),
            0xA4: (self.execute_and_n, ("H", 4)),
            0xA5: (self.execute_and_n, ("L", 4)),
            0xA6: (self.execute_and_n, ("HL", 8)),
            0xE6: (self.execute_and_n, ("#", 8)),
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

        Z = 1 if (result & 0xFF) == 0 else 0
        H = 1

        self.cpu.set_flags(Z, 0, H, 0)
        self.registers["A"] = result & 0xFF
        self.cpu.timer.tick(ticks)
        return ticks
