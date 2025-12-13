class JP_NN:
    def __init__(self, cpu):
        self.cpu = cpu
        self.registers = self.cpu.registers
        self.mmu = self.cpu.mmu

    def jp_nn_instructions(self):
        instructions = {
            0xC3: lambda: self.execute_jp_nn("#", 12),
            0xE9: lambda: self.execute_jp_nn("HL", 8)
        }
        return instructions

    def execute_jp_nn(self, r, ticks):
        if r == "#":
            addrs = self.cpu.fetch_16bit()
        elif r == "HL":
            addrs = (self.registers["H"] << 8) | self.registers["L"]
        self.registers["pc"] = addrs
        self.cpu.timer.tick(ticks)
