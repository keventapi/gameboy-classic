from ld.ld_nn_n import LD_NN_N
from ld.ld_r1_r2 import LD_R1_R2
from ld.ld_a_n import LD_A_N
from ld.ld_a_ff00_c import LD_A_FF00_C


class LD(LD_NN_N, LD_R1_R2, LD_A_N, LD_A_FF00_C):
    def __init__(self):
        self.instructions = {}
        self.instructions.update(self.ld_nn_n_instructions())
        self.instructions.update(self.ld_r1_r2_instructions())
        self.instructions.update(self.ld_a_n_instructions())
        self.instructions.update(self.ld_a_ff00_c_instructions())


