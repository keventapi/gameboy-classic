class BIT_B_R:
    def __init__(self, cpu):
        self.cpu = cpu
        self.registers = self.cpu.registers
        self.mmu = self.cpu.mmu

    def bit_b_r_instructions(self):
        instructions = {
            0x47: lambda: self.execute_bit_b_r(0, "A", 8),
            0x40: lambda: self.execute_bit_b_r(0, "B", 8),
            0x41: lambda: self.execute_bit_b_r(0, "C", 8),
            0x42: lambda: self.execute_bit_b_r(0, "D", 8),
            0x43: lambda: self.execute_bit_b_r(0, "E", 8),
            0x44: lambda: self.execute_bit_b_r(0, "H", 8),
            0x45: lambda: self.execute_bit_b_r(0, "L", 8),
            0x46: lambda: self.execute_bit_b_r(0, "HL", 12),
            0x48: lambda: self.execute_bit_b_r(1, "B", 8),
            0x49: lambda: self.execute_bit_b_r(1, "C", 8),
            0x4A: lambda: self.execute_bit_b_r(1, "D", 8),
            0x4B: lambda: self.execute_bit_b_r(1, "E", 8),
            0x4C: lambda: self.execute_bit_b_r(1, "H", 8),
            0x4D: lambda: self.execute_bit_b_r(1, "L", 8),
            0x4E: lambda: self.execute_bit_b_r(1, "HL", 12),
            0x4F: lambda: self.execute_bit_b_r(1, "A", 8),
            0x50: lambda: self.execute_bit_b_r(2, "B", 8),
            0x51: lambda: self.execute_bit_b_r(2, "C", 8),
            0x52: lambda: self.execute_bit_b_r(2, "D", 8),
            0x53: lambda: self.execute_bit_b_r(2, "E", 8),
            0x54: lambda: self.execute_bit_b_r(2, "H", 8),
            0x55: lambda: self.execute_bit_b_r(2, "L", 8),
            0x56: lambda: self.execute_bit_b_r(2, "HL", 12),
            0x57: lambda: self.execute_bit_b_r(2, "A", 8),
            0x58: lambda: self.execute_bit_b_r(3, "B", 8),
            0x59: lambda: self.execute_bit_b_r(3, "C", 8),
            0x5A: lambda: self.execute_bit_b_r(3, "D", 8),
            0x5B: lambda: self.execute_bit_b_r(3, "E", 8),
            0x5C: lambda: self.execute_bit_b_r(3, "H", 8),
            0x5D: lambda: self.execute_bit_b_r(3, "L", 8),
            0x5E: lambda: self.execute_bit_b_r(3, "HL", 12),
            0x5F: lambda: self.execute_bit_b_r(3, "A", 8),
            0x60: lambda: self.execute_bit_b_r(4, "B", 8),
            0x61: lambda: self.execute_bit_b_r(4, "C", 8),
            0x62: lambda: self.execute_bit_b_r(4, "D", 8),
            0x63: lambda: self.execute_bit_b_r(4, "E", 8),
            0x64: lambda: self.execute_bit_b_r(4, "H", 8),
            0x65: lambda: self.execute_bit_b_r(4, "L", 8),
            0x66: lambda: self.execute_bit_b_r(4, "HL", 12),
            0x67: lambda: self.execute_bit_b_r(4, "A", 8),
            0x68: lambda: self.execute_bit_b_r(5, "B", 8),
            0x69: lambda: self.execute_bit_b_r(5, "C", 8),
            0x6A: lambda: self.execute_bit_b_r(5, "D", 8),
            0x6B: lambda: self.execute_bit_b_r(5, "E", 8),
            0x6C: lambda: self.execute_bit_b_r(5, "H", 8),
            0x6D: lambda: self.execute_bit_b_r(5, "L", 8),
            0x6E: lambda: self.execute_bit_b_r(5, "HL", 12),
            0x6F: lambda: self.execute_bit_b_r(5, "A", 8),
            0x70: lambda: self.execute_bit_b_r(6, "B", 8),
            0x71: lambda: self.execute_bit_b_r(6, "C", 8),
            0x72: lambda: self.execute_bit_b_r(6, "D", 8),
            0x73: lambda: self.execute_bit_b_r(6, "E", 8),
            0x74: lambda: self.execute_bit_b_r(6, "H", 8),
            0x75: lambda: self.execute_bit_b_r(6, "L", 8),
            0x76: lambda: self.execute_bit_b_r(6, "HL", 12),
            0x77: lambda: self.execute_bit_b_r(6, "A", 8),
            0x78: lambda: self.execute_bit_b_r(7, "B", 8),
            0x79: lambda: self.execute_bit_b_r(7, "C", 8),
            0x7A: lambda: self.execute_bit_b_r(7, "D", 8),
            0x7B: lambda: self.execute_bit_b_r(7, "E", 8),
            0x7C: lambda: self.execute_bit_b_r(7, "H", 8),
            0x7D: lambda: self.execute_bit_b_r(7, "L", 8),
            0x7E: lambda: self.execute_bit_b_r(7, "HL", 12),
            0x7F: lambda: self.execute_bit_b_r(7, "A", 8)
        }
        return instructions

    def execute_bit_b_r(self, b, r, ticks):
        flag = self.registers["F"]
        if r == "HL":
            addrs = (self.registers["H"] << 8) | self.registers["L"]
            value = self.mmu.read(addrs)
        else:
            value = self.registers[r]

        bitx = (value >> b) & 1
        Z = 1 if bitx == 0 else 0
        N = 0
        H = 1
        C = (flag >> 4) & 1

        self.cpu.set_flags(Z, N, H, C)

        self.cpu.timer.tick(ticks)
        return ticks
