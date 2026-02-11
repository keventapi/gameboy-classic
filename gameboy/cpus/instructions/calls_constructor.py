from .calls.call_cc_nn import CALL_CC_NN
from .calls.call_nn import CALL_NN


class CALL:
    def __init__(self, cpu):
        self.call_cc_nn = CALL_CC_NN(cpu)
        self.call_nn = CALL_NN(cpu)

        instances = [
            self.call_cc_nn,
            self.call_nn
        ]

        for instance in instances:
            for attr_name in dir(instance):
                if not attr_name.startswith("__"):
                    attr_value = getattr(instance, attr_name)
                    if callable(attr_value):
                        setattr(self, attr_name, attr_value)
