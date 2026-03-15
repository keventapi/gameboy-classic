class INC_NN:
    def __init__(self, cpu):
        self.cpu = cpu
        

    def instructions_inc_nn(self):
        instructions = {
            0x03: (self.execute_inc_nn, ("BC", 8)),
            0x13: (self.execute_inc_nn, ("DE", 8)),
            0x23: (self.execute_inc_nn, ("HL", 8)),
            0x33: (self.execute_inc_nn, ("SP", 8)),
        }
        return instructions

    def execute_inc_nn(self, r16, ticks):
        if r16 == "SP":
            self.cpu.registers["sp"] = (self.cpu.registers["sp"] + 1) & 0xFFFF
        else:
            operand = (self.cpu.registers[r16[0]] << 8) | self.cpu.registers[r16[1]]
            operand = (operand + 1) & 0xFFFF
            self.cpu.registers[r16[0]] = (operand >> 8) & 0xFF
            self.cpu.registers[r16[1]] = operand & 0xFF
        self.cpu.timer.tick(ticks)
        return ticks
