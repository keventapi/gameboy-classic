class ADD_SP_N:
    def __init__(self, cpu):
        self.cpu = cpu
        self.fetch = self.cpu.fetch

    def instructions_add_sp_n(self):
        instructions = {
            0xE8: (self.execute_add_sp_n, (16))
        }
        return instructions

    def execute_add_sp_n(self, ticks):
        imediate = self.fetch() & 0xFF
        signed_offset = imediate
        if signed_offset > 0x7F:
            signed_offset -= 0x100

        src = self.cpu.registers["sp"]
        Z = 0
        N = 0
        H = 1 if (src & 0xF) + (imediate & 0xF) > 0xF else 0
        C = 1 if (src & 0xFF) + imediate > 0xFF else 0
        self.cpu.set_flags(Z, N, H, C)
        self.cpu.registers["sp"] = (src + signed_offset) & 0xFFFF
        self.cpu.timer.tick(ticks)
        return ticks
