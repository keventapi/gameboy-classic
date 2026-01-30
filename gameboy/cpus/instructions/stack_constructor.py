from .stack.pop import POP
from .stack.push import PUSH


class STACK:
    def __init__(self, cpu):
        self.pop = POP(cpu)
        self.push = PUSH(cpu)


