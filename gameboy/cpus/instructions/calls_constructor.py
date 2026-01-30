from .calls.call_cc_nn import CALL_CC_NN
from .calls.call_nn import CALL_NN


class CALL:
    def __init__(self, cpu):
        self.call_cc_nn = CALL_CC_NN(cpu)
        self.call_nn = CALL_NN(cpu)
