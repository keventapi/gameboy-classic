class PUSH:
    def __init__(self, cpu):
        self.cpu = cpu
        self.push8 = self.cpu.push8
        self.registers = self.cpu.registers
        self.mmu = self.cpu.mmu

    def push_instructions(self):
        instructions = {
            0xF5: lambda: self.execute_push("AF", 16),
            0xC5: lambda: self.execute_push("BC", 16),
            0xD5: lambda: self.execute_push("DE", 16),
            0xE5: lambda: self.execute_push("HL", 16)
        }
        return instructions

    def execute_push(self, r16, ticks):
        high = r16[0]
        low = r16[1]
        self.push8(self.registers[high])
        self.push8(self.registers[low])
        self.cpu.timer.tick(ticks)
        return ticks
