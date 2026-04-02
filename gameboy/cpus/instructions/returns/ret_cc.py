class RET_CC:
    def __init__(self, cpu):
        self.cpu = cpu
        
        self.mmu = self.cpu.mmu

    def ret_cc_instructions(self):
        instructions = {
            0xC0: (self.execute_ret_cc, ("NZ", 8)),
            0xC8: (self.execute_ret_cc, ("Z", 8)),
            0xD0: (self.execute_ret_cc, ("NC", 8)),
            0xD8: (self.execute_ret_cc, ("C", 8))
        }
        return instructions

    def execute_ret_cc(self, condiction, ticks):
        flag = self.cpu.registers["F"]
        if "Z" in condiction:
            value = (flag >> 7) & 1
        else:
            value = (flag >> 4) & 1

        condiction_met = value == 1 if "N" not in condiction else value == 0
        if condiction_met:
            new_pc = self.cpu.pull16()
            self.cpu.registers["pc"] = new_pc & 0xFFFF
            self.cpu.timer.tick(ticks+12)
            return ticks + 12
        self.cpu.timer.tick(ticks)
        return ticks
