class DEC_N:
    def __init__(self, cpu):
        self.cpu = cpu
        self.mmu = self.cpu.mmu
        

    def dec_n_instructions(self):
        instructions = {
            0x3D: (self.execute_dec_n, ("A", 4)),
            0x05: (self.execute_dec_n, ("B", 4)),
            0x0D: (self.execute_dec_n, ("C", 4)),
            0x15: (self.execute_dec_n, ("D", 4)),
            0x1D: (self.execute_dec_n, ("E", 4)),
            0x25: (self.execute_dec_n, ("H", 4)),
            0x2D: (self.execute_dec_n, ("L", 4)),
            0x35: (self.execute_dec_n, ("HL", 12))
        }
        return instructions

    def execute_dec_n(self, r, ticks):
        if len(r) > 1:
            addrs = self.cpu.registers[r[0]] << 8 | self.cpu.registers[r[1]]
            value = self.mmu.read(addrs & 0xFFFF)
            self.cpu.timer.tick(4)
            self.mmu.write(addrs & 0xFFFF, (value-1) & 0xFF)
            self.cpu.timer.tick(4)
        else:
            value = self.cpu.registers[r]
            self.cpu.registers[r] = (self.cpu.registers[r] - 1) & 0xFF

        Z = 1 if ((value - 1) & 0xFF) == 0 else 0
        N = 1
        H = 1 if ((value & 0xF) < (1 & 0xF)) else 0
        C = (self.cpu.registers["F"] >> 4) & 1

        self.cpu.set_flags(Z, N, H, C)
        self.cpu.timer.tick(4)
        return ticks
