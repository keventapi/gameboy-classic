from sub.sub_a_n import SUB_A_N
from sub.sbc_a_n import SBC_A_N


class SUB:
    def __init__(self, cpu):
        self.sub_a_n = SUB_A_N(cpu)
        self.sbc_a_n = SBC_A_N(cpu)

    def get_sub_instructions(self):
        instructions = {}
        updater = [self.sub_a_n.sub_a_n_instructions,
                   self.sbc_a_n.sbc_a_n_intructions]
        for u in updater:
            instructions.update(u())
        return instructions
