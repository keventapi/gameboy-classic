class PUSH:
    def __init__(self, cpu):
        self.cpu = cpu
        self.push8 = self.cpu.push8
        self.registers = self.cpu.registers
        self.mmu = self.cpu.mmu

    def push_instructions(self):
        instructions = {
            0xF5: lambda: self.execute_push("AF"),
            0xC5: lambda: self.execute_push("BC"),
            0xD5: lambda: self.execute_push("DE"),
            0xE5: lambda: self.execute_push("HL")
        }
        return instructions

    def execute_push(self, r16):
        high = r16[0]
        low = r16[1]
        self.push8(self.registers[high])
        self.push8(self.registers[low])
