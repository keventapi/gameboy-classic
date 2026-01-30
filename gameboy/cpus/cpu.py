from .instruction_assembly import INSTRUCTIONS
from . import instructions_agregator as instr

class CPU:
    def __init__(self, mmu, timer):
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

        self.registers = {"pc": 0x100, "sp": 0xFFFE,
                          "A": 0, "F": 0,
                          "B": 0, "C": 0,
                          "D": 0, "E": 0,
                          "H": 0, "L": 0}

        self.limit = 0xFFFE
        self.assert_instructions()
        self.handle_builder()

    def assert_instructions(self):
        self.instructions = INSTRUCTIONS(self)

    def not_implemented(self):
        raise NotImplementedError("papapapa por enquanto")

    def handle_builder(self):
        for i in range(256):
            if hasattr(instr, f"op_{i:02x}"):
                self.instructions_attr[i] = getattr(instr, f"op_{i:02x}")

    def set_flags(self, Z, N, H, C):
        self.registers["F"] = (Z << 7) | (N << 6) | (H << 5) | (C << 4)
        self.registers["F"] &= 0xF0

    def fetch_16bit(self):
        return self.fetch() | (self.fetch() << 8)

    def check_instruction_interrupt(self):
        if self.di_pending:
            self.ime = False
            self.di_pending = False
        if self.ei_pending:
            self.ime = True
            self.ei_pending = False

    def debug(self, opcode, last_state):
        print("-"*64)
        print(f"opcode: {opcode:02x}")
        print(f"A: \n before: 0x{last_state["A"]:02x} \n after 0x{self.registers["A"]:02x}")
        print(f"B: \n before: 0x{last_state["B"]:02x} \n after 0x{self.registers["B"]:02x}")
        print(f"C: \n before: 0x{last_state["C"]:02x} \n after 0x{self.registers["C"]:02x}")
        print(f"D: \n before: 0x{last_state["D"]:02x} \n after 0x{self.registers["D"]:02x}")
        print(f"E: \n before: 0x{last_state["E"]:02x} \n after 0x{self.registers["E"]:02x}")
        print(f"F: \n before: {last_state["F"]:08b} \n after {self.registers["F"]:08b}")
        print(f"sp: \n before: {last_state["sp"]} \n after {self.registers["sp"]}")
        print("-"*64)

    def reset_if(self, b):
        value = self.mmu.read(0xFF0F)
        new_value = value & (~(1 << b))
        self.mmu.write(0xFF0F, new_value)

    def call_isr(self):
        b = -1
        value_if = self.mmu.read(0xFF0F)
        value_ie = self.mmu.read(0xFFFF)
        for i in range(5):
            if ((value_if >> i) & 1) & 1 and ((value_ie >> i) & 1) != 0:
                b = i
                break
        if b != -1:
            self.ime = False
            addrs = 0x0040 + (b * 8)
            high = (self.registers["pc"] >> 8) & 0xFF
            low = self.registers["pc"] & 0xFF
            self.push8(high)
            self.push8(low)
            self.registers["pc"] = addrs
            self.reset_if(b)
            self.timer.tick(20)
            return 20
        return 4

    def ceck_if_ie(self):
        value_if = self.mmu.read(0xFF0F) & 0x1F
        value_ie = self.mmu.read(0xFFFF) & 0x1F
        #print(f"if: {value_if:08b} \n ie:{value_ie:08b} \n ime: {self.ime}")
        return (value_if & value_ie & 0x1F) != 0

    def step(self):
        last_state = self.registers.copy()

        if self.ceck_if_ie():
            self.is_halted = False
            if self.ime:
                self.call_isr()
                return

        if not self.is_halted:
            opcode = self.fetch()
            callback = self.decode(opcode)
            if any([self.ei_pending, self.di_pending]):
                ticks = callback(self)
                self.check_instruction_interrupt()
            else:
                ticks = callback(self)
        else:
            self.timer.tick(4)
            ticks = 4
        #self.debug(opcode, last_state)

        

        return ticks

    def push8(self, value):
        self.registers["sp"] -= 1
        self.registers["sp"] &= 0xFFFF
        self.mmu.write(self.registers["sp"], value)

    def pull8(self):
        value = self.mmu.read(self.registers["sp"])
        self.registers["sp"] += 1
        self.registers["sp"] &= 0xFFFF
        return value

    def fetch(self):
        pc = self.registers["pc"]
        opcode = self.mmu.read(pc) & 0xFF
        self.registers["pc"] += 1
        return opcode

    def decode(self, opcode):
        instruction = self.instructions_attr[opcode]
        return instruction
