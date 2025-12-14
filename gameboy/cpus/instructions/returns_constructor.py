from .returns.ret import RET
from .returns.ret_cc import RET_CC


class RETURN:
    def __init__(self, cpu):
        self.ret = RET(cpu)
        self.ret_cc = RET_CC(cpu)

    def return_instructions(self):
        instructions = {

        }
        updater = [
            self.ret.ret_instructions,
            self.ret_cc.ret_cc_instructions
        ]
        for u in updater:
            instructions.update(u())
        return instructions
