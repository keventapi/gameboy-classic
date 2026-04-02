class RET:
    def __init__(self, cpu):
        self.cpu = cpu
        
        self.mmu = self.cpu.mmu

    def ret_instructions(self):
        instructions = {
            0xC9: (self.execute_ret, (False, 16)),
            0xD9: (self.execute_ret, (True, 16))
        }
        return instructions

    def execute_ret(self, enable_interrupt, ticks):
        new_pc = self.cpu.pull16()

        self.cpu.registers["pc"] = new_pc & 0xFFFF
        if enable_interrupt:
            self.cpu.ime = True
        self.cpu.timer.tick(ticks)
        return ticks
