class CALL_NN:
    def __init__(self, cpu):
        self.cpu = cpu
        self.registers = self.cpu.registers
        self.mmu = self.cpu.mmu

    def call_nn_instructions(self):
        instructions = {
            0xCD: lambda: self.execute_call_nn(24)
        }
        return instructions

    def execute_call_nn(self, ticks):
        addrs = self.cpu.fetch_16bit()
        pc = self.registers["pc"]

        high = (pc >> 8) & 0xFF
        low = pc & 0xFF

        self.cpu.push8(high)
        self.cpu.push8(low)

        self.registers["pc"] = addrs
        self.cpu.timer.tick(ticks)
        return ticks
