class LD_NN_SP:
    def __init__(self):
        pass

    def ld_nn_sp_instructions(self):
        instruction = {
            0x08: lambda: self.execute_ld_nn_sp()
        }
        return instruction
    
    def execute_ld_nn_sp(self):
        low_byte_addr = self.fetch()
        high_byte_addr = self.fetch()
        nn = (high_byte_addr << 8) | low_byte_addr
        sp_value = self.registers["SP"]
        low_sp = sp_value & 0xFF
        high_sp = (sp_value >> 8) & 0xFF
        self.mmu.write(nn, low_sp)
        self.mmu.write(nn+1, high_sp)