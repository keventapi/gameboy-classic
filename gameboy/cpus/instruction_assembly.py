from .instructions.add_constructor import ADD
from .instructions.ld_constructor import LD
from .instructions.stack_constructor import STACK
from .instructions.sub_constructor import SUB
from .instructions.alu_constructor import ALU
from .instructions.calls_constructor import CALL
from .instructions.cb_constructor import CB
from .instructions.jumps_constructor import JUMP
from .instructions.miscellaneous_constructor import MISCELLANEOUS
from .instructions.restarts_constructor import RESTART
from .instructions.returns_constructor import RETURN
from .instructions.shifts_constructor import SHIFTS


class INSTRUCTIONS:
    def __init__(self, cpu):
        self.add = ADD(cpu)
        self.ld = LD(cpu)
        self.stack = STACK(cpu)
        self.sub = SUB(cpu)
        self.alu = ALU(cpu)
        self.call = CALL(cpu)
        self.cb = CB(cpu)
        self.jump = JUMP(cpu)
        self.miscellaneous = MISCELLANEOUS(cpu)
        self.restart = RESTART(cpu)
        self.returns = RETURN(cpu)
        self.shifts = SHIFTS(cpu)
