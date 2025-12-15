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

    def debug(self, opcode, last_state):
        print("-"*64)
        print(f"opcode: {opcode:02x}")
        print(f"A: \n before: {bin(last_state["A"])} \n after {bin(self.registers["A"])}")
        print(f"B: \n before: {bin(last_state["B"])} \n after {bin(self.registers["B"])}")
        print(f"C: \n before: {bin(last_state["C"])} \n after {bin(self.registers["C"])}")
        print(f"D: \n before: {bin(last_state["D"])} \n after {bin(self.registers["D"])}")
        print(f"E: \n before: {bin(last_state["E"])} \n after {bin(self.registers["E"])}")
        print(f"F: \n before: {bin(last_state["F"])} \n after {bin(self.registers["F"])}")
        print(f"sp: \n before: {last_state["sp"]} \n after {self.registers["sp"]}")
        print("-"*64)

    def step(self):
        last_state = self.registers.copy()
        if not self.is_halted:
            if self.timer.interrupt_enabled and self.timer.interrupt:
                # chama interrupt service
                return
            opcode = self.fetch()
            callback = self.decode(opcode)
            if any([self.ei_pending, self.di_pending]):
                callback()
                self.check_instruction_interrupt()
            else:
                callback()
        else:
            self.timer.tick(1)
        self.debug(opcode, last_state)

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
