from .instruction_assembly import INSTRUCTIONS


class CPU:
    def __init__(self, mmu, timer):
        self.is_halted = False
        self.di_pending = False
        self.ei_pending = False
        self.mmu = mmu
        self.timer = timer
        self.pc = 0x100

        self.registers_map = {
            0b000: "B", 0b001: "C",
            0b010: "D", 0b011: "E",
            0b100: "H", 0b101: "L",
            0b111: "A", 0b110: "HL"
        }

        self.registers = {"pc": 0x100, "sp": 0xFFFE,
                          "A": 0, "F": 0,
                          "B": 0, "C": 0,
                          "D": 0, "E": 0,
                          "H": 0, "L": 0}

        self.limit = 0xFFFE
        self.assert_instructions()

    def assert_instructions(self):
        self.instructions = INSTRUCTIONS(self)

    def set_flags(self, Z, N, H, C):
        self.registers["F"] = (Z << 7) | (N << 6) | (H << 5) | (C << 4)
        self.registers["F"] &= 0xF0

    def fetch_16bit(self):
        return self.fetch() | (self.fetch() << 8)

    def check_instruction_interrupt(self):
        if self.di_pending:
            self.timer.interrupt_enabled = False
            self.di_pending = False
        if self.ei_pending:
            self.timer.interrupt_enabled = True
            self.ei_pending = False

    def step(self):
        if not self.is_halted:
            if self.timer.interrupt_enabled and self.timer.interrupt:
                # chama interrupt service
                return
            opcode = self.fetch()
            self.debug(opcode)
            callback = self.decode(opcode)
            if any([self.ei_pending, self.di_pending]):
                callback()
                self.check_instruction_interrupt()
            else:
                callback()
        else:
            self.timer.tick(1)

    def push8(self, value):
        if 0xC000 <= self.registers["sp"] - 1 <= self.limit:
            self.registers["sp"] -= 1
            self.mmu.write(self.registers["sp"], value)
        else:
            raise Exception("stack overflow")

    def pull8(self):
        if 0xC000 <= self.registers["sp"] + 1 <= self.limit:
            value = self.mmu.read(self.registers["sp"])
            self.registers["sp"] += 1
            return value
        raise Exception("stack underflow")

    def fetch(self):
        pc = self.registers["pc"]
        opcode = self.mmu.read(pc) & 0xFF
        self.registers["pc"] += 1
        return opcode

    def decode(self, opcode):
        instruction = self.instructions.get_instruction(opcode)
        if not instruction:
            raise NotImplementedError(f"""INSTRUÇÃO AUSENTE!
                                      Opcode: 0x{opcode:02X}
                                      no Endereço:
                                        0x{self.registers["pc"]:04X}""")
        return instruction
