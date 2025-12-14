class RST_N:
    def __init__(self, cpu):
        self.cpu = cpu
        self.registers = self.cpu.registers
        self.mmu = self.cpu.mmu

    def rst_n_instructions(self):
        instructions = {
            0xC7: lambda: self.execute_rst_n(0x00, 16),
            0xCF: lambda: self.execute_rst_n(0x08, 16),
            0xD7: lambda: self.execute_rst_n(0x10, 16),
            0xDF: lambda: self.execute_rst_n(0x18, 16),
            0xE7: lambda: self.execute_rst_n(0x20, 16),
            0xEF: lambda: self.execute_rst_n(0x28, 16),
            0xF7: lambda: self.execute_rst_n(0x30, 16),
            0xFF: lambda: self.execute_rst_n(0x38, 16),
        }
        return instructions

    def execute_rst_n(self, n, ticks):
        pc = self.registers["pc"]

        high = (pc >> 8) & 0xFF
        low = pc & 0xFF

        self.cpu.push8(high)
        self.cpu.push8(low)

        self.registers["pc"] = n & 0xFFFF
        self.cpu.timer.tick(ticks)
