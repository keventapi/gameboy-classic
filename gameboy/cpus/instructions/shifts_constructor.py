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

        instances = [
            self.rla,
            self.rlca,
            self.rra,
            self.rrca
        ]

        for instance in instances:
            for attr_name in dir(instance):
                if not attr_name.startswith("__"):
                    attr_value = getattr(instance, attr_name)
                    if callable(attr_value):
                        setattr(self, attr_name, attr_value)
