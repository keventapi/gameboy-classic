class JP_CC_NN:
    def __init__(self, cpu):
        self.cpu = cpu
        self.registers = self.cpu.registers
        self.mmu = self.cpu.mmu

    def jp_cc_nn_instructions(self):
        instructions = {
            0xC2: (self.execute_jp_cc_nn, ("NZ", 12)),
            0xCA: (self.execute_jp_cc_nn, ("Z", 12)),
            0xD2: (self.execute_jp_cc_nn, ("NC", 12)),
            0xDA: (self.execute_jp_cc_nn, ("C", 12))
        }
        return instructions

    def execute_jp_cc_nn(self, condiction, ticks):
        addrs = self.cpu.fetch_16bit()
        flags = self.registers["F"]
        if "Z" in condiction:
            value = (flags >> 7) & 1
        elif "C" in condiction:
            value = (flags >> 4) & 1

        condiction_met = value == 1 if "N" not in condiction else value == 0
        if condiction_met:
            self.registers["pc"] = addrs
            self.cpu.timer.tick(ticks+4)
            return ticks + 4

        self.cpu.timer.tick(ticks)
        return ticks
