from instructions.add_constructor import ADD
from instructions.ld_constructor import LD
from instructions.stack_constructor import STACK
from instructions.sub_constructor import SUB


class Instructions:
    def __init__(self, cpu):
        self.add = ADD(cpu)
        self.ld = LD(cpu)
        self.stack = STACK(cpu)
        self.sub = SUB(cpu)
        self.instructions_map = {}

    def update_instruction(self):
        updater = [self.add.get_add_instructions,
                   self.ld.get_ld_instructions,
                   self.stack.get_stack_instructions,
                   self.sub.get_sub_instructions]
        for u in updater:
            self.instructions_map.update(u())

    def get_instruction(self, opcode):
        return self.instructions_map.get(opcode)
