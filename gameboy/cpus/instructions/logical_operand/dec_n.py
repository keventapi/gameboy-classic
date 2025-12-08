class DEC_N:
    def __init__(self, cpu):
        self.cpu = cpu
        self.mmu = self.cpu.mmu
        self.registers = self.cpu.registers

    def dec_n_instructions(self):
        instructions = {

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

        self.registers["F"] = (Z << 7) | (N << 6) | (H << 5) | (C << 4)
        self.registers["F"] &= 0xF0

        self.cpu.timer.tick(ticks)