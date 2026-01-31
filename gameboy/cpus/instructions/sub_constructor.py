from .sub.sub_a_n import SUB_A_N
from .sub.sbc_a_n import SBC_A_N


class SUB:
    def __init__(self, cpu):
        self.sub_a_n = SUB_A_N(cpu)
        self.sbc_a_n = SBC_A_N(cpu)

        instances = [
            self.sub_a_n,
            self.sbc_a_n
        ]

        for instance in instances:
            for attr_name in dir(instance):
                if not attr_name.startswith("__"):
                    attr_value = getattr(instance, attr_name)
                    if callable(attr_value):
                        setattr(self, attr_name, attr_value)
