class CP_N:
    def __init__(self, cpu):
        self.cpu = cpu
        self.fetch = self.cpu.fetch
        self.registers = self.cpu.registers
        self.mmu = self.cpu.mmu

    def cp_n_instructions(self):
        instructions = {
            0xBF: (self.execute_cp_n, ("A", 4)),
            0xB8: (self.execute_cp_n, ("B", 4)),
            0xB9: (self.execute_cp_n, ("C", 4)),
            0xBA: (self.execute_cp_n, ("D", 4)),
            0xBB: (self.execute_cp_n, ("E", 4)),
            0xBC: (self.execute_cp_n, ("H", 4)),
            0xBD: (self.execute_cp_n, ("L", 4)),
            0xBE: (self.execute_cp_n, ("HL", 8)),
            0xFE: (self.execute_cp_n, ("#", 8))
        }
        return instructions

    def execute_cp_n(self, r, ticks):
        result = self.registers["A"]
        if len(r) > 1:
            addrs = (self.registers[r[0]] << 8) | self.registers[r[1]]
            operand = self.mmu.read(addrs & 0xFFFF)
            result -= operand
        elif r == "#":
            operand = self.fetch()
            result -= operand
        else:
            operand = self.registers[r]
            result -= operand

        Z = 1 if (result & 0xFF) == 0 else 0
        N = 1
        H = 1 if (self.registers["A"] & 0xF) < (operand & 0xF) else 0
        C = 1 if (self.registers["A"] & 0xFF) < (operand & 0xFF) else 0

        self.cpu.set_flags(Z, N, H, C)
        self.cpu.timer.tick(ticks)
        return ticks
