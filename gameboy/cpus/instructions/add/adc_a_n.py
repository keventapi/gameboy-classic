class ADC_A_N:
    def __init__(self, cpu):
        self.cpu = cpu
        self.fetch = self.cpu.fetch
        self.registers = self.cpu.registers
        self.mmu = self.cpu.mmu

    def adc_a_n_instructions(self):
        instructions = {
            0x8F: lambda: self.execute_adc_a_n("A", 4),
            0x88: lambda: self.execute_adc_a_n("B", 4),
            0x89: lambda: self.execute_adc_a_n("C", 4),
            0x8A: lambda: self.execute_adc_a_n("D", 4),
            0x8B: lambda: self.execute_adc_a_n("E", 4),
            0x8C: lambda: self.execute_adc_a_n("H", 4),
            0x8D: lambda: self.execute_adc_a_n("L", 4),
            0x8E: lambda: self.execute_adc_a_n("HL", 8),
            0xCE: lambda: self.execute_adc_a_n("#", 8)
        }
        return instructions

    def execute_adc_a_n(self, r, ticks):
        if r == "HL":
            addrs = (self.registers["H"] << 8) | self.registers["L"]
            n = self.mmu.read(addrs)
        elif r == "#":
            n = self.fetch()
        else:
            n = self.registers[r]

        carry_flag = (self.registers["F"] >> 4) & 1
        sum = n + carry_flag + self.registers["A"]

        Z = 1 if sum & 0xFF == 0 else 0
        N = 0
        H = 1 if ((self.registers["A"] & 0xF) + (n & 0xF) + carry_flag) > 0xF else 0
        C = 1 if sum > 0xFF else 0

        self.registers["A"] = sum & 0xFF
        self.cpu.set_flags(Z, N, H, C)
        self.cpu.timer.tick(ticks)
        return ticks
