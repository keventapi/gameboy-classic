class ADC_A_N:
    def __init__(self, cpu):
        self.cpu = cpu
        self.fetch = self.cpu.fetch
        self.registers = self.cpu.registers
        self.mmu = self.cpu.mmu

    def adc_a_n_instructions(self):
        instructions = {
            0x8F: lambda: self.execute_adc_a_n("A"),
            0x88: lambda: self.execute_adc_a_n("B"),
            0x89: lambda: self.execute_adc_a_n("C"),
            0x8A: lambda: self.execute_adc_a_n("D"),
            0x8B: lambda: self.execute_adc_a_n("E"),
            0x8C: lambda: self.execute_adc_a_n("H"),
            0x8D: lambda: self.execute_adc_a_n("L"),
            0x8E: lambda: self.execute_adc_a_n("HL"),
            0xCE: lambda: self.execute_adc_a_n("#")
        }
        return instructions

    def execute_adc_a_n(self, r):
        if r == "HL":
            addrs = (self.registers["H"] << 8) | self.registers["L"]
            n = self.mmu.read(addrs)
        elif r == "#":
            n = self.fetch()
        else:
            n = self.registers[r]

        carry_flag = (self.registers["F"] >> 4) & 1
        sum = n + carry_flag + self.registers["A"]

        # Z
        if sum & 0xFF == 0:
            self.registers["F"] |= 0b10000000
        else:
            self.registers["F"] &= 0b01111111

        # N
        self.registers["F"] &= 0b10111111

        # H
        if ((self.registers["A"] & 0xF) + (n & 0xF) + carry_flag) > 0xF:
            self.registers["F"] |= 0b00100000
        else:
            self.registers["F"] &= 0b11011111

        # C
        if sum > 0xFF:
            self.registers["F"] |= 0b00010000
        else:
            self.registers["F"] &= 0b11101111

        self.registers["A"] = sum & 0xFF
        self.registers["F"] &= 0xF0
