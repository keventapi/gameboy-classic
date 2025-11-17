class LD_SP_HL:
    def __init__(self) -> None:
        pass

    def ld_sp_hl_instructions(self):
        instructions = {
            0xF9: lambda: self.execute_ld_sp_hl()
        }
        return instructions
    
    def execute_ld_sp_hl(self):
        hl = (self.registers["H"] << 8) | self.registers["L"]
        self.registers["SP"] = hl