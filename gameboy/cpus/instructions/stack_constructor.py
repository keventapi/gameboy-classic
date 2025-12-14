from .stack.pop import POP
from .stack.push import PUSH


class STACK:
    def __init__(self, cpu):
        self.pop = POP(cpu)
        self.push = PUSH(cpu)

    def get_stack_instructions(self):
        instructions = {}
        updater = [self.pop.pop_instructions,
                   self.push.push_instructions]
        for u in updater:
            instructions.update(u())
        return instructions
