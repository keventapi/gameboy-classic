from .stack.pop import POP
from .stack.push import PUSH


class STACK:
    def __init__(self, cpu):
        self.pop = POP(cpu)
        self.push = PUSH(cpu)

        instances = [
            self.push,
            self.pop
        ]

        for instance in instances:
            for attr_name in dir(instance):
                if not attr_name.startswith("__"):
                    attr_value = getattr(instance, attr_name)
                    if callable(attr_value):
                        setattr(self, attr_name, attr_value)

