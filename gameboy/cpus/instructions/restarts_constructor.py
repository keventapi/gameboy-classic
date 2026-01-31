from .restarts.rst_n import RST_N


class RESTART:
    def __init__(self, cpu):
        self.rst_n = RST_N(cpu)

        instances = [
            self.rst_n
        ]

        for instance in instances:
            for attr_name in dir(instance):
                if not attr_name.startswith("__"):
                    attr_value = getattr(instance, attr_name)
                    if callable(attr_value):
                        setattr(self, attr_name, attr_value)
