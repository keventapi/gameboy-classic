from .returns.ret import RET
from .returns.ret_cc import RET_CC


class RETURN:
    def __init__(self, cpu):
        self.ret = RET(cpu)
        self.ret_cc = RET_CC(cpu)


