class LD_A_N:
    def __init__(self, cpu):
        self.cpu = cpu
        self.fetch = self.cpu.fetch
        self.registers = self.cpu.registers
        self.mmu = self.cpu.mmu

    def ld_a_n_instructions(self):
        instruction = {
            0x0A: lambda: self.ld_a_n("A", "BC", 8),
            0x1A: lambda: self.ld_a_n("A", "DE", 8),
            0xFA: lambda: self.ld_a_n("A", "nn", 16),
            0x3E: lambda: self.ld_a_n("A", "#", 8),
            0x02: lambda: self.ld_n_a("BC", "A", 8),
            0x12: lambda: self.ld_n_a("DE", "A", 8),
            0x77: lambda: self.ld_n_a("HL", "A", 8),
            0xEA: lambda: self.ld_n_a("nn", "A", 16)
        }
        return instruction

    def ld_n_a(self, r1, r2, ticks):
        if r1 == "nn":
            immediate = self.fetch() | (self.fetch() << 8)
            self.mmu.write(immediate, self.registers[r2])
        else:
            high, low = r1[0], r1[1]
            immediate = (self.registers[high] << 8) | self.registers[low]
            self.mmu.write(immediate, self.registers[r2])
        self.cpu.timer.tick(ticks)

    def ld_a_n(self, r1, r2, ticks):
        if r2 == "nn":
            immediate = self.fetch() | (self.fetch() << 8)
            self.registers[r1] = self.mmu.read(immediate)
        elif r2 == "#":
            immediate = self.fetch()
            self.registers[r1] = immediate
        else:
            high, low = r2[0], r2[1]
            immediate = (self.registers[high] << 8) | self.registers[low]
            self.registers[r1] = self.mmu.read(immediate)
        self.cpu.timer.tick(ticks)
