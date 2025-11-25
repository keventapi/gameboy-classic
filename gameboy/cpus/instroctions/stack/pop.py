class POP:
    def __init__(self, cpu):
        self.cpu = cpu
        self.pull8 = self.cpu.pull8
        self.registers = self.cpu.registers
        self.mmu = self.cpu.mmu

    def pop_instructions(self):
        instructions = {
            0xF1: lambda: self.execute_pop("AF"),
            0xC1: lambda: self.execute_pop("BC"),
            0xD1: lambda: self.execute_pop("DE"),
            0xE1: lambda: self.execute_pop("HL")
        }
        return instructions

    def execute_pop(self, r16):
        high = r16[0]
        low = r16[1]
        if low == "F":
            self.registers[low] = self.pull8() & 0xF0
        else:
            self.registers[low] = self.pull8()
        self.registers[high] = self.pull8()
