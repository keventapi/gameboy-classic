class LD_NN_N:
    def __init__(self):
        pass

    def ld_nn_n_instructions(self):
        instructions = {0x06: lambda: self.ld_n_nn("B"),
                        0x0E: lambda: self.ld_n_nn("C"),
                        0x16: lambda: self.ld_n_nn("D"),
                        0x1E: lambda: self.ld_n_nn("E"),
                        0x26: lambda: self.ld_n_nn("H"),
                        0x2E: lambda: self.ld_n_nn("L")}
        return instructions
        
    def ld_n_nn(self, register):
        nn = self.fetch()
        self.registers[register] = nn
        return None

