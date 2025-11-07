class LD_R1_R2:
    def __init__(self):
        pass

    def ld_r1_r2_instructions(self):
        instructions = {
         0x7F: lambda: self.execute8b_ld_r1_r2("A", "A"),
         0x78: lambda: self.execute8b_ld_r1_r2("A", "B"),
         0x79: lambda: self.execute8b_ld_r1_r2("A", "C"),
         0x7A: lambda: self.execute8b_ld_r1_r2("A", "D"),
         0x7B: lambda: self.execute8b_ld_r1_r2("A", "E"),
         0x7C: lambda: self.execute8b_ld_r1_r2("A", "H"),
         0x7D: lambda: self.execute8b_ld_r1_r2("A", "L"),
         0x7E: lambda: self.execute8b_ld_r1_r2("A", "HL"),
         0x40: lambda: self.execute8b_ld_r1_r2("B", "B"),
         0x41: lambda: self.execute8b_ld_r1_r2("B", "C"),
         0x42: lambda: self.execute8b_ld_r1_r2("B", "D"),
         0x43: lambda: self.execute8b_ld_r1_r2("B", "E"),
         0x44: lambda: self.execute8b_ld_r1_r2("B", "H"),
         0x45: lambda: self.execute8b_ld_r1_r2("B", "L"),
         0x46: lambda: self.execute8b_ld_r1_r2("B", "HL"),
         0x48: lambda: self.execute8b_ld_r1_r2("C", "B"),
         0x49: lambda: self.execute8b_ld_r1_r2("C", "C"),
         0x4A: lambda: self.execute8b_ld_r1_r2("C", "D"),
         0x4B: lambda: self.execute8b_ld_r1_r2("C", "E"),
         0x4C: lambda: self.execute8b_ld_r1_r2("C", "H"),
         0x4D: lambda: self.execute8b_ld_r1_r2("C", "L"),
         0x4E: lambda: self.execute8b_ld_r1_r2("C", "HL"),
         0x50: lambda: self.execute8b_ld_r1_r2("D", "B"),
         0x51: lambda: self.execute8b_ld_r1_r2("D", "C"),
         0x52: lambda: self.execute8b_ld_r1_r2("D", "D"),
         0x53: lambda: self.execute8b_ld_r1_r2("D", "E"),
         0x54: lambda: self.execute8b_ld_r1_r2("D", "H"),
         0x55: lambda: self.execute8b_ld_r1_r2("D", "L"),
         0x56: lambda: self.execute8b_ld_r1_r2("D", "HL"),
         0x58: lambda: self.execute8b_ld_r1_r2("E", "B"),
         0x59: lambda: self.execute8b_ld_r1_r2("E", "C"),
         0x5A: lambda: self.execute8b_ld_r1_r2("E", "D"),
         0x5B: lambda: self.execute8b_ld_r1_r2("E", "E"),
         0x5C: lambda: self.execute8b_ld_r1_r2("E", "H"),
         0x5D: lambda: self.execute8b_ld_r1_r2("E", "L"),
         0x5E: lambda: self.execute8b_ld_r1_r2("E", "HL"),
         0x60: lambda: self.execute8b_ld_r1_r2("H", "B"),
         0x61: lambda: self.execute8b_ld_r1_r2("H", "C"),
         0x62: lambda: self.execute8b_ld_r1_r2("H", "D"),
         0x63: lambda: self.execute8b_ld_r1_r2("H", "E"),
         0x64: lambda: self.execute8b_ld_r1_r2("H", "H"),
         0x65: lambda: self.execute8b_ld_r1_r2("H", "L"),
         0x66: lambda: self.execute8b_ld_r1_r2("H", "HL"),
         0x68: lambda: self.execute8b_ld_r1_r2("L", "B"),
         0x69: lambda: self.execute8b_ld_r1_r2("L", "C"),
         0x6A: lambda: self.execute8b_ld_r1_r2("L", "D"),
         0x6B: lambda: self.execute8b_ld_r1_r2("L", "E"),
         0x6C: lambda: self.execute8b_ld_r1_r2("L", "H"),
         0x6D: lambda: self.execute8b_ld_r1_r2("L", "L"),
         0x6E: lambda: self.execute8b_ld_r1_r2("L", "HL"),
         0x70: lambda: self.execute8b_ld_r1_r2("HL", "B"),
         0x71: lambda: self.execute8b_ld_r1_r2("HL", "C"),
         0x72: lambda: self.execute8b_ld_r1_r2("HL", "D"),
         0x73: lambda: self.execute8b_ld_r1_r2("HL", "E"),
         0x74: lambda: self.execute8b_ld_r1_r2("HL", "H"),
         0x75: lambda: self.execute8b_ld_r1_r2("HL", "L"),
         0x36: lambda: self.execute8b_ld_r1_r2("HL", "m")
        }
        return instructions
    
    def execute8b_ld_r1_r2(self, r1, r2):
        if r2 == "HL":
            hl = (self.registers["H"] << 8) | self.registers["L"]
            self.registers[r1] = self.mmu.read(hl) & 0xFF
        elif r1 == "HL":
            hl = (self.registers["H"] << 8) | self.registers["L"]
            self.mmu.write(hl, self.registers[r2])
        else:
            self.registers[r1] = self.registers[r2] & 0xFF
        return None

