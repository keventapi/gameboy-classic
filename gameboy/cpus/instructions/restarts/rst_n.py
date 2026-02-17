class RST_N:
    def __init__(self, cpu):
        self.cpu = cpu
        self.registers = self.cpu.registers
        self.mmu = self.cpu.mmu

    def rst_n_instructions(self):
        instructions = {
            0xC7: (self.execute_rst_n, (0x00, 16)),
            0xCF: (self.execute_rst_n, (0x08, 16)),
            0xD7: (self.execute_rst_n, (0x10, 16)),
            0xDF: (self.execute_rst_n, (0x18, 16)),
            0xE7: (self.execute_rst_n, (0x20, 16)),
            0xEF: (self.execute_rst_n, (0x28, 16)),
            0xF7: (self.execute_rst_n, (0x30, 16)),
            0xFF: (self.execute_rst_n, (0x38, 16)),
        }
        return instructions

    def execute_rst_n(self, n, ticks):
        pc = self.registers["pc"]

        self.cpu.push16(pc)
        self.registers["pc"] = n & 0xFFFF
        self.cpu.timer.tick(ticks)
        return ticks
