class SWAP_N:
    def __init__(self, cpu):  # necessario dispatcher pra instruções CB
        self.cpu = cpu
        self.registers = self.cpu.registers
        self.mmu = self.cpu.mmu

    def instructions_swap_n(self):
        instructions = {
            0x37: (self.execute_swap_n, ("A", 8)),
            0x30: (self.execute_swap_n, ("B", 8)),
            0x31: (self.execute_swap_n, ("C", 8)),
            0x32: (self.execute_swap_n, ("D", 8)),
            0x33: (self.execute_swap_n, ("E", 8)),
            0x34: (self.execute_swap_n, ("H", 8)),
            0x35: (self.execute_swap_n, ("L", 8)),
            0x36: (self.execute_swap_n, ("HL", 16))
        }
        return instructions

    def execute_swap_n(self, r, ticks):
        if len(r) > 1:
            addrs = (self.registers[r[0]] << 8) | self.registers[r[1]]
            value = self.mmu.read(addrs)
            result = ((value & 0xF) << 4) | (value >> 4) & 0xF
            self.mmu.write(addrs, result & 0xFF)
        else:
            value = self.registers[r]
            result = ((value & 0xF) << 4) | ((value >> 4) & 0xF)
            self.registers[r] = result & 0xFF

        Z = 1 if (result & 0xFF) == 0 else 0
        self.cpu.set_flags(Z, 0, 0, 0)
        self.cpu.timer.tick(ticks)
        return ticks
