class RLC_N:
    def __init__(self, cpu):
        self.cpu = cpu
        self.mmu = self.cpu.mmu
        

    def rlc_n_instructions(self):
        instructions = {
            0x07: (self.execute_rlc_n, ("A", 8)),
            0x00: (self.execute_rlc_n, ("B", 8)),
            0x01: (self.execute_rlc_n, ("C", 8)),
            0x02: (self.execute_rlc_n, ("D", 8)),
            0x03: (self.execute_rlc_n, ("E", 8)),
            0x04: (self.execute_rlc_n, ("H", 8)),
            0x05: (self.execute_rlc_n, ("L", 8)),
            0x06: (self.execute_rlc_n, ("HL", 16))
        }
        return instructions

    def execute_rlc_n(self, r, ticks):
        self.cpu.timer.tick(4)
        if r == "HL":
            addrs = (self.cpu.registers["H"] << 8) | self.cpu.registers["L"]
            value = self.mmu.read(addrs)
            self.cpu.timer.tick(4)
        else:
            value = self.cpu.registers[r]

        bit7 = (value >> 7) & 1
        value = (value << 1) & 0xFF
        value |= bit7
        Z = 1 if value == 0 else 0
        N = 0
        H = 0
        C = bit7

        if r == "HL":
            self.mmu.write(addrs, value)
            self.cpu.timer.tick(4)
        else:
            self.cpu.registers[r] = value

        self.cpu.set_flags(Z, N, H, C)
        self.cpu.timer.tick(4)
        return ticks
