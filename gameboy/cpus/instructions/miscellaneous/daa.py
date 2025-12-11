class DAA:
    def __init__(self, cpu):
        self.cpu = cpu
        self.registers = self.cpu.registers

    def daa_instructions(self):
        instructions = {
            0x27: lambda: self.execute_daa(4)
        }
        return instructions

    def execute_daa(self, ticks):
        value = self.registers["A"] & 0xFF
        flag = self.registers["F"]
        old_N = (flag >> 6) & 1
        old_H = (flag >> 5) & 1
        old_C = (flag >> 4) & 1
        C = old_C

        if old_N == 0:
            if old_H or (value & 0x0F) > 0x09:
                value += 0x06

            if old_C or value > 0x99:
                value += 0x60
                C = 1

        else:
            if old_C:
                value -= 0x60

            if old_H:
                value -= 0x06

        value &= 0xFF
        Z = 1 if value == 0 else 0
        N = old_N
        H = 0

        self.cpu.set_flags(Z, N, H, C)
        self.registers["A"] = value & 0xFF
        self.cpu.timer.tick(ticks)
