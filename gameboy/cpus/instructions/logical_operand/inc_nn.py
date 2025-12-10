class INC_NN:
    def __init__(self, cpu):
        self.cpu = cpu
        self.registers = self.cpu.registers

    def instructions_inc_nn(self):
        instructions = {
            0x03: lambda: self.execute_inc_nn("BC", 8),
            0x13: lambda: self.execute_inc_nn("DE", 8),
            0x23: lambda: self.execute_inc_nn("HL", 8),
            0x33: lambda: self.execute_inc_nn("SP", 8),
        }
        return instructions

    def execute_inc_nn(self, r16, ticks):
        if r16 == "SP":
            self.registers["SP"] = (self.registers["SP"] + 1) & 0xFFFF
        else:
            operand = (self.registers[r16[0]] << 8) | self.registers[r16[1]]
            operand += 1
            self.registers[r16[0]] = (operand >> 8) & 0xFF
            self.registers[r16[1]] = operand & 0xFF
        self.cpu.timer.tick(ticks)
