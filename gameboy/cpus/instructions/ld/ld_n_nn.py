class LD_N_NN:
    def __init__(self, cpu):
        self.cpu = cpu
        self.fetch = self.cpu.fetch
        self.registers = self.cpu.registers
        self.mmu = self.cpu.mmu

    def ld_n_nn_instructions(self):
        instructions = {
            0x01: lambda: self.execute_ld_n_nn("BC", 12),
            0x11: lambda: self.execute_ld_n_nn("DE", 12),
            0x21: lambda: self.execute_ld_n_nn("HL", 12),
            0X31: lambda: self.execute_ld_n_nn("SP", 12)
        }
        return instructions

    def execute_ld_n_nn(self, r16, ticks):
        low = self.fetch()
        high = self.fetch()
        nn = (high << 8) | low
        if r16 == "SP":
            self.registers[r16] = nn
        else:
            self.registers[r16[0]] = high
            self.registers[r16[1]] = low
        self.cpu.timer.tick(ticks)
