class XOR_N:
    def __init__(self, cpu):
        self.cpu = cpu
        self.fetch = self.cpu.fetch
        self.mmu = self.cpu.mmu
        self.registers = self.cpu.registers

    def xor_n_instructions(self):
        instructions = {

        }
        return instructions

    def execute_xor_n(self, r, ticks):
        result = self.registers["A"]
        if len(r) > 1:
            addrs = (self.registers[r[0]] << 8) | self.registers[r[1]]
            result ^= self.mmu.read(addrs)
        elif r == "#":
            imediate = self.fetch()
            result ^= imediate
        else:
            result ^= self.registers[r]

        self.registers["F"] = 0x00

        if (result & 0xFF) == 0:
            self.registers["F"] |= 0b10000000

        self.registers["A"] = result & 0xFF
        self.registers["F"] &= 0xF0
        self.cpu.timer.tick(ticks)
