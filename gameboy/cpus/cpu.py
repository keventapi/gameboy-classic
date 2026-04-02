from .instruction_assembly import INSTRUCTIONS
from . import instructions_agregator as instr


class CPU:
    def __init__(self, mmu, timer):
        self.read_value = 0
        self.value = 0x00

        self.is_halted = False
        self.di_pending = False
        self.ei_pending = False
        self.ime = True

        self.instructions_attr = [self.not_implemented] * 256

        self.mmu = mmu
        self.timer = timer
        self.pc = 0x100

        self.registers_map = {
            0b000: "B", 0b001: "C",
            0b010: "D", 0b011: "E",
            0b100: "H", 0b101: "L",
            0b111: "A", 0b110: "HL"
        }

        self.registers = {"pc": 0, "sp": 0xFFFE,
                          "A": 0, "F": 0,
                          "B": 0, "C": 0,
                          "D": 0, "E": 0,
                          "H": 0, "L": 0}

        self.assert_instructions()
        self.handle_builder()
        self.print_opcode = False

    def assert_instructions(self):
        self.instructions = INSTRUCTIONS(self)

    def not_implemented(self, obj):
        print(f"opcode: {obj.current_opcode:02x}")
        exit()

    def handle_builder(self):
        for i in range(256):
            if hasattr(instr, f"op_{i:02x}"):
                self.instructions_attr[i] = getattr(instr, f"op_{i:02x}")

    def set_flags(self, Z, N, H, C):
        self.registers["F"] = (Z << 7) | (N << 6) | (H << 5) | (C << 4)
        self.registers["F"] &= 0xF0

    def fetch_16bit(self):
        return (self.fetch() | (self.fetch() << 8)) & 0xFFFF

    def check_instruction_interrupt(self):
        if self.di_pending:
            self.ime = False
            self.di_pending = False
        if self.ei_pending:
            self.ime = True
            self.ei_pending = False

    def reset_if(self, b):
        value = self.mmu.read(0xFF0F)
        new_value = (value & (~(1 << b))) | 0xE0
        self.mmu.write(0xFF0F, new_value)

    def call_isr(self):
        b = -1
        value_if = self.mmu.read(0xFF0F)
        value_ie = self.mmu.read(0xFFFF)
        for i in range(5):
            if ((value_if >> i) & 1) == 1 and ((value_ie >> i) & 1) != 0:
                b = i
                break
        if b != -1:
            self.ime = False
            addrs = 0x0040 + (b * 8)
            self.push16(self.registers["pc"])
            self.registers["pc"] = addrs
            self.reset_if(b)
            self.timer.tick(20)
            return 20
        self.timer.tick(4)
        return 4

    def ceck_if_ie(self):
        value_if = self.mmu.read(0xFF0F) & 0x1F
        value_ie = self.mmu.read(0xFFFF) & 0x1F
        return (value_if & value_ie & 0x1F) != 0


    def step(self):
        opcode = 0

        if self.ceck_if_ie():
            if self.is_halted:
                self.is_halted = False
            if self.ime:
                return self.call_isr()

        if not self.is_halted:
            opcode = self.fetch()
            callback = self.decode(opcode)
            if self.ei_pending or self.di_pending:
                ticks = callback(self)
                self.check_instruction_interrupt()
            else:
                ticks = callback(self)
        else:
            self.timer.tick(4)
            ticks = 4
        if self.print_opcode:
            print(f"opcode: {opcode:02x}")
        return ticks

    def push8(self, value):
        self.registers["sp"] -= 1
        self.registers["sp"] &= 0xFFFF
        self.mmu.write(self.registers["sp"], value & 0xFF)

    def push16(self, value):
        high = (value >> 8) & 0xFF
        self.push8(high)
        low = value & 0xFF
        self.push8(low)

    def pull8(self):
        value = self.mmu.read(self.registers["sp"]) & 0xFF
        self.registers["sp"] += 1
        self.registers["sp"] &= 0xFFFF
        return value

    def pull16(self):
        low = self.pull8()
        high = self.pull8()
        return ((high << 8) | low) & 0xFFFF

    def fetch(self):
        pc = self.registers["pc"]
        opcode = self.mmu.read(pc) & 0xFF
        self.registers["pc"] += 1
        return opcode

    def decode(self, opcode):
        instruction = self.instructions_attr[opcode]
        return instruction
