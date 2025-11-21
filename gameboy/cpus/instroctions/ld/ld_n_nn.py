class LD_N_NN:
    def __init__(self) -> None:
        pass

    def ld_n_nn_instructions(self):
        instructions = {
            0x01: lambda: self.execute_ld_n_nn("BC"),
            0x11: lambda: self.execute_ld_n_nn("DE"),
            0x21: lambda: self.execute_ld_n_nn("HL"),
            0X31: lambda: self.execute_ld_n_nn("SP")
        }
        return instructions
    
    def execute_ld_n_nn(self, r16):
        low = self.fetch()
        high = self.fetch()
        nn = (high << 8) | low
        if r16 == "SP":
            self.registers[r16] = nn
        else:
            self.registers[r16[0]] = high
            self.registers[r16[1]] = low
