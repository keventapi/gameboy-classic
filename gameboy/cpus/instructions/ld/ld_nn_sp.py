class LD_NN_SP:
    def __init__(self, cpu):
        self.cpu = cpu
        self.fetch = self.cpu.fetch
        self.registers = self.cpu.registers
        self.mmu = self.cpu.mmu

    def ld_nn_sp_instructions(self):
        instruction = {
            0x08: (self.execute_ld_nn_sp, (20))
        }
        return instruction

    def execute_ld_nn_sp(self, ticks):
        low_byte_addr = self.fetch()
        high_byte_addr = self.fetch()
        nn = ((high_byte_addr << 8) | low_byte_addr) & 0xFFFF
        sp_value = self.registers["SP"]
        low_sp = sp_value & 0xFF
        high_sp = (sp_value >> 8) & 0xFF
        self.mmu.write(nn, low_sp)
        self.mmu.write((nn+1) & 0xFFFF, high_sp)
        self.cpu.timer.tick(ticks)
        return ticks
