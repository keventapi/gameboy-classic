class DEC_N:
    def __init__(self, cpu):
        self.cpu = cpu
        self.mmu = self.cpu.mmu
        self.registers = self.cpu.registers

    def dec_n_instructions(self):
        instructions = {
            0x3D: lambda: self.execute_dec_n("A", 4),
            0x05: lambda: self.execute_dec_n("B", 4),
            0x0D: lambda: self.execute_dec_n("C", 4),
            0x15: lambda: self.execute_dec_n("D", 4),
            0x1D: lambda: self.execute_dec_n("E", 4),
            0x25: lambda: self.execute_dec_n("H", 4),
            0x2D: lambda: self.execute_dec_n("L", 4),
            0x35: lambda: self.execute_dec_n("HL", 12)
        }
        return instructions

    def execute_dec_n(self, r, ticks):
        if len(r) > 1:
            addrs = self.registers[r[0]] << 8 | self.registers[r[1]]
            value = self.mmu.read(addrs)
            self.mmu.write(addrs, (value-1) & 0xFF)
        else:
            value = self.registers[r]
            self.registers[r] = (self.registers[r] - 1) & 0xFF

        Z = 1 if ((value - 1) & 0xFF) == 0 else 0
        N = 1
        H = 1 if ((value & 0xF) < (1 & 0xF)) else 0
        C = (self.registers["F"] >> 4) & 1

        self.cpu.set_flags(Z, N, H, C)
        self.cpu.timer.tick(ticks)
