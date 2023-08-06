# This script contain implentation of operators.
# Author:
#     Albert Dongz
# History:
#     2020.7.16 First Release
# Dependencies:
#     PyTorch
# Attention:
#     1. Nothing
import torch.nn
from ..quant_base import QuantBase


class QuantRelu(QuantBase):
    def __init__(self, name, module, bit_width, logger):
        super().__init__(name, module, bit_width, logger)
        self.activation_positive = True
        self.weight_fl = -1

    def quantize_weight(self):
        pass


class QuantLRelu(QuantBase):
    def __init__(self, name, module, bit_width, logger):
        super().__init__(name, module, bit_width, logger)
        self.activation_positive = False
        self.weight_fl = -1

    def quantize_weight(self):
        pass


class QuantPRelu(QuantBase):
    def __init__(self, name, module, bit_width, logger):
        super().__init__(name, module, bit_width, logger)
        self.activation_positive = False
        self.weight_fl = -1

    def quantize_weight(self):
        pass


class Quanttanh(QuantBase):
    def __init__(self, name, module, bit_width, logger):
        super().__init__(name, module, bit_width, logger)
        self.activation_positive = False
        self.weight_fl = -1

    def quantize_weight(self):
        pass