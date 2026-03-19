class CALL_CC_NN:
    def __init__(self, cpu):
        self.cpu = cpu
        self.mmu = self.cpu.mmu

    def call_cc_nn_instructions(self):
        instructions = {
            0xC4: (self.execute_call_cc_nn, ("NZ", 12)),
            0xCC: (self.execute_call_cc_nn, ("Z", 12)),
            0xD4: (self.execute_call_cc_nn, ("NC", 12)),
            0xDC: (self.execute_call_cc_nn, ("C", 12))
        }
        return instructions

    def execute_call_cc_nn(self, condiction, ticks):
        last_state = self.cpu.registers.copy()
        addrs = self.cpu.fetch_16bit()
        pc = self.cpu.registers["pc"]

        flags = self.cpu.registers["F"]
        if "Z" in condiction:
            value = (flags >> 7) & 1
        else:
            value = (flags >> 4) & 1

        condiction_met = value == 1 if "N" not in condiction else value == 0
        if condiction_met:
            self.cpu.push16(pc)
            self.cpu.registers["pc"] = addrs
            self.cpu.timer.tick(ticks*2)
            return ticks * 2

        self.cpu.timer.tick(ticks)
        return ticks
