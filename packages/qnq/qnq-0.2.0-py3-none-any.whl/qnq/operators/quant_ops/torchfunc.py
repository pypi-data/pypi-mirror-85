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
import numpy as np
from ..quant_base import QuantBase


class QuantTorchFunc(QuantBase):
    def __init__(self, name, module, bit_width, logger):
        super().__init__(name, module, bit_width, logger)
        self.activation_positive = False
        self.weight_fl = -1

    def quantize_weight(self):
        pass


# extra implentation
class QuantTorchCat(QuantBase):
    def __init__(self, name, module, bit_width, logger):
        super().__init__(name, module, bit_width, logger)
        self.activation_positive = False
        self.kld_sum = 0

    def quantize_weight(self):
        pass

    def quantize_activation(self):
        for name in self.module.layers:
            self.kld_sum += quant_layer_list[name].activation_kld
        self.activation_fl = np.argmin(kld_sum)