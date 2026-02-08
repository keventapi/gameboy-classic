from .cb_instructions.bit_b_r import BIT_B_R
from .cb_instructions.rc_n import RC_N
from .cb_instructions.res_b_r import RES_B_R
from .cb_instructions.rl_n import RL_N
from .cb_instructions.rlc_n import RLC_N
from .cb_instructions.rrc_n import RRC_N
from .cb_instructions.set_b_r import SET_B_R
from .cb_instructions.sla_n import SLA_N
from .cb_instructions.sra_n import SRA_N
from .cb_instructions.srl_n import SRL_N
from .cb_instructions.swap_n import SWAP_N


class CB:
    def __init__(self, cpu):
        self.cpu = cpu
        self.bit_b_r = BIT_B_R(cpu)
        self.rc_n = RC_N(cpu)
        self.res_b_r = RES_B_R(cpu)
        self.rl_n = RL_N(cpu)
        self.rlc_n = RLC_N(cpu)
        self.rrc_n = RRC_N(cpu)
        self.set_b_r = SET_B_R(cpu)
        self.sla_n = SLA_N(cpu)
        self.sra_n = SRA_N(cpu)
        self.srl_n = SRL_N(cpu)
        self.swap_n = SWAP_N(cpu)
        self.instructions = {}
        self.get_instruction_complement()

    def get_instruction_complement(self):
        updater = [self.bit_b_r.bit_b_r_instructions,
                   self.rc_n.rc_n_instructions,
                   self.res_b_r.res_b_r_intructions,
                   self.rl_n.rl_n_instructions,
                   self.rlc_n.rlc_n_instructions,
                   self.rrc_n.rrc_n_instructions,
                   self.set_b_r.set_b_r_intructions,
                   self.sla_n.sla_n_instructions,
                   self.sra_n.sra_n_instructions,
                   self.srl_n.srl_n_instructions,
                   self.swap_n.instructions_swap_n]
        for u in updater:
            self.instructions.update(u())

    def dispatch(self):
        opcode = self.cpu.fetch()
        callback = self.instructions[opcode]
        if len(callback) > 0:
            return callback[0](*callback[1])
        else:
            raise NotImplementedError("CB instruction missing")

    def get_cb_instructions(self):
        instructions = {
            0xcb: (self.dispatch, (4))
        }
        return instructions
