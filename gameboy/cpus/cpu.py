from instructionmixin import InstructionMixin
class Cpu(InstructionMixin):
    def __init__(self, working_ram, cartridge):
        """
        :param working_ram: Objeto criado a partir da RAM (em gameboy/memory/ram.py)
        :param cartridge: Objeto criado a partir do cartridge (em gameboy/memory/cartridge.py)

        pc → Endereço inicial fiel ao hardware, onde o program counter começa (0x0100)
        registers_map → Mapeamento mais intuitivo dos registradores, facilitando o debugging
        registers → Estrutura que armazena os registradores reais; PC e SP são os únicos de 16 bits,
                     enquanto os de 8 bits podem formar pares para representar valores de 16 bits
        limit → Limite superior da pilha (stack)
        """


        self.memory = working_ram
        self.cartridge = cartridge

        self.pc = 0x100

        # SP, PC e F não são acessíveis diretamente via opcode;
        # são manipulados apenas durante a execução das instruções.
        self.registers_map = {
            0b000: "B", 0b001: "C",
            0b010: "D", 0b011: "E",
            0b100: "H", 0b101: "L",
            0b111: "A", 0b110: "HL"
        }

        self.registers = {"pc": 0x100, "sp": 0xFFFE,
                          "A": 0, "F": 0,
                          "B": 0,"C": 0,
                          "D": 0, "E": 0,
                          "H": 0, "L": 0}

        self.limit = 0xFFFE

    def step(self):
        """
        Executa um ciclo completo de CPU:
        1. Busca o opcode atual na memória.
        2. Decodifica o opcode em uma tupla contendo os parâmetros necessários.
        3. Executa a instrução correspondente.

        :return: Valor retornado pela instrução (se houver). Caso contrário, retorna -1.
        """
        opcode = self.fetch()
        decoded = self.decode(opcode)
        value = self.execute(decoded)
        if value is None:
            return -1
        return value

    def push8(self, value):
        """
        Empilha um valor de 8 bits na memória.

        O Stack Pointer (SP) é decrementado antes da escrita,
        conforme o comportamento original da CPU do Game Boy.

        :param value: Valor de 8 bits a ser colocado na pilha.
        :raises Exception: Caso o endereço resultante ultrapasse os limites válidos de stack (overflow).
        """
        if 0xC000 <= self.registers["sp"] -1 <= self.limit:
            self.registers["sp"] -= 1
            self.memory.write(self.registers["sp"], value)
        else:
            raise Exception("stack overflow")

    def pull8(self):
        """
        Desempilha um valor de 8 bits do topo da pilha.

        O valor é lido no endereço atual apontado por SP e,
        em seguida, o Stack Pointer (SP) é incrementado,
        restaurando o comportamento original da CPU do Game Boy.

        :return: Valor de 8 bits desempilhado.
        :raises Exception: Caso o endereço exceda os limites válidos da stack (underflow).
        """
        if 0xC000 <= self.registers["sp"]+1 <= self.limit:
            value = self.memory.read(self.registers["sp"])
            self.registers["sp"] += 1
            return value
        raise Exception("stack underflow")

    def fetch(self):
        """
        Busca o próximo opcode na memória apontada pelo Program Counter (PC).

        O valor de 8 bits é lido da memória e o PC é incrementado em 1,
        simulando o comportamento real da CPU do Game Boy.

        :return: Opcode de 8 bits lido da memória.
        """
        pc = self.registers["pc"]
        opcode = self.memory.read(pc) & 0xFF
        self.registers["pc"] += 1
        return opcode

    def decode(self, opcode):
        """
        Decodifica o opcode atual e identifica a instrução correspondente.

        Verifica se o opcode pertence à faixa de instruções conhecidas da CPU.
        Caso pertença, extrai os parâmetros necessários (como registradores)
        e retorna as informações para a próxima etapa de execução.

        :param opcode: Opcode retornado pelo método fetch().
        :return: Tupla contendo o nome da instrução e seus parâmetros.
        """

        #LD n  nn
        if opcode in (0x06,0x0E, 0x16, 0x1E, 0x26, 0x2E):
            n = (opcode >> 3) & 0b111
            return "LD n nn", self.registers_map[n]

        #ld r1 r2 8bits
        elif (opcode >> 6) == 0b01:
            n1 = (opcode >> 3) & 0b111
            n2 = opcode & 0b111
            return "LD r1 r2", self.registers_map[n1], self.registers_map[n2]

        elif opcode in (0x0A, 0x1A, 0xFA, 0x3E):
            ld_exception_map = {
                (0x0A & 0b111): "BC",
                (0x1A & 0b111): "DE",
                (0xFA & 0b111): "nn",
                (0x3E & 0b111): "#",
                **self.registers_map
            }
            dest = (opcode >> 3) & 0b111
            src = opcode & 0b111
            return "LD r1 r2", ld_exception_map[dest], ld_exception_map[src]

        elif opcode == 0xF2:
            return "LD A (C)"
        elif opcode == 0xE2:
            return "LD (C) A"

    def execute(self, decoded):
        """
        Executa a instrução decodificada e aplica seus efeitos sobre os registradores.

        Este método representa a etapa final do ciclo de instrução,
        realizando a operação indicada pelo opcode previamente decodificado.

        :param decoded: Tupla retornada pelo método decode(), contendo a instrução e seus parâmetros.
        :return: None, exceto se a instrução possuir valor de retorno explícito.
        """
        if decoded[0] == "LD n nn":
            return self.ld_n_nn(decoded)

        elif decoded[0] == "LD r1 r2":
            return self.ld_r1_r2(decoded)

        elif decoded[0] in ("LD (C) A", "LD A (C)"):
            return self.ld_a_FF00_C(decoded)
