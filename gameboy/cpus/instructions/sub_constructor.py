from .sub.sub_a_n import SUB_A_N
from .sub.sbc_a_n import SBC_A_N


class SUB:
    def __init__(self, cpu):
        self.sub_a_n = SUB_A_N(cpu)
        self.sbc_a_n = SBC_A_N(cpu)

