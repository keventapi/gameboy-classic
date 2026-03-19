class ADD_HL_N:
    def __init__(self, cpu):
        self.cpu = cpu
        self.mmu = self.cpu.mmu

    def add_hl_n_instructions(self):
        instructions = {
            0x09: (self.execute_add_hl_n, ("BC", 8)),
            0x19: (self.execute_add_hl_n, ("DE", 8)),
            0x29: (self.execute_add_hl_n, ("HL", 8)),
            0x39: (self.execute_add_hl_n, ("SP", 8))
        }
        return instructions

    def execute_add_hl_n(self, r16, ticks):
        if r16 == "SP":
            operand = self.cpu.registers["sp"]
        else:
            operand = (self.cpu.registers[r16[0]] << 8) | self.cpu.registers[r16[1]]
        src = ((self.cpu.registers["H"] << 8) | self.cpu.registers["L"])
        value = (src + operand) & 0xFFFF

        Z = (self.cpu.registers["F"] >> 7) & 0x1
        N = 0
        H = 1 if (src & 0xFFF) + (operand & 0xFFF) > 0xFFF else 0
        C = 1 if (src & 0xFFFF) + (operand & 0xFFFF) > 0xFFFF else 0

        self.cpu.set_flags(Z, N, H, C)
        self.cpu.registers["H"] = (value >> 8) & 0xFF
        self.cpu.registers["L"] = value & 0xFF

        self.cpu.timer.tick(ticks)
        return ticks
