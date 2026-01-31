class LD_NN_N:
    def __init__(self, cpu):
        self.cpu = cpu
        self.fetch = self.cpu.fetch
        self.registers = self.cpu.registers
        self.mmu = self.cpu.mmu

    def ld_nn_n_instructions(self):
        instructions = {
            0x06: (self.ld_n_nn, ("B", 8)),
            0x0E: (self.ld_n_nn, ("C", 8)),
            0x16: (self.ld_n_nn, ("D", 8)),
            0x1E: (self.ld_n_nn, ("E", 8)),
            0x26: (self.ld_n_nn, ("H", 8)),
            0x2E: (self.ld_n_nn, ("L", 8))
        }
        return instructions

    def ld_n_nn(self, register, ticks):
        nn = self.fetch()
        self.registers[register] = nn
        self.cpu.timer.tick(ticks)
        return ticks
