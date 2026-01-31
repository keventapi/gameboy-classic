from .miscellaneous.ccf import CCF
from .miscellaneous.cpl import CPL
from .miscellaneous.daa import DAA
from .miscellaneous.di import DI
from .miscellaneous.ei import EI
from .miscellaneous.halt import HALT
from .miscellaneous.nop import NOP
from .miscellaneous.scf import SCF
from .miscellaneous.stop import STOP

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
        self.stop = STOP(cpu)

        instances = [
            self.ccf ,
            self.cpl ,
            self.daa ,
            self.scf ,
            self.di ,
            self.ei ,
            self.halt,
            self.nop ,
            self.stop
        ]

        for instance in instances:
            for attr_name in dir(instance):
                if not attr_name.startswith("__"):
                    attr_value = getattr(instance, attr_name)
                    if callable(attr_value):
                        setattr(self, attr_name, attr_value)


