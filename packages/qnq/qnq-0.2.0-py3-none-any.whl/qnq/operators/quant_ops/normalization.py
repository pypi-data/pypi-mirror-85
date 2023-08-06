# This script contain implentation of operators.
# Author:
#     Albert Dongz
# History:
#     2020.7.16 First Release
# Dependencies:
#     PyTorch
# Attention:
#     1. Nothing
import torch
import torch.nn as nn
import numpy as np
from ..quant_base import *


class QuantBatchNorm(QuantBase):
    def __init__(self, name, module, bit_width, logger):
        super().__init__(name, module, bit_width, logger)

    def quantize_weight(self):
        mean_data = self.module.running_mean.cpu().data.flatten()
        var_data = self.module.running_var.cpu().data.flatten()
        if self.module.weight is not None:
            weight_data = self.module.weight.cpu().data.flatten()
            bias_data = self.module.bias.cpu().data.flatten()
            data = torch.cat((weight_data, bias_data, mean_data, var_data),
                             0).numpy()
        else:
            data = torch.cat((mean_data, var_data), 0).numpy()

        # init kld
        hist, hist_edge = np.histogram(data,
                                       bins=self.bins_num,
                                       range=(-1 * self.activation_max,
                                              self.activation_max))
        min_kld_fl, _ = kld_based_dynamics_double(hist, self.bit_width)
        self.weight_fl = min_kld_fl
        if self.module.weight is not None:
            self.module.weight.data = float2fixed(self.module.weight,
                                                  self.bit_width,
                                                  self.weight_fl)
            self.module.bias.data = float2fixed(self.module.bias,
                                                self.bit_width, self.weight_fl)
        self.module.running_mean.data = float2fixed(self.module.running_mean,
                                                    self.bit_width,
                                                    self.weight_fl)
        self.module.running_var.data = float2fixed(self.module.running_var,
                                                   self.bit_width,
                                                   self.weight_fl)


class QuantLayerNorm(QuantBase):
    def __init__(self, name, module, bit_width, is_debug):
        super().__init__(name, module, bit_width, is_debug)
