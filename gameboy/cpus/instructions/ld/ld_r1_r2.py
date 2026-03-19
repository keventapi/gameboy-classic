class LD_R1_R2:
    def __init__(self, cpu):
        self.cpu = cpu
        
        self.mmu = self.cpu.mmu

    def ld_r1_r2_instructions(self):
        instructions = {
         0x7F: (self.execute8b_ld_r1_r2, ("A", "A", 4)),
         0x78: (self.execute8b_ld_r1_r2, ("A", "B", 4)),
         0x79: (self.execute8b_ld_r1_r2, ("A", "C", 4)),
         0x7A: (self.execute8b_ld_r1_r2, ("A", "D", 4)),
         0x7B: (self.execute8b_ld_r1_r2, ("A", "E", 4)),
         0x7C: (self.execute8b_ld_r1_r2, ("A", "H", 4)),
         0x7D: (self.execute8b_ld_r1_r2, ("A", "L", 4)),
         0x7E: (self.execute8b_ld_r1_r2, ("A", "HL", 8)),

         0x40: (self.execute8b_ld_r1_r2, ("B", "B", 4)),
         0x41: (self.execute8b_ld_r1_r2, ("B", "C", 4)),
         0x42: (self.execute8b_ld_r1_r2, ("B", "D", 4)),
         0x43: (self.execute8b_ld_r1_r2, ("B", "E", 4)),
         0x44: (self.execute8b_ld_r1_r2, ("B", "H", 4)),
         0x45: (self.execute8b_ld_r1_r2, ("B", "L", 4)),
         0x46: (self.execute8b_ld_r1_r2, ("B", "HL", 8)),
         0x47: (self.execute8b_ld_r1_r2, ("B", "A", 4)),

         0x48: (self.execute8b_ld_r1_r2, ("C", "B", 4)),
         0x49: (self.execute8b_ld_r1_r2, ("C", "C", 4)),
         0x4A: (self.execute8b_ld_r1_r2, ("C", "D", 4)),
         0x4B: (self.execute8b_ld_r1_r2, ("C", "E", 4)),
         0x4C: (self.execute8b_ld_r1_r2, ("C", "H", 4)),
         0x4D: (self.execute8b_ld_r1_r2, ("C", "L", 4)),
         0x4E: (self.execute8b_ld_r1_r2, ("C", "HL", 8)),
         0x4F: (self.execute8b_ld_r1_r2, ("C", "A", 4)),

         0x50: (self.execute8b_ld_r1_r2, ("D", "B", 4)),
         0x51: (self.execute8b_ld_r1_r2, ("D", "C", 4)),
         0x52: (self.execute8b_ld_r1_r2, ("D", "D", 4)),
         0x53: (self.execute8b_ld_r1_r2, ("D", "E", 4)),
         0x54: (self.execute8b_ld_r1_r2, ("D", "H", 4)),
         0x55: (self.execute8b_ld_r1_r2, ("D", "L", 4)),
         0x56: (self.execute8b_ld_r1_r2, ("D", "HL", 8)),
         0x57: (self.execute8b_ld_r1_r2, ("D", "A", 4)),

         0x58: (self.execute8b_ld_r1_r2, ("E", "B", 4)),
         0x59: (self.execute8b_ld_r1_r2, ("E", "C", 4)),
         0x5A: (self.execute8b_ld_r1_r2, ("E", "D", 4)),
         0x5B: (self.execute8b_ld_r1_r2, ("E", "E", 4)),
         0x5C: (self.execute8b_ld_r1_r2, ("E", "H", 4)),
         0x5D: (self.execute8b_ld_r1_r2, ("E", "L", 4)),
         0x5E: (self.execute8b_ld_r1_r2, ("E", "HL", 8)),
         0x5F: (self.execute8b_ld_r1_r2, ("E", "A", 4)),

         0x60: (self.execute8b_ld_r1_r2, ("H", "B", 4)),
         0x61: (self.execute8b_ld_r1_r2, ("H", "C", 4)),
         0x62: (self.execute8b_ld_r1_r2, ("H", "D", 4)),
         0x63: (self.execute8b_ld_r1_r2, ("H", "E", 4)),
         0x64: (self.execute8b_ld_r1_r2, ("H", "H", 4)),
         0x65: (self.execute8b_ld_r1_r2, ("H", "L", 4)),
         0x66: (self.execute8b_ld_r1_r2, ("H", "HL", 8)),
         0x67: (self.execute8b_ld_r1_r2, ("H", "A", 4)),

         0x68: (self.execute8b_ld_r1_r2, ("L", "B", 4)),
         0x69: (self.execute8b_ld_r1_r2, ("L", "C", 4)),
         0x6A: (self.execute8b_ld_r1_r2, ("L", "D", 4)),
         0x6B: (self.execute8b_ld_r1_r2, ("L", "E", 4)),
         0x6C: (self.execute8b_ld_r1_r2, ("L", "H", 4)),
         0x6D: (self.execute8b_ld_r1_r2, ("L", "L", 4)),
         0x6E: (self.execute8b_ld_r1_r2, ("L", "HL", 8)),
         0x6F: (self.execute8b_ld_r1_r2, ("L", "A", 4)),

         0x70: (self.execute8b_ld_r1_r2, ("HL", "B", 8)),
         0x71: (self.execute8b_ld_r1_r2, ("HL", "C", 8)),
         0x72: (self.execute8b_ld_r1_r2, ("HL", "D", 8)),
         0x73: (self.execute8b_ld_r1_r2, ("HL", "E", 8)),
         0x74: (self.execute8b_ld_r1_r2, ("HL", "H", 8)),
         0x75: (self.execute8b_ld_r1_r2, ("HL", "L", 8)),
         0x36: (self.execute8b_ld_r1_r2, ("HL", "N", 12)),
         0x77: (self.execute8b_ld_r1_r2, ("HL", "A", 8))
        }
        return instructions

    def execute8b_ld_r1_r2(self, r1, r2, ticks):
        if r2 == "HL":
            hl = (self.cpu.registers["H"] << 8) | self.cpu.registers["L"]
            self.cpu.registers[r1] = self.mmu.read(hl) & 0xFF
            self.cpu.timer.tick(4)
        elif r1 == "HL" and r2 != "N":
            hl = (self.cpu.registers["H"] << 8) | self.cpu.registers["L"]
            self.mmu.write(hl, self.cpu.registers[r2])
            self.cpu.timer.tick(4)
        elif r1 == "HL" and r2 == "N":
            hl = (self.cpu.registers["H"] << 8) | self.cpu.registers["L"]
            n = self.cpu.fetch()
            self.cpu.timer.tick(4)
            self.mmu.write(hl, n)
            self.cpu.timer.tick(4)
        else:
            self.cpu.registers[r1] = self.cpu.registers[r2] & 0xFF
        self.cpu.timer.tick(4)
        return ticks
