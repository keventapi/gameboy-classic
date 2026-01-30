from .restarts.rst_n import RST_N


class RESTART:
    def __init__(self, cpu):
        self.rst_n = RST_N(cpu)

