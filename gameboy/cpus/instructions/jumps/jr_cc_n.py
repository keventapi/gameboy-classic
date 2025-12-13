class JR_CC_N:
    def __init__(self, cpu):
        self.cpu = cpu
        self.registers = self.cpu.registers
        self.mmu = self.cpu.mmu

    def jr_cc_n_instructions(self):
        instructions = {
            0x20: lambda: self.execute_jr_cc_n("NZ", 8),
            0x28: lambda: self.execute_jr_cc_n("Z", 8),
            0x30: lambda: self.execute_jr_cc_n("NC", 8),
            0x38: lambda: self.execute_jr_cc_n("C", 8)
        }
        return instructions

    def execute_jr_cc_n(self, condiction, ticks):
        flag = self.registers["F"]
        addrs = self.cpu.fetch()
        if "Z" in condiction:
            value = (flag >> 7) & 1
        else:
            value = (flag >> 4) & 1

        condiction_met = value == 1 if "N" not in condiction else value == 0

        if condiction_met:
            n = addrs
            if n >= 0x80:
                n -= 0x100
            self.registers["pc"] += n
            self.cpu.timer.tick(ticks+4)
            return

        self.cpu.timer.tick(ticks)
