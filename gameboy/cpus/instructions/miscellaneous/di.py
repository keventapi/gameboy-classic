class DI:
    def __init__(self, cpu):
        self.cpu = cpu

    def instructions_di(self):
        instructions = {
            0xF3: lambda: self.execute_di(4)
        }
        return instructions

    def execute_di(self, ticks):
        self.cpu.ime = False
        self.cpu.timer.tick(ticks)
        return ticks
