class SLA_N:
    def __init__(self, cpu):
        self.cpu = cpu
        
        self.mmu = self.cpu.mmu

    def sla_n_instructions(self):
        instructions = {
            0x27: (self.execute_sla_n, ("A", 8)),
            0x20: (self.execute_sla_n, ("B", 8)),
            0x21: (self.execute_sla_n, ("C", 8)),
            0x22: (self.execute_sla_n, ("D", 8)),
            0x23: (self.execute_sla_n, ("E", 8)),
            0x24: (self.execute_sla_n, ("H", 8)),
            0x25: (self.execute_sla_n, ("L", 8)),
            0x26: (self.execute_sla_n, ("HL", 16))
        }
        return instructions

    def execute_sla_n(self, r, ticks):
        self.cpu.timer.tick(4)
        if r == "HL":
            addrs = (self.cpu.registers["H"] << 8) | self.cpu.registers["L"]
            value = self.mmu.read(addrs)
            self.cpu.timer.tick(4)
        else:
            value = self.cpu.registers[r]

        C = (value >> 7) & 1
        value = (value << 1) & 0xFF
        Z = 1 if value == 0 else 0
        H = 0
        N = 0
        self.cpu.set_flags(Z, N, H, C)

        if r == "HL":
            self.mmu.write(addrs, value)
            self.cpu.timer.tick(4)
        else:
            self.cpu.registers[r] = value

        self.cpu.timer.tick(4)
        return ticks
