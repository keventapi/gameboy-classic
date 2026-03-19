class LDACTION_A_HL:
    def __init__(self, cpu):
        self.cpu = cpu
        
        self.mmu = self.cpu.mmu

    def lda_a_hl_instruction(self):
        instructions = {
            0x3A: (self.execute_ldd, (True, 8)),
            0x32: (self.execute_ldd, (False, 8)),
            0x2A: (self.execute_ldi, (True, 8)),
            0x22: (self.execute_ldi, (False, 8))
        }
        return instructions

    def execute_ldd(self, read_hl, ticks):
        hl = (self.cpu.registers["H"] << 8) | self.cpu.registers["L"]
        if read_hl:
            self.cpu.registers["A"] = self.mmu.read(hl & 0xFFFF)
        else:
            self.mmu.write(hl, self.cpu.registers["A"])

        hl -= 1
        hl &= 0xFFFF
        h = (hl >> 8) & 0xFF
        l = hl & 0xFF
        self.cpu.registers["H"] = h
        self.cpu.registers["L"] = l
        self.cpu.timer.tick(ticks)
        return ticks

    def execute_ldi(self, read_hl, ticks):
        hl = (self.cpu.registers["H"] << 8) | self.cpu.registers["L"]
        if read_hl:
            self.cpu.registers["A"] = self.mmu.read(hl & 0xFFFF)
        else:
            self.mmu.write(hl, self.cpu.registers["A"])

        hl += 1
        hl &= 0xFFFF
        h = (hl >> 8) & 0xFF
        l = hl & 0xFF
        self.cpu.registers["H"] = h
        self.cpu.registers["L"] = l
        self.cpu.timer.tick(ticks)
        return ticks
