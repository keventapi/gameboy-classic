class Cpu:
    def __init__(self, working_ram, cartridge):
        self.memory = working_ram
        self.cartridge = cartridge

        self.pc = 0x100

        self.registers_map = {
            0b000: "B", 0b001: "C",
            0b010: "D", 0b011: "E",
            0b100: "H", 0b101: "L",
            0b111: "A", 0b110: "HL"
        } #sp, pc e F não são acessaveis pelo opcode e sim por execução das funçoes

        self.registers = {"pc": 0x100, "sp": 0xFFFE,
                          "A": 0, "F": 0,
                          "B": 0,"C": 0,
                          "D": 0, "E": 0,
                          "H": 0, "L": 0}
        self.limit = 0xFFFE

    def step(self):
        opcode = self.fetch()
        decoded = self.decode(opcode)
        value = self.execute(decoded, opcode)
        if value is None:
            return -1
        return value

    def push8(self, value):
        if 0xC000 <= self.registers["sp"] -1 <= self.limit:
            self.registers["sp"] -= 1
            self.memory.write(self.registers["sp"], value)
        else:
            raise Exception("stack overflow")

    def pull8(self):
        if 0xC000 <= self.registers["sp"]+1 <= self.limit:
            value = self.memory.read(self.registers["sp"])
            self.registers["sp"] += 1
            return value
        raise Exception("stack underflow")

    def fetch(self):
        pc = self.registers["pc"]
        opcode = self.memory.read(pc) & 0xFF
        self.registers["pc"] += 1
        return opcode

    def decode(self, opcode):
        #LD n  nn
        if opcode in (0x06,0x0E, 0x16, 0x1E, 0x26, 0x2E):
            n = (opcode >> 3) & 0b111
            return "LD n nn", self.registers_map[n]



    def execute(self, decoded, opcode):
        if decoded[0] == "LD n nn":
            nn = self.fetch()
            self.registers[decoded[1]] = nn
            return