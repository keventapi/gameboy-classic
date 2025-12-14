from .miscellaneous.ccf import CCF
from .miscellaneous.cpl import CPL
from .miscellaneous.daa import DAA
from .miscellaneous.di import DI
from .miscellaneous.ei import EI
from .miscellaneous.halt import HALT
from .miscellaneous.nop import NOP
from .miscellaneous.scf import SCF


class MISCELLANEOUS:
    def __init__(self, cpu):
        self.ccf = CCF(cpu)
        self.cpl = CPL(cpu)
        self.daa = DAA(cpu)
        self.di = DI(cpu)
        self.ei = EI(cpu)
        self.halt = HALT(cpu)
        self.nop = NOP(cpu)
        self.scf = SCF(cpu)

    def miscellaneous_instructions(self):
        instructions = {

        }
        updater = [
            self.ccf.instructions_ccf,
            self.cpl.instructions_cpl,
            self.daa.daa_instructions,
            self.di.instructions_di,
            self.ei.instructions_ei,
            self.halt.instructions_halt,
            self.nop.intructions_nop,
            self.scf.instructions_scf
        ]
        for u in updater:
            instructions.update(u())
        return instructions
