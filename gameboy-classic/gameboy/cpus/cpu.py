from gameboy.cpus.instruction_assembly import Instructions


class Cpu:
    def __init__(self, mmu, timer):
        self.mmu = mmu
        self.timer = timer
        self.pc = 0x100
        self.instructions = Instructions(self)

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

    def step(self):
        opcode = self.fetch()
        callback = self.decode(opcode)
        callback()

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
            raise NotImplementedError("não foi implementado essa instrução")
        return instruction
