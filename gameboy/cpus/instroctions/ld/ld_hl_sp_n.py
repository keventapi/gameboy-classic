class LD_HL_SP_N:
    def __init__():
        pass

    def ld_hl_sp_n_instructions(self):
        instructions = {
            0xF8: lambda: self.run_ld_hl_sp_n()
        }
        return instructions
    
    def run_ld_hl_sp_n(self):
        n = self.fetch()
        if n >= 0x80:
            n -= 0x100
        
        sp = self.registers["SP"] & 0xFF
        addrs = (sp + n) & 0xFFFF

        self.registers["H"] = (addrs >> 8) & 0xFF
        self.registers["L"] = (addrs & 0xFF)
        
        # reset Z e N
        self.registers["F"] &= 0b00110000
        unsigned = (n & 0xFF)

        # reset H dependendo da operação
        if (((sp & 0xF) + (unsigned & 0xF)) & 0x10) != 0:
            self.registers["F"] |= 0b00100000
        else:
            self.registers["F"] &= 0b11010000

        # rest N dependendo da operação
        if ((sp + unsigned) & 0x100) != 0:
            self.registers["F"] |= 0b00010000
        else:
            self.registers["F"] &= 0b11100000

        # zera os bits 3 a 4
        self.registers["F"] &= 0xF0

