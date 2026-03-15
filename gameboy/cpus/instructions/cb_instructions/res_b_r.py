class RES_B_R:
    def __init__(self, cpu):
        self.cpu = cpu
        self.mmu = self.cpu.mmu

    def res_b_r_intructions(self):
        instructions = {
            0x87: (self.execute_res_b_r, (0, "A", 8)),
            0x80: (self.execute_res_b_r, (0, "B", 8)),
            0x81: (self.execute_res_b_r, (0, "C", 8)),
            0x82: (self.execute_res_b_r, (0, "D", 8)),
            0x83: (self.execute_res_b_r, (0, "E", 8)),
            0x84: (self.execute_res_b_r, (0, "H", 8)),
            0x85: (self.execute_res_b_r, (0, "L", 8)),
            0x86: (self.execute_res_b_r, (0, "HL", 16)),
            0x88: (self.execute_res_b_r, (1, "B", 8)),
            0x89: (self.execute_res_b_r, (1, "C", 8)),
            0x8A: (self.execute_res_b_r, (1, "D", 8)),
            0x8B: (self.execute_res_b_r, (1, "E", 8)),
            0x8C: (self.execute_res_b_r, (1, "H", 8)),
            0x8D: (self.execute_res_b_r, (1, "L", 8)),
            0x8E: (self.execute_res_b_r, (1, "HL", 16)),
            0x8F: (self.execute_res_b_r, (1, "A", 8)),
            0x90: (self.execute_res_b_r, (2, "B", 8)),
            0x91: (self.execute_res_b_r, (2, "C", 8)),
            0x92: (self.execute_res_b_r, (2, "D", 8)),
            0x93: (self.execute_res_b_r, (2, "E", 8)),
            0x94: (self.execute_res_b_r, (2, "H", 8)),
            0x95: (self.execute_res_b_r, (2, "L", 8)),
            0x96: (self.execute_res_b_r, (2, "HL", 16)),
            0x97: (self.execute_res_b_r, (2, "A", 8)),
            0x98: (self.execute_res_b_r, (3, "B", 8)),
            0x99: (self.execute_res_b_r, (3, "C", 8)),
            0x9A: (self.execute_res_b_r, (3, "D", 8)),
            0x9B: (self.execute_res_b_r, (3, "E", 8)),
            0x9C: (self.execute_res_b_r, (3, "H", 8)),
            0x9D: (self.execute_res_b_r, (3, "L", 8)),
            0x9E: (self.execute_res_b_r, (3, "HL", 16)),
            0x9F: (self.execute_res_b_r, (3, "A", 8)),
            0xA0: (self.execute_res_b_r, (4, "B", 8)),
            0xA1: (self.execute_res_b_r, (4, "C", 8)),
            0xA2: (self.execute_res_b_r, (4, "D", 8)),
            0xA3: (self.execute_res_b_r, (4, "E", 8)),
            0xA4: (self.execute_res_b_r, (4, "H", 8)),
            0xA5: (self.execute_res_b_r, (4, "L", 8)),
            0xA6: (self.execute_res_b_r, (4, "HL", 16)),
            0xA7: (self.execute_res_b_r, (4, "A", 8)),
            0xA8: (self.execute_res_b_r, (5, "B", 8)),
            0xA9: (self.execute_res_b_r, (5, "C", 8)),
            0xAA: (self.execute_res_b_r, (5, "D", 8)),
            0xAB: (self.execute_res_b_r, (5, "E", 8)),
            0xAC: (self.execute_res_b_r, (5, "H", 8)),
            0xAD: (self.execute_res_b_r, (5, "L", 8)),
            0xAE: (self.execute_res_b_r, (5, "HL", 16)),
            0xAF: (self.execute_res_b_r, (5, "A", 8)),
            0xB0: (self.execute_res_b_r, (6, "B", 8)),
            0xB1: (self.execute_res_b_r, (6, "C", 8)),
            0xB2: (self.execute_res_b_r, (6, "D", 8)),
            0xB3: (self.execute_res_b_r, (6, "E", 8)),
            0xB4: (self.execute_res_b_r, (6, "H", 8)),
            0xB5: (self.execute_res_b_r, (6, "L", 8)),
            0xB6: (self.execute_res_b_r, (6, "HL", 16)),
            0xB7: (self.execute_res_b_r, (6, "A", 8)),
            0xB8: (self.execute_res_b_r, (7, "B", 8)),
            0xB9: (self.execute_res_b_r, (7, "C", 8)),
            0xBA: (self.execute_res_b_r, (7, "D", 8)),
            0xBB: (self.execute_res_b_r, (7, "E", 8)),
            0xBC: (self.execute_res_b_r, (7, "H", 8)),
            0xBD: (self.execute_res_b_r, (7, "L", 8)),
            0xBE: (self.execute_res_b_r, (7, "HL", 16)),
            0xBF: (self.execute_res_b_r, (7, "A", 8))
        }
        return instructions

    def execute_res_b_r(self, b, r, ticks):
        self.cpu.timer.tick(4)
        if r == "HL":
            addrs = (self.cpu.registers["H"] << 8) | self.cpu.registers["L"]
            value = self.mmu.read(addrs)
            self.cpu.timer.tick(4)
        else:
            value = self.cpu.registers[r]

        value = value & ~(1 << b)
        value &= 0xFF
        if r == "HL":
            self.mmu.write(addrs, value)
            self.cpu.timer.tick(4)
        else:
            self.cpu.registers[r] = value

        self.cpu.timer.tick(4)
        return ticks
