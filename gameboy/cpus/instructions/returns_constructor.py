from .returns.ret import RET
from .returns.ret_cc import RET_CC


class RETURN:
    def __init__(self, cpu):
        self.ret = RET(cpu)
        self.ret_cc = RET_CC(cpu)

        instances = [
            self.ret,
            self.ret_cc
        ]

        for instance in instances:
            for attr_name in dir(instance):
                if not attr_name.startswith("__"):
                    attr_value = getattr(instance, attr_name)
                    if callable(attr_value):
                        setattr(self, attr_name, attr_value)

