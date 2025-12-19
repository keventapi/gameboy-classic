class LD_HL_SP_N:
    def __init__(self, cpu):
        self.cpu = cpu
        self.fetch = self.cpu.fetch
        self.registers = self.cpu.registers
        self.mmu = self.cpu.mmu

    def ld_hl_sp_n_instructions(self):
        instructions = {
            0xF8: lambda: self.run_ld_hl_sp_n(12)
        }
        return instructions

    def run_ld_hl_sp_n(self, ticks):
        fetch = self.fetch()

        n = fetch
        if n >= 0x80:
            n -= 0x100

        sp = self.registers["SP"]
        addrs = (sp + n) & 0xFFFF

        self.registers["H"] = (addrs >> 8) & 0xFF
        self.registers["L"] = (addrs & 0xFF)

        H = 1 if ((sp & 0xF) + (fetch & 0xF)) > 0xF else 0
        C = 1 if ((sp & 0xFF) + fetch) > 0xFF else 0

        self.cpu.set_flags(0, 0, H, C)
        self.cpu.timer.tick(ticks)
        return ticks
