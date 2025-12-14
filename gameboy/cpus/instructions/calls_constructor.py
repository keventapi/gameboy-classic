from .calls.call_cc_nn import CALL_CC_NN
from .calls.call_nn import CALL_NN


class CALL:
    def __init__(self, cpu):
        self.call_cc_nn = CALL_CC_NN(cpu)
        self.call_nn = CALL_NN(cpu)

    def get_call_instructions(self):
        instructions = {

        }
        updater = [
            self.call_cc_nn.call_cc_nn_instructions,
            self.call_nn.call_nn_instructions
        ]
        for u in updater:
            instructions.update(u())
        return instructions
