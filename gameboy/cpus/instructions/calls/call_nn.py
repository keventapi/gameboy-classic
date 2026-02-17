class CALL_NN:
    def __init__(self, cpu):
        self.cpu = cpu
        self.registers = self.cpu.registers
        self.mmu = self.cpu.mmu

    def call_nn_instructions(self):
        instructions = {
            0xCD: (self.execute_call_nn, (24))
        }
        return instructions

    def execute_call_nn(self, ticks):
        last_state = self.registers.copy()
        addrs = self.cpu.fetch_16bit()
        pc = self.registers["pc"]

        self.cpu.push16(pc)

        self.registers["pc"] = addrs
        self.cpu.timer.tick(ticks)
        # self.cpu.debug(last_state, f"CALL non condictional")
        return ticks
