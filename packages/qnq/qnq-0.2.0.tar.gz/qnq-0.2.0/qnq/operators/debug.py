# This script contain implentation of operators.
# Author:
#     Albert Dongz
# History:
#     2020.7.16 First Release
# Dependencies:
#     PyTorch
# Attention:
#     1. Nothing
import os
import torch.nn
import numpy as np
import matplotlib.pyplot as plt

from .quant_base import QuantBase


class QuantDebug(QuantBase):
    def __init__(self, name, module, bit_width, logger, log_path):
        super().__init__(name, module, bit_width, logger)
        self.log_path = log_path
        self.real_bins = 254
        self.real_weight_max = 0.0
        self.real_weight_min = 0.0
        self.real_activation_max = 0.0
        self.real_activation_min = 0.0
        self.real_activation_distribution = np.zeros(self.real_bins)
        self.real_activation_distribution_edge = None

    def init_boundary(self):
        # init activation boundary
        max_val = np.max(self.activation)
        min_val = np.min(self.activation)
        self.real_activation_max = max(max_val, self.real_activation_max)
        self.real_activation_min = min(min_val, self.real_activation_min)

    def init_histograms(self):
        if self.activation_positive:
            real_hist, real_hist_edge = np.histogram(
                self.activation,
                bins=self.real_bins,
                # use 2**(1 - self.bit_width) not zero,
                # because relu's activation have so many zero values, about 50~90%.
                range=(2**(1 - self.bit_width),
                       min(2**(self.bit_width - 1), self.real_activation_max)))
        else:
            real_hist, real_hist_edge = np.histogram(
                self.activation,
                bins=self.real_bins,
                range=(max(-2**(self.bit_width - 1), self.real_activation_min),
                       min(2**(self.bit_width - 1), self.real_activation_max)))
        self.real_activation_distribution_edge = real_hist_edge
        self.real_activation_distribution += real_hist

    def quantize_weight(self):
        try:
            # init real boundary
            # module can do not have weight, eg. relu
            weight_data = self.module.weight.cpu().data.flatten().numpy()
            self.real_weight_max = np.max(weight_data)
            self.real_weight_min = np.min(weight_data)
            # fig
            plt.title(self.name + " real weight histogram")
            plt.hist(weight_data, bins=100, density=True)
            plt.savefig(
                os.path.normpath(self.log_path + '/figs/' + self.name +
                                 "_real_weight.png"))
            plt.clf()
        except:
            pass

    def quantize_activation(self):
        # fig
        self.real_activation_distribution /= sum(
            self.real_activation_distribution)
        plt.title(self.name + " real activation histogram")
        plt.bar(self.real_activation_distribution_edge[1:],
                self.real_activation_distribution)
        plt.savefig(
            os.path.normpath(self.log_path + '/figs/' + self.name +
                             "_real_activation.png"))
        plt.clf()
