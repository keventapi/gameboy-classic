class RET_CC:
    def __init__(self, cpu):
        self.cpu = cpu
        self.registers = self.cpu.registers
        self.mmu = self.cpu.mmu

    def ret_cc_instructions(self):
        instructions = {
            0xC0: lambda: self.execute_ret_cc("NZ", 8),
            0xC8: lambda: self.execute_ret_cc("Z", 8),
            0xD0: lambda: self.execute_ret_cc("NC", 8),
            0xD8: lambda: self.execute_ret_cc("C", 8)
        }
        return instructions

    def execute_ret_cc(self, condiction, ticks):
        flag = self.registers["F"]
        if "Z" in condiction:
            value = (flag >> 7) & 1
        else:
            value = (flag >> 4) & 1

        condiction_met = value == 1 if "N" not in condiction else value == 0
        if condiction_met:
            low = self.cpu.pull8()
            high = self.cpu.pull8()
            new_pc = (high << 8) | low
            self.registers["pc"] = new_pc
            self.cpu.timer.tick(ticks+12)
            return
        self.cpu.timer.tick(ticks)
