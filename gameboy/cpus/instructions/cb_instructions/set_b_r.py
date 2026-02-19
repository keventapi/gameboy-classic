class SET_B_R:
    def __init__(self, cpu):
        self.cpu = cpu
        self.registers = self.cpu.registers
        self.mmu = self.cpu.mmu

    def set_b_r_intructions(self):
        instructions = {
            0xC7: (self.execute_set_b_r, (0, "A", 8)),
            0xC0: (self.execute_set_b_r, (0, "B", 8)),
            0xC1: (self.execute_set_b_r, (0, "C", 8)),
            0xC2: (self.execute_set_b_r, (0, "D", 8)),
            0xC3: (self.execute_set_b_r, (0, "E", 8)),
            0xC4: (self.execute_set_b_r, (0, "H", 8)),
            0xC5: (self.execute_set_b_r, (0, "L", 8)),
            0xC6: (self.execute_set_b_r, (0, "HL", 16)),
            0xC8: (self.execute_set_b_r, (1, "B", 8)),
            0xC9: (self.execute_set_b_r, (1, "C", 8)),
            0xCA: (self.execute_set_b_r, (1, "D", 8)),
            0xCB: (self.execute_set_b_r, (1, "E", 8)),
            0xCC: (self.execute_set_b_r, (1, "H", 8)),
            0xCD: (self.execute_set_b_r, (1, "L", 8)),
            0xCE: (self.execute_set_b_r, (1, "HL", 16)),
            0xCF: (self.execute_set_b_r, (1, "A", 8)),
            0xD0: (self.execute_set_b_r, (2, "B", 8)),
            0xD1: (self.execute_set_b_r, (2, "C", 8)),
            0xD2: (self.execute_set_b_r, (2, "D", 8)),
            0xD3: (self.execute_set_b_r, (2, "E", 8)),
            0xD4: (self.execute_set_b_r, (2, "H", 8)),
            0xD5: (self.execute_set_b_r, (2, "L", 8)),
            0xD6: (self.execute_set_b_r, (2, "HL", 16)),
            0xD7: (self.execute_set_b_r, (2, "A", 8)),
            0xD8: (self.execute_set_b_r, (3, "B", 8)),
            0xD9: (self.execute_set_b_r, (3, "C", 8)),
            0xDA: (self.execute_set_b_r, (3, "D", 8)),
            0xDB: (self.execute_set_b_r, (3, "E", 8)),
            0xDC: (self.execute_set_b_r, (3, "H", 8)),
            0xDD: (self.execute_set_b_r, (3, "L", 8)),
            0xDE: (self.execute_set_b_r, (3, "HL", 16)),
            0xDF: (self.execute_set_b_r, (3, "A", 8)),
            0xE0: (self.execute_set_b_r, (4, "B", 8)),
            0xE1: (self.execute_set_b_r, (4, "C", 8)),
            0xE2: (self.execute_set_b_r, (4, "D", 8)),
            0xE3: (self.execute_set_b_r, (4, "E", 8)),
            0xE4: (self.execute_set_b_r, (4, "H", 8)),
            0xE5: (self.execute_set_b_r, (4, "L", 8)),
            0xE6: (self.execute_set_b_r, (4, "HL", 16)),
            0xE7: (self.execute_set_b_r, (4, "A", 8)),
            0xE8: (self.execute_set_b_r, (5, "B", 8)),
            0xE9: (self.execute_set_b_r, (5, "C", 8)),
            0xEA: (self.execute_set_b_r, (5, "D", 8)),
            0xEB: (self.execute_set_b_r, (5, "E", 8)),
            0xEC: (self.execute_set_b_r, (5, "H", 8)),
            0xED: (self.execute_set_b_r, (5, "L", 8)),
            0xEE: (self.execute_set_b_r, (5, "HL", 16)),
            0xEF: (self.execute_set_b_r, (5, "A", 8)),
            0xF0: (self.execute_set_b_r, (6, "B", 8)),
            0xF1: (self.execute_set_b_r, (6, "C", 8)),
            0xF2: (self.execute_set_b_r, (6, "D", 8)),
            0xF3: (self.execute_set_b_r, (6, "E", 8)),
            0xF4: (self.execute_set_b_r, (6, "H", 8)),
            0xF5: (self.execute_set_b_r, (6, "L", 8)),
            0xF6: (self.execute_set_b_r, (6, "HL", 16)),
            0xF7: (self.execute_set_b_r, (6, "A", 8)),
            0xF8: (self.execute_set_b_r, (7, "B", 8)),
            0xF9: (self.execute_set_b_r, (7, "C", 8)),
            0xFA: (self.execute_set_b_r, (7, "D", 8)),
            0xFB: (self.execute_set_b_r, (7, "E", 8)),
            0xFC: (self.execute_set_b_r, (7, "H", 8)),
            0xFD: (self.execute_set_b_r, (7, "L", 8)),
            0xFE: (self.execute_set_b_r, (7, "HL", 16)),
            0xFF: (self.execute_set_b_r, (7, "A", 8))
        }
        return instructions

    def execute_set_b_r(self, b, r, ticks):
        self.cpu.timer.tick(4)
        if r == "HL":
            addrs = (self.registers["H"] << 8) | self.registers["L"]
            value = self.mmu.read(addrs)
            self.cpu.timer.tick(4)
        else:
            value = self.registers[r]

        value = value | 1 << b
        value &= 0xFF
        if r == "HL":
            self.mmu.write(addrs, value)
            self.cpu.timer.tick(4)
        else:
            self.registers[r] = value

        self.cpu.timer.tick(4)
        return ticks
