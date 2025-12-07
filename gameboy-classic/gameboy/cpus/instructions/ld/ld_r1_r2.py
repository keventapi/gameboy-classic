class LD_R1_R2:
    def __init__(self, cpu):
        self.cpu = cpu
        self.registers = self.cpu.registers
        self.mmu = self.cpu.mmu

    def ld_r1_r2_instructions(self):
        instructions = {
         0x7F: lambda: self.execute8b_ld_r1_r2("A", "A", 4),
         0x78: lambda: self.execute8b_ld_r1_r2("A", "B", 4),
         0x79: lambda: self.execute8b_ld_r1_r2("A", "C", 4),
         0x7A: lambda: self.execute8b_ld_r1_r2("A", "D", 4),
         0x7B: lambda: self.execute8b_ld_r1_r2("A", "E", 4),
         0x7C: lambda: self.execute8b_ld_r1_r2("A", "H", 4),
         0x7D: lambda: self.execute8b_ld_r1_r2("A", "L", 4),
         0x7E: lambda: self.execute8b_ld_r1_r2("A", "HL", 8),
         0x40: lambda: self.execute8b_ld_r1_r2("B", "B", 4),
         0x41: lambda: self.execute8b_ld_r1_r2("B", "C", 4),
         0x42: lambda: self.execute8b_ld_r1_r2("B", "D", 4),
         0x43: lambda: self.execute8b_ld_r1_r2("B", "E", 4),
         0x44: lambda: self.execute8b_ld_r1_r2("B", "H", 4),
         0x45: lambda: self.execute8b_ld_r1_r2("B", "L", 4),
         0x46: lambda: self.execute8b_ld_r1_r2("B", "HL", 8),
         0x48: lambda: self.execute8b_ld_r1_r2("C", "B", 4),
         0x49: lambda: self.execute8b_ld_r1_r2("C", "C", 4),
         0x4A: lambda: self.execute8b_ld_r1_r2("C", "D", 4),
         0x4B: lambda: self.execute8b_ld_r1_r2("C", "E", 4),
         0x4C: lambda: self.execute8b_ld_r1_r2("C", "H", 4),
         0x4D: lambda: self.execute8b_ld_r1_r2("C", "L", 4),
         0x4E: lambda: self.execute8b_ld_r1_r2("C", "HL", 8),
         0x50: lambda: self.execute8b_ld_r1_r2("D", "B", 4),
         0x51: lambda: self.execute8b_ld_r1_r2("D", "C", 4),
         0x52: lambda: self.execute8b_ld_r1_r2("D", "D", 4),
         0x53: lambda: self.execute8b_ld_r1_r2("D", "E", 4),
         0x54: lambda: self.execute8b_ld_r1_r2("D", "H", 4),
         0x55: lambda: self.execute8b_ld_r1_r2("D", "L", 4),
         0x56: lambda: self.execute8b_ld_r1_r2("D", "HL", 8),
         0x58: lambda: self.execute8b_ld_r1_r2("E", "B", 4),
         0x59: lambda: self.execute8b_ld_r1_r2("E", "C", 4),
         0x5A: lambda: self.execute8b_ld_r1_r2("E", "D", 4),
         0x5B: lambda: self.execute8b_ld_r1_r2("E", "E", 4),
         0x5C: lambda: self.execute8b_ld_r1_r2("E", "H", 4),
         0x5D: lambda: self.execute8b_ld_r1_r2("E", "L", 4),
         0x5E: lambda: self.execute8b_ld_r1_r2("E", "HL", 8),
         0x60: lambda: self.execute8b_ld_r1_r2("H", "B", 4),
         0x61: lambda: self.execute8b_ld_r1_r2("H", "C", 4),
         0x62: lambda: self.execute8b_ld_r1_r2("H", "D", 4),
         0x63: lambda: self.execute8b_ld_r1_r2("H", "E", 4),
         0x64: lambda: self.execute8b_ld_r1_r2("H", "H", 4),
         0x65: lambda: self.execute8b_ld_r1_r2("H", "L", 4),
         0x66: lambda: self.execute8b_ld_r1_r2("H", "HL", 8),
         0x68: lambda: self.execute8b_ld_r1_r2("L", "B", 4),
         0x69: lambda: self.execute8b_ld_r1_r2("L", "C", 4),
         0x6A: lambda: self.execute8b_ld_r1_r2("L", "D", 4),
         0x6B: lambda: self.execute8b_ld_r1_r2("L", "E", 4),
         0x6C: lambda: self.execute8b_ld_r1_r2("L", "H", 4),
         0x6D: lambda: self.execute8b_ld_r1_r2("L", "L", 4),
         0x6E: lambda: self.execute8b_ld_r1_r2("L", "HL", 8),
         0x70: lambda: self.execute8b_ld_r1_r2("HL", "B", 8),
         0x71: lambda: self.execute8b_ld_r1_r2("HL", "C", 8),
         0x72: lambda: self.execute8b_ld_r1_r2("HL", "D", 8),
         0x73: lambda: self.execute8b_ld_r1_r2("HL", "E", 8),
         0x74: lambda: self.execute8b_ld_r1_r2("HL", "H", 8),
         0x75: lambda: self.execute8b_ld_r1_r2("HL", "L", 8),
         0x36: lambda: self.execute8b_ld_r1_r2("HL", "N", 12)
        }
        return instructions

    def execute8b_ld_r1_r2(self, r1, r2, ticks):
        if r2 == "HL":
            hl = (self.registers["H"] << 8) | self.registers["L"]
            self.registers[r1] = self.mmu.read(hl) & 0xFF
        elif r1 == "HL" and r2 != "N":
            hl = (self.registers["H"] << 8) | self.registers["L"]
            self.mmu.write(hl, self.registers[r2])
        elif r1 == "HL" and r2 == "N":
            hl = (self.registers["H"] << 8) | self.registers["L"]
            n = self.cpu.fetch()
            self.mmu.write(hl, n)
        else:
            self.registers[r1] = self.registers[r2] & 0xFF
        self.cpu.timer.tick(ticks)
