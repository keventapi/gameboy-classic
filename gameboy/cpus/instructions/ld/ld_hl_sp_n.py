class LD_HL_SP_N:
    def __init__(self, cpu):
        self.cpu = cpu
        self.fetch = self.cpu.fetch
        self.registers = self.cpu.registers
        self.mmu = self.cpu.mmu

    def ld_hl_sp_n_instructions(self):
        instructions = {
            0xF8: lambda: self.run_ld_hl_sp_n()
        }
        return instructions

    def run_ld_hl_sp_n(self):
        fetch = self.fetch()

        n = fetch
        if n >= 0x80:
            n -= 0x100

        sp = self.registers["SP"]
        addrs = (sp + n) & 0xFFFF

        self.registers["H"] = (addrs >> 8) & 0xFF
        self.registers["L"] = (addrs & 0xFF)

        # reset Z e N
        self.registers["F"] &= 0b00110000

        # reset H dependendo da operação
        if ((sp & 0xF) + (fetch & 0xF)) > 0xF:
            self.registers["F"] |= 0b00100000
        else:
            self.registers["F"] &= 0b11010000

        # rest C dependendo da operação
        if ((sp & 0xFF) + fetch) > 0xFF:
            self.registers["F"] |= 0b00010000
        else:
            self.registers["F"] &= 0b11100000

        # zera os bits 3 a 4
        self.registers["F"] &= 0xF0
