class INC_N:
    def __init__(self, cpu):
        self.cpu = cpu
        self.registers = self.cpu.registers
        self.mmu = self.cpu.mmu

    def inc_n_instructions(self):
        instructions = {
            0x3C: (self.execute_inc_n, ("A", 4)),
            0x04: (self.execute_inc_n, ("B", 4)),
            0x0C: (self.execute_inc_n, ("C", 4)),
            0x14: (self.execute_inc_n, ("D", 4)),
            0x1C: (self.execute_inc_n, ("E", 4)),
            0x24: (self.execute_inc_n, ("H", 4)),
            0x2C: (self.execute_inc_n, ("L", 4)),
            0x34: (self.execute_inc_n, ("HL", 12))
        }
        return instructions

    def execute_inc_n(self, r, ticks):
        if len(r) > 1:
            addrs = self.registers[r[0]] << 8 | self.registers[r[1]]
            value = self.mmu.read(addrs & 0xFFFF)
            self.mmu.write(addrs, value+1 & 0xFF)
        else:
            value = self.registers[r]
            self.registers[r] = (self.registers[r] + 1) & 0xFF

        Z = 1 if ((value + 1) & 0xFF) == 0 else 0
        N = 0
        H = 1 if (value & 0xF) + (1 & 0xF) > 0xF else 0
        C = (self.registers["F"] >> 4) & 1

        self.cpu.set_flags(Z, N, H, C)
        self.cpu.timer.tick(ticks)
        return ticks
