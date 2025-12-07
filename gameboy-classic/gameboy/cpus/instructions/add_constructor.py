from add.add_a_n import ADD_A_N
from add.adc_a_n import ADC_A_N


class ADD:
    def __init__(self, cpu):
        self.add_a_n = ADD_A_N(cpu)
        self.adc_a_n = ADC_A_N(cpu)

    def get_add_instructions(self):
        instructions = {}
        updater = [self.add_a_n.add_a_n_instructions,
                   self.adc_a_n.adc_a_n_instructions]
        for u in updater:
            instructions.update(u())
        return instructions
