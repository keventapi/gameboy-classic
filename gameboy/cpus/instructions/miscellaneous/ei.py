class EI:
    def __init__(self, cpu):
        self.cpu = cpu

    def instructions_ei(self):
        instructions = {
            0xFB: lambda: self.execute_ei(4)
        }
        return instructions

    def execute_ei(self, ticks):
        self.cpu.ei_pending = True
