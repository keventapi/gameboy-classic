class JP_NN:
    def __init__(self, cpu):
        self.cpu = cpu
        
        self.mmu = self.cpu.mmu

    def jp_nn_instructions(self):
        instructions = {
            0xC3: (self.execute_jp_nn, ("#", 16)),
            0xE9: (self.execute_jp_nn, ("HL", 4))
        }
        return instructions

    def execute_jp_nn(self, r, ticks):
        if r == "#":
            addrs = self.cpu.fetch_16bit()
        elif r == "HL":
            addrs = (self.cpu.registers["H"] << 8) | self.cpu.registers["L"]
        self.cpu.registers["pc"] = addrs & 0xFFFF
        self.cpu.timer.tick(ticks)
        return ticks
