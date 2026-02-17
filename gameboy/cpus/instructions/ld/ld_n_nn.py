class LD_N_NN:
    def __init__(self, cpu):
        self.cpu = cpu
        self.fetch = self.cpu.fetch
        self.registers = self.cpu.registers
        self.mmu = self.cpu.mmu

    def ld_n_nn_instructions(self):
        instructions = {
            0x01: (self.execute_ld_n_nn, ("BC", 12)),
            0x11: (self.execute_ld_n_nn, ("DE", 12)),
            0x21: (self.execute_ld_n_nn, ("HL", 12)),
            0X31: (self.execute_ld_n_nn, ("SP", 12))
        }
        return instructions

    def execute_ld_n_nn(self, r16, ticks):
        nn = self.cpu.fetch_16bit()
        if r16 == "SP":
            self.registers["sp"] = nn & 0xFFFF
        else:
            self.registers[r16[0]] = (nn >> 8) & 0xFF
            self.registers[r16[1]] = nn & 0xFF
        self.cpu.timer.tick(ticks)
        return ticks
