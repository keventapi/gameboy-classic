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

