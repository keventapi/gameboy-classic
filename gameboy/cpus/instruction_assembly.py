from .instructions.add_constructor import ADD
from .instructions.ld_constructor import LD
from .instructions.stack_constructor import STACK
from .instructions.sub_constructor import SUB
from .instructions.alu_constructor import ALU
from .instructions.calls_constructor import CALL
from .instructions.cb_constructor import CB
from .instructions.jumps_constructor import JUMP
from .instructions.miscellaneous_constructor import MISCELLANEOUS
from .instructions.restarts_constructor import RESTART
from .instructions.returns_constructor import RETURN
from .instructions.shifts_constructor import SHIFTS


class INSTRUCTIONS:
    def __init__(self, cpu):
        self.add = ADD(cpu)
        self.ld = LD(cpu)
        self.stack = STACK(cpu)
        self.sub = SUB(cpu)
        self.alu = ALU(cpu)
        self.call = CALL(cpu)
        self.cb = CB(cpu)
        self.jump = JUMP(cpu)
        self.miscellaneous = MISCELLANEOUS(cpu)
        self.restart = RESTART(cpu)
        self.returns = RETURN(cpu)
        self.shifts = SHIFTS(cpu)
        self.instructions_map = {}
        self.update_instruction()

    def update_instruction(self):
        updater = [self.add.get_add_instructions,
                   self.ld.get_ld_instructions,
                   self.stack.get_stack_instructions,
                   self.sub.get_sub_instructions,
                   self.alu.get_alu_instructions,
                   self.call.get_call_instructions,
                   self.cb.get_cb_instructions,
                   self.jump.get_jump_instructions,
                   self.miscellaneous.miscellaneous_instructions,
                   self.restart.restart_instructions,
                   self.returns.return_instructions,
                   self.shifts.shift_instructions]
        for u in updater:
            self.instructions_map.update(u())
        self.create_instruction_list()

    def create_instruction_list(self):
        opcode = 0x00
        self.instructions_list = []
        while opcode <= 0xFF:
            instruction = self.instructions_map.get(opcode)
            self.instructions_list.append(instruction)
            opcode += 1
        print(self.instructions_list)

    def get_instruction(self, opcode):
        return self.instructions_list[opcode]
