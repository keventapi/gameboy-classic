from .logical_operand.and_n import AND_N
from .logical_operand.cp_n import CP_N
from .logical_operand.dec_n import DEC_N
from .logical_operand.dec_nn import DEC_NN
from .logical_operand.inc_n import INC_N
from .logical_operand.inc_nn import INC_NN
from .logical_operand.or_n import OR_N
from .logical_operand.xor_n import XOR_N


class ALU:
    def __init__(self, cpu):
        self.and_n = AND_N(cpu)
        self.cp_n = CP_N(cpu)
        self.dec_n = DEC_N(cpu)
        self.dec_nn = DEC_NN(cpu)
        self.inc_n = INC_N(cpu)
        self.inc_nn = INC_NN(cpu)
        self.or_n = OR_N(cpu)
        self.xor_n = XOR_N(cpu)

        instances = [
            self.and_n,
            self.cp_n,
            self.dec_n,
            self.dec_nn,
            self.inc_n,
            self.inc_nn,
            self.or_n,
            self.xor_n
        ]

        for instance in instances:
            for attr_name in dir(instance):
                if not attr_name.startswith("__"):
                    attr_value = getattr(instance, attr_name)
                    if callable(attr_value):
                        setattr(self, attr_name, attr_value)
        
