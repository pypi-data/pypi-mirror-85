# This script contain implentation of operators.
# Author:
#     Albert Dongz
# History:
#     2020.7.16 First Release
# Dependencies:
#     PyTorch
# Attention:
#     1. Nothing
import numpy as np

from .debug import QuantDebug
from .quant_base import *


class QuantInput(QuantDebug):
    def __init__(self, name, module, bit_width, logger, log_path, data_loader):
        super().__init__(name, module, bit_width, logger, log_path)
        self.weight_fl = -1
        self.data_loader = data_loader

    def debug_input(self):
        for index, metadata in enumerate(self.data_loader):
            # self.activation here is input.
            self.activation = metadata[0].flatten().numpy()
            self.init_boundary()

        for index, metadata in enumerate(self.data_loader):
            self.activation = metadata[0].flatten().numpy()
            self.init_histograms()

        self.quantize_activation()

    def quantize_input(self):
        for index, metadata in enumerate(self.data_loader):
            data = metadata[0].flatten().numpy()
            hist, hist_edge = np.histogram(data,
                                           bins=self.bins_num,
                                           range=(-1 * self.activation_max,
                                                  self.activation_max))
            self.activation_distribution += hist
        self.activation_fl, self.activation_kld = kld_based_dynamics_double(
            self.activation_distribution, self.bit_width)