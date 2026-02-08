class EI:
    def __init__(self, cpu):
        self.cpu = cpu

    def instructions_ei(self):
        instructions = {
            0xFB: (self.execute_ei, (4))
        }
        return instructions

    def execute_ei(self, ticks):
        self.cpu.ei_pending = True
        print(self.cpu.registers["pc"], "acabou de executar ei")
        self.cpu.timer.tick(ticks)
        return ticks
