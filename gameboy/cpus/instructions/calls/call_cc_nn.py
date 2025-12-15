class CALL_CC_NN:
    def __init__(self, cpu):
        self.cpu = cpu
        self.registers = self.cpu.registers
        self.mmu = self.cpu.mmu

    def call_cc_nn_instructions(self):
        instructions = {
            0xC4: lambda: self.execute_call_cc_nn("NZ", 12),
            0xCC: lambda: self.execute_call_cc_nn("Z", 12),
            0xD4: lambda: self.execute_call_cc_nn("NC", 12),
            0xDC: lambda: self.execute_call_cc_nn("C", 12)
        }
        return instructions

    def execute_call_cc_nn(self, condiction, ticks):
        addrs = self.cpu.fetch_16bit()
        pc = self.registers["pc"]

        high = (pc >> 8) & 0xFF
        low = pc & 0xFF

        flags = self.registers["F"]
        if "Z" in condiction:
            value = (flags >> 7) & 1
        else:
            value = (flags >> 4) & 1

        condiction_met = (value == 1) if "N" not in condiction else value == 0
        if condiction_met:
            self.cpu.push8(high)
            self.cpu.push8(low)

            self.registers["pc"] = addrs
            self.cpu.timer.tick(ticks*2)
            return
        self.cpu.timer.tick(ticks)
