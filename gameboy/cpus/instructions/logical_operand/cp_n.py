class CP_N:
    def __init__(self, cpu):
        self.cpu = cpu
        self.fetch = self.cpu.fetch
        self.registers = self.cpu.registers
        self.mmu = self.cpu.mmu

    def cp_n_instructions(self):
        instructions = {
            0xBF: lambda: self.execute_cp_n("A", 4),
            0xB8: lambda: self.execute_cp_n("B", 4),
            0xB9: lambda: self.execute_cp_n("C", 4),
            0xBA: lambda: self.execute_cp_n("D", 4),
            0xBB: lambda: self.execute_cp_n("E", 4),
            0xBC: lambda: self.execute_cp_n("H", 4),
            0xBD: lambda: self.execute_cp_n("L", 4),
            0xBE: lambda: self.execute_cp_n("HL", 8),
            0xFE: lambda: self.execute_cp_n("#", 8)
        }
        return instructions

    def execute_cp_n(self, r, ticks):
        result = self.registers["A"]
        if len(r) > 1:
            addrs = (self.registers[r[0]] << 8) | self.registers[r[1]]
            operand = self.mmu.read(addrs)
            result -= operand
        elif r == "#":
            operand = self.fetch()
            result -= operand
        else:
            operand = self.registers[r]
            result -= operand

        self.registers["F"] = 0x00

        # Z
        if (result & 0xFF) == 0:
            self.registers["F"] |= 0b10000000

        # N
        self.registers["F"] |= 0b01000000

        # H
        if (self.registers["A"] & 0xF) < (operand & 0xF):
            self.registers["F"] |= 0b00100000

        # C
        if (self.registers["A"] & 0xFF) < (operand & 0xFF):
            self.registers["F"] |= 0b00010000

        self.registers["F"] &= 0xF0
        self.cpu.timer.tick(ticks)
