from .restarts.rst_n import RST_N


class RESTART:
    def __init__(self, cpu):
        self.rst_n = RST_N(cpu)

    def restart_instructions(self):
        instructions = {

        }
        updater = [self.rst_n.rst_n_instructions]
        for u in updater:
            instructions.update(u())
        return instructions
