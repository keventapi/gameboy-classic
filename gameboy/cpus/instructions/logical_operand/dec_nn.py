class DEC_NN:
    def __init__(self, cpu):
        self.cpu = cpu
        self.registers = self.cpu.registers

    def instructions_dec_nn(self):
        instructions = {
            0x0B: lambda: self.execute_dec_nn("BC", 8),
            0x1B: lambda: self.execute_dec_nn("DE", 8),
            0x2B: lambda: self.execute_dec_nn("HL", 8),
            0x3B: lambda: self.execute_dec_nn("SP", 8)
        }
        return instructions

    def execute_dec_nn(self, r16, ticks):
        if r16 == "SP":
            self.registers[r16] = (self.registers[r16] - 1) & 0xFFFF
        else:
            operand = (self.registers[r16[0]] << 8) | self.registers[r16[1]]
            operand = (operand - 1) & 0xFFFF
            self.registers[r16[0]] = (operand >> 8) & 0xFF
            self.registers[r16[1]] = operand & 0xFF
        self.cpu.timer.tick(ticks)
        return ticks
