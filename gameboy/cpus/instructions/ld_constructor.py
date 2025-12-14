from .ld.ld_a_ff00_c import LD_A_FF00_C
from .ld.ld_a_ff00_n import LD_A_FF00_N
from .ld.ld_a_n import LD_A_N
from .ld.ld_hl_sp_n import LD_HL_SP_N
from .ld.ld_n_nn import LD_N_NN
from .ld.ld_nn_n import LD_NN_N
from .ld.ld_nn_sp import LD_NN_SP
from .ld.ld_r1_r2 import LD_R1_R2
from .ld.ld_sp_hl import LD_SP_HL
from .ld.lda_a_hl import LDACTION_A_HL


class LD:
    def __init__(self, cpu):
        self.ld_a_ff00_c = LD_A_FF00_C(cpu)
        self.ld_a_ff00_n = LD_A_FF00_N(cpu)
        self.ld_a_n = LD_A_N(cpu)
        self.ld_hl_sp_n = LD_HL_SP_N(cpu)
        self.ld_n_nn = LD_N_NN(cpu)
        self.ld_nn_n = LD_NN_N(cpu)
        self.ld_nn_sp = LD_NN_SP(cpu)
        self.ld_r1_r2 = LD_R1_R2(cpu)
        self.ld_sp_hl = LD_SP_HL(cpu)
        self.ldaction_a_hl = LDACTION_A_HL(cpu)

    def get_ld_instructions(self):
        instructions = {}
        updater = [self.ld_a_ff00_c.ld_a_ff00_c_instructions,
                   self.ld_a_ff00_n.ld_a_ff00_n_instructions,
                   self.ld_a_n.ld_a_n_instructions,
                   self.ld_hl_sp_n.ld_hl_sp_n_instructions,
                   self.ld_n_nn.ld_n_nn_instructions,
                   self.ld_nn_n.ld_nn_n_instructions,
                   self.ld_nn_sp.ld_nn_sp_instructions,
                   self.ld_r1_r2.ld_r1_r2_instructions,
                   self.ld_sp_hl.ld_sp_hl_instructions,
                   self.ldaction_a_hl.lda_a_hl_instruction]
        for i in updater:
            instructions.update(i())
        return instructions
