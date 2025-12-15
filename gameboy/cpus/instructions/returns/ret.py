class RET:
    def __init__(self, cpu):
        self.cpu = cpu
        self.registers = self.cpu.registers
        self.mmu = self.cpu.mmu

    def ret_instructions(self):
        instructions = {
            0xC9: lambda: self.execute_ret(False, 16),
            0xD9: lambda: self.execute_ret(True, 16)
        }
        return instructions

    def execute_ret(self, enable_interrupt, ticks):
        low = self.cpu.pull8()
        high = self.cpu.pull8()
        new_pc = (high << 8) | low

        self.registers["pc"] = new_pc
        if enable_interrupt:
            self.cpu.ime = True
        self.cpu.timer.tick(ticks)
