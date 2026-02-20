class STOP:
    def __init__(self, cpu):
        self.cpu = cpu
        self.registers = self.cpu.registers

    def execute_stop(self, ticks):
        self.cpu.is_halted = True
        self.cpu.timer.ppu.disable_display()
        self.cpu.timer.tick(ticks)
        return ticks
