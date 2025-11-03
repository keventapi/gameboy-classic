class InstructionMixin:
    def ld_n_nn(self, decoded):
        nn = self.fetch()
        self.registers[decoded[1]] = nn
        return None

    def ld_r1_r2(self, decoded):
        if len(decoded[1]) > 1:
            if decoded[1] == "nn":
                nn = (self.fetch() << 8) | self.fetch()
                self.memory.write(nn, self.registers[decoded[2]])
                return None

            reg16 = (self.registers[decoded[1][0]] << 8) | self.registers[decoded[1][1]]
            self.memory.write(reg16, self.registers[decoded[2]])

        # caso r2 de 16 bits
        elif len(decoded[2]) > 1:
            if decoded[2] == "nn":
                nn = self.fetch() | (self.fetch() << 8)
                self.registers[decoded[1]] = nn
                return None

            reg16 = (self.registers[decoded[2][0]] << 8) | self.registers[decoded[2][1]]
            self.registers[decoded[1]] = self.memory.read(reg16)

        else:
            if decoded[2] == "#":
                n = self.fetch()
                self.registers[decoded[1]] = n
                return None

            self.registers[decoded[2]] = self.registers[decoded[1]]
        return None

    def ld_a_FF00_C(self, decoded):
        instruction = ("LD (C) A", "LD A (C)").index(decoded[0])
        if instruction == 0:
            self.registers["A"] = self.memory.read(0xFF00 + self.registers["C"])
        else:
            self.memory.write(0xFF00 + self.registers["C"], self.registers["A"])
    
    def ldd_x_yz(self, decoded):
        if decoded[0][6] != " ":
            r1 = decoded[4]
            r2 = decoded[5]
            yz = (self.registers[r1] << 8) | self.registers[r2]
            x = decoded[0][-1]
            self.memory.write(yz, self.registers[x])
        else:
            r1 = decoded[-2]
            r2 = decoded[-1]
            yz = (self.registers[r1] << 8) | self.registers[r2]
            x = decoded[4]
            self.registers[x] = self.memory.read(yz)        
        yz -= 1
        yz &= 0xFFFF
        self.registers[r1] = (yz >> 8) & 0xFF
        self.registers[r2] = yz & 0xFF
        return None
