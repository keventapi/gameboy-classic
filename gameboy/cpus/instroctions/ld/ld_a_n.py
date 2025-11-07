class LD_A_N:
    def __init__(self):
        pass

    def ld_a_n_instructions(self):
        instruction = {
            0x0A: lambda: self.ld_a_n("A", "BC"),
            0x1A: lambda: self.ld_a_n("A", "DE"),
            0x7E: lambda: self.ld_a_n("A", "HL"),
            0xFA: lambda: self.ld_a_n("A", "nn"),
            0x3E: lambda: self.ld_a_n("A", "#")
        }
        return instruction
    
    def ld_a_n(self, r1, r2):
        if r2 == "nn":
            immediate = self.fetch() | (self.fetch() << 8)
            self.registers[r1] = self.mmu.read(immediate)
            return
        elif r2 == "#":
            immediate = self.fetch()
            self.registers[r1] = immediate
            return
        else:
            high, low = r2[0], r2[1]
            immediate = (self.registers[high] << 8) | self.registers[low]
            self.registers[r1] = self.mmu.read(immediate)
            return
        