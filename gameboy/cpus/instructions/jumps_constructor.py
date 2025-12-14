from .jumps.jp_cc_nn import JP_CC_NN
from .jumps.jp_nn import JP_NN
from .jumps.jr_cc_n import JR_CC_N
from .jumps.jr_n import JR_N


class JUMP:
    def __init__(self, cpu):
        self.jp_cc_nn = JP_CC_NN(cpu)
        self.jp_nn = JP_NN(cpu)
        self.jr_cc_n = JR_CC_N(cpu)
        self.jr_n = JR_N(cpu)

    def get_jump_instructions(self):
        instructions = {

        }
        updater = [
            self.jp_cc_nn.jp_cc_nn_instructions,
            self.jp_nn.jp_nn_instructions,
            self.jr_cc_n.jr_cc_n_instructions,
            self.jr_n.jr_n_instructions
        ]
        for u in updater:
            instructions.update(u())
        return instructions
