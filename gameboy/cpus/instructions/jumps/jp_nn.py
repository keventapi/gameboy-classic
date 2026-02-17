class JP_NN:
    def __init__(self, cpu):
        self.cpu = cpu
        self.registers = self.cpu.registers
        self.mmu = self.cpu.mmu

    def jp_nn_instructions(self):
        instructions = {
            0xC3: (self.execute_jp_nn, ("#", 16)),
            0xE9: (self.execute_jp_nn, ("HL", 4))
        }
        return instructions

    def execute_jp_nn(self, r, ticks):
        last_state = self.registers.copy()
        if r == "#":
            addrs = self.cpu.fetch_16bit()
        elif r == "HL":
            addrs = (self.registers["H"] << 8) | self.registers["L"]
        self.registers["pc"] = addrs & 0xFFFF
        self.cpu.timer.tick(ticks)
        # self.cpu.debug(last_state, f"jp {r} non condictional")
        return ticks
