from .shifts.rla import RLA
from .shifts.rlca import RLCA
from .shifts.rra import RRA
from .shifts.rrca import RRCA


class SHIFTS:
    def __init__(self, cpu):
        self.rla = RLA(cpu)
        self.rlca = RLCA(cpu)
        self.rra = RRA(cpu)
        self.rrca = RRCA(cpu)

    def shift_instructions(self):
        instructions = {

        }
        updater = [
            self.rla.rla_instructions,
            self.rlca.rlca_instructions,
            self.rra.rra_instructions,
            self.rrca.rrca_instructions
        ]
        for u in updater:
            instructions.update(u())
        return instructions
