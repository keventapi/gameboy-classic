from .add.add_a_n import ADD_A_N
from .add.adc_a_n import ADC_A_N
from .add.add_hl_n import ADD_HL_N
from .add.add_sp_n import ADD_SP_N


class ADD:
    def __init__(self, cpu):
        self.add_a_n = ADD_A_N(cpu)
        self.adc_a_n = ADC_A_N(cpu)
        self.add_hl_n = ADD_HL_N(cpu)
        self.add_sp_n = ADD_SP_N(cpu)

        instances = [
            self.adc_a_n,
            self.add_a_n,
            self.add_hl_n,
            self.add_sp_n,
        ]

        for instance in instances:
            for attr_name in dir(instance):
                if not attr_name.startswith("__"):
                    attr_value = getattr(instance, attr_name)
                    if callable(attr_value):
                        setattr(self, attr_name, attr_value)

    def get_add_instructions(self):
        instructions = {}
        updater = [self.add_a_n.add_a_n_instructions,
                   self.adc_a_n.adc_a_n_instructions,
                   self.add_hl_n.add_hl_n_instructions,
                   self.add_sp_n.instructions_add_sp_n]
        for u in updater:
            instructions.update(u())
        return instructions
