class SET_B_R:
    def __init__(self, cpu):
        self.cpu = cpu
        self.registers = self.cpu.registers
        self.mmu = self.cpu.mmu

    def set_b_r_intructions(self):
        instructions = {
            0xC7: lambda: self.execute_set_b_r(0, "A", 8),
            0xC0: lambda: self.execute_set_b_r(0, "B", 8),
            0xC1: lambda: self.execute_set_b_r(0, "C", 8),
            0xC2: lambda: self.execute_set_b_r(0, "D", 8),
            0xC3: lambda: self.execute_set_b_r(0, "E", 8),
            0xC4: lambda: self.execute_set_b_r(0, "H", 8),
            0xC5: lambda: self.execute_set_b_r(0, "L", 8),
            0xC6: lambda: self.execute_set_b_r(0, "HL", 16),
            0xC8: lambda: self.execute_set_b_r(1, "B", 8),
            0xC9: lambda: self.execute_set_b_r(1, "C", 8),
            0xCA: lambda: self.execute_set_b_r(1, "D", 8),
            0xCB: lambda: self.execute_set_b_r(1, "E", 8),
            0xCC: lambda: self.execute_set_b_r(1, "H", 8),
            0xCD: lambda: self.execute_set_b_r(1, "L", 8),
            0xCE: lambda: self.execute_set_b_r(1, "HL", 16),
            0xCF: lambda: self.execute_set_b_r(1, "A", 8),
            0xD0: lambda: self.execute_set_b_r(2, "B", 8),
            0xD1: lambda: self.execute_set_b_r(2, "C", 8),
            0xD2: lambda: self.execute_set_b_r(2, "D", 8),
            0xD3: lambda: self.execute_set_b_r(2, "E", 8),
            0xD4: lambda: self.execute_set_b_r(2, "H", 8),
            0xD5: lambda: self.execute_set_b_r(2, "L", 8),
            0xD6: lambda: self.execute_set_b_r(2, "HL", 16),
            0xD7: lambda: self.execute_set_b_r(2, "A", 8),
            0xD8: lambda: self.execute_set_b_r(3, "B", 8),
            0xD9: lambda: self.execute_set_b_r(3, "C", 8),
            0xDA: lambda: self.execute_set_b_r(3, "D", 8),
            0xDB: lambda: self.execute_set_b_r(3, "E", 8),
            0xDC: lambda: self.execute_set_b_r(3, "H", 8),
            0xDD: lambda: self.execute_set_b_r(3, "L", 8),
            0xDE: lambda: self.execute_set_b_r(3, "HL", 16),
            0xDF: lambda: self.execute_set_b_r(3, "A", 8),
            0xE0: lambda: self.execute_set_b_r(4, "B", 8),
            0xE1: lambda: self.execute_set_b_r(4, "C", 8),
            0xE2: lambda: self.execute_set_b_r(4, "D", 8),
            0xE3: lambda: self.execute_set_b_r(4, "E", 8),
            0xE4: lambda: self.execute_set_b_r(4, "H", 8),
            0xE5: lambda: self.execute_set_b_r(4, "L", 8),
            0xE6: lambda: self.execute_set_b_r(4, "HL", 16),
            0xE7: lambda: self.execute_set_b_r(4, "A", 8),
            0xE8: lambda: self.execute_set_b_r(5, "B", 8),
            0xE9: lambda: self.execute_set_b_r(5, "C", 8),
            0xEA: lambda: self.execute_set_b_r(5, "D", 8),
            0xEB: lambda: self.execute_set_b_r(5, "E", 8),
            0xEC: lambda: self.execute_set_b_r(5, "H", 8),
            0xED: lambda: self.execute_set_b_r(5, "L", 8),
            0xEE: lambda: self.execute_set_b_r(5, "HL", 16),
            0xEF: lambda: self.execute_set_b_r(5, "A", 8),
            0xF0: lambda: self.execute_set_b_r(6, "B", 8),
            0xF1: lambda: self.execute_set_b_r(6, "C", 8),
            0xF2: lambda: self.execute_set_b_r(6, "D", 8),
            0xF3: lambda: self.execute_set_b_r(6, "E", 8),
            0xF4: lambda: self.execute_set_b_r(6, "H", 8),
            0xF5: lambda: self.execute_set_b_r(6, "L", 8),
            0xF6: lambda: self.execute_set_b_r(6, "HL", 16),
            0xF7: lambda: self.execute_set_b_r(6, "A", 8),
            0xF8: lambda: self.execute_set_b_r(7, "B", 8),
            0xF9: lambda: self.execute_set_b_r(7, "C", 8),
            0xFA: lambda: self.execute_set_b_r(7, "D", 8),
            0xFB: lambda: self.execute_set_b_r(7, "E", 8),
            0xFC: lambda: self.execute_set_b_r(7, "H", 8),
            0xFD: lambda: self.execute_set_b_r(7, "L", 8),
            0xFE: lambda: self.execute_set_b_r(7, "HL", 16),
            0xFF: lambda: self.execute_set_b_r(7, "A", 8)
        }
        return instructions

    def execute_set_b_r(self, b, r, ticks):
        if r == "HL":
            addrs = (self.registers["H"] << 8) | self.registers["L"]
            value = self.mmu.read(addrs)
        else:
            value = self.registers[r]

        value = value | 1 << b
        value &= 0xFF
        if r == "HL":
            self.mmu.write(addrs, value)
        else:
            self.registers[r] = value

        self.cpu.timer.tick(ticks)
        return ticks
