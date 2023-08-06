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


class QuantDropout(QuantBase):
    def __init__(self, name, module, bit_width, logger):
        super().__init__(name, module, bit_width, logger)
        self.activation_positive = False

    def quantize_weight(self):
        pass
