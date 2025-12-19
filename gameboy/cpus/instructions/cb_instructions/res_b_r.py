class RES_B_R:
    def __init__(self, cpu):
        self.cpu = cpu
        self.registers = self.cpu.registers
        self.mmu = self.cpu.mmu

    def res_b_r_intructions(self):
        instructions = {
            0x87: lambda: self.execute_res_b_r(0, "A", 8),
            0x80: lambda: self.execute_res_b_r(0, "B", 8),
            0x81: lambda: self.execute_res_b_r(0, "C", 8),
            0x82: lambda: self.execute_res_b_r(0, "D", 8),
            0x83: lambda: self.execute_res_b_r(0, "E", 8),
            0x84: lambda: self.execute_res_b_r(0, "H", 8),
            0x85: lambda: self.execute_res_b_r(0, "L", 8),
            0x86: lambda: self.execute_res_b_r(0, "HL", 16),
            0x88: lambda: self.execute_res_b_r(1, "B", 8),
            0x89: lambda: self.execute_res_b_r(1, "C", 8),
            0x8A: lambda: self.execute_res_b_r(1, "D", 8),
            0x8B: lambda: self.execute_res_b_r(1, "E", 8),
            0x8C: lambda: self.execute_res_b_r(1, "H", 8),
            0x8D: lambda: self.execute_res_b_r(1, "L", 8),
            0x8E: lambda: self.execute_res_b_r(1, "HL", 16),
            0x8F: lambda: self.execute_res_b_r(1, "A", 8),
            0x90: lambda: self.execute_res_b_r(2, "B", 8),
            0x91: lambda: self.execute_res_b_r(2, "C", 8),
            0x92: lambda: self.execute_res_b_r(2, "D", 8),
            0x93: lambda: self.execute_res_b_r(2, "E", 8),
            0x94: lambda: self.execute_res_b_r(2, "H", 8),
            0x95: lambda: self.execute_res_b_r(2, "L", 8),
            0x96: lambda: self.execute_res_b_r(2, "HL", 16),
            0x97: lambda: self.execute_res_b_r(2, "A", 8),
            0x98: lambda: self.execute_res_b_r(3, "B", 8),
            0x99: lambda: self.execute_res_b_r(3, "C", 8),
            0x9A: lambda: self.execute_res_b_r(3, "D", 8),
            0x9B: lambda: self.execute_res_b_r(3, "E", 8),
            0x9C: lambda: self.execute_res_b_r(3, "H", 8),
            0x9D: lambda: self.execute_res_b_r(3, "L", 8),
            0x9E: lambda: self.execute_res_b_r(3, "HL", 16),
            0x9F: lambda: self.execute_res_b_r(3, "A", 8),
            0xA0: lambda: self.execute_res_b_r(4, "B", 8),
            0xA1: lambda: self.execute_res_b_r(4, "C", 8),
            0xA2: lambda: self.execute_res_b_r(4, "D", 8),
            0xA3: lambda: self.execute_res_b_r(4, "E", 8),
            0xA4: lambda: self.execute_res_b_r(4, "H", 8),
            0xA5: lambda: self.execute_res_b_r(4, "L", 8),
            0xA6: lambda: self.execute_res_b_r(4, "HL", 16),
            0xA7: lambda: self.execute_res_b_r(4, "A", 8),
            0xA8: lambda: self.execute_res_b_r(5, "B", 8),
            0xA9: lambda: self.execute_res_b_r(5, "C", 8),
            0xAA: lambda: self.execute_res_b_r(5, "D", 8),
            0xAB: lambda: self.execute_res_b_r(5, "E", 8),
            0xAC: lambda: self.execute_res_b_r(5, "H", 8),
            0xAD: lambda: self.execute_res_b_r(5, "L", 8),
            0xAE: lambda: self.execute_res_b_r(5, "HL", 16),
            0xAF: lambda: self.execute_res_b_r(5, "A", 8),
            0xB0: lambda: self.execute_res_b_r(6, "B", 8),
            0xB1: lambda: self.execute_res_b_r(6, "C", 8),
            0xB2: lambda: self.execute_res_b_r(6, "D", 8),
            0xB3: lambda: self.execute_res_b_r(6, "E", 8),
            0xB4: lambda: self.execute_res_b_r(6, "H", 8),
            0xB5: lambda: self.execute_res_b_r(6, "L", 8),
            0xB6: lambda: self.execute_res_b_r(6, "HL", 16),
            0xB7: lambda: self.execute_res_b_r(6, "A", 8),
            0xB8: lambda: self.execute_res_b_r(7, "B", 8),
            0xB9: lambda: self.execute_res_b_r(7, "C", 8),
            0xBA: lambda: self.execute_res_b_r(7, "D", 8),
            0xBB: lambda: self.execute_res_b_r(7, "E", 8),
            0xBC: lambda: self.execute_res_b_r(7, "H", 8),
            0xBD: lambda: self.execute_res_b_r(7, "L", 8),
            0xBE: lambda: self.execute_res_b_r(7, "HL", 16),
            0xBF: lambda: self.execute_res_b_r(7, "A", 8)
        }
        return instructions

    def execute_res_b_r(self, b, r, ticks):
        if r == "HL":
            addrs = (self.registers["H"] << 8) | self.registers["L"]
            value = self.mmu.read(addrs)
        else:
            value = self.registers[r]

        value = value & ~(1 << b)
        value &= 0xFF
        if r == "HL":
            self.mmu.write(addrs, value)
        else:
            self.registers[r] = value

        self.cpu.timer.tick(ticks)
        return ticks
