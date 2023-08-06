# This script contain util will help you, good luck!
# Author:
#     Albert Dongz
# History:
#     2020.4.17 First Release
# Dependencies:
#     PyTorch
# Attention:
#     1. Nothing

import os
import torch
import logging
import datetime
import torch.nn as nn


def lognow(path="./checkpoints/"):
    """This function set up logging.

    Keyword Arguments:
        path {str} -- log save path (default: {"./checkpoints/"})

    Returns:
        str -- log absolute path, contain time and param path.
    """
    # get current time and create log dir
    now = datetime.datetime.now().strftime('%Y-%m-%d--%H-%M-%S')
    log_path = os.path.normpath(path + '/' + now)
    if not os.path.exists(log_path):
        os.makedirs(log_path)

    # setting up logging
    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.INFO)
    handler = logging.FileHandler(log_path + "/log.txt")
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.addHandler(console)
    logger.info('Start logging.')
    return logger, log_path


def float2fixed_del(data, bw, fl):
    """turn torch.Tensor to fixed Tensor.

    Args:
        data (torch.Tensor): torch.Tensor
        bw (int): bit width of quantization
        fl (int): fraction length of data, from left to right, ignore sign bit.

    Returns:
        torch.Tensor: fixed Tensor
    """
    unit = 2.0**(-bw + 1 + fl)
    fixed_data = torch.clamp(torch.round(data / unit) * unit,
                             min=-2**fl + unit,
                             max=+2**fl - unit)
    return fixed_data


def float2fixed(data, bw, fl):
    """turn torch.Tensor to fixed Tensor.

    Args:
        data (torch.Tensor): torch.Tensor
        bw (int): bit width of quantization.
        fl (int): fraction length.

    Returns:
        torch.Tensor: fixed Tensor
    """
    unit = 2.0**(-fl)
    fixed_data = torch.clamp(torch.round(data / unit) * unit,
                             min=-2**(bw - 1 - fl) + unit,
                             max=+2**(bw - 1 - fl) - unit)
    return fixed_data


def bn2scale(model_state, layer_name):
    """
    description:
        将指定bn层的函数改成scale层的形式，解决由PyTorch BN层的四个参数数量级不一致导致的在量化时的精度
        较大损失，返回值为包含处理好的bn层的模型参数。
        PyTorch BN数学公式：out = gamma * (x - mean)/sqrt(var) + beta
        Caffe Scale 数学公式：out = alpha * x + beta
        通过使得 new_gamma = gamma / sqrt(var),
               new_beta = beta - gamma * mean / sqrt(var)
               new_mean = 0, new_var = 1 来完成变换。P.S. 为了利用原来的BN的结构来实现scale。
    :parameter
        model_state:
            未处理过的模型参数
        layer_name: str
            bn层的参数存储名字的layername，如cnn.batchnorm0，如果全名为cnn.batchnorm0.weight
    :return:
        model_state:
            处理过的模型参数
    """
    # 从未处理的模型中获取bn层的四个参数
    weight = model_state.get(layer_name + ".weight")
    bias = model_state.get(layer_name + ".bias")
    mean = model_state.get(layer_name + ".running_mean")
    var = model_state.get(layer_name + ".running_var")
    # 计算标准差，即sqrt(var) => std
    std = torch.sqrt(var)
    # 计算新的值
    a = weight / std
    b = bias - weight * mean / std
    e = torch.zeros(mean.shape).to(torch.int32)
    s = torch.ones(var.shape).to(torch.int32)
    # 保存参数到模型
    model_state[layer_name + ".weight"] = a
    model_state[layer_name + ".bias"] = b
    model_state[layer_name + ".running_mean"] = e
    model_state[layer_name + ".running_var"] = s


def bn2scale(module):
    """
    description:
        将指定bn层的函数改成scale层的形式，解决由PyTorch BN层的四个参数数量级不一致导致的在量化时的精度
        较大损失，返回值为包含处理好的bn层的模型参数。
        PyTorch BN数学公式：out = gamma * (x - mean)/sqrt(var) + beta
        Caffe Scale 数学公式：out = alpha * x + beta
        通过使得 new_gamma = gamma / sqrt(var),
               new_beta = beta - gamma * mean / sqrt(var)
               new_mean = 0, new_var = 1 来完成变换。P.S. 为了利用原来的BN的结构来实现scale。
    :parameter
        model_state:
            未处理过的模型参数
        layer_name: str
            bn层的参数存储名字的layername，如cnn.batchnorm0，如果全名为cnn.batchnorm0.weight
    :return:
        model_state:
            处理过的模型参数
    """
    # 从未处理的module中获取bn层的四个参数
    weight = module.weight
    bias = module.bias
    mean = module.running_mean
    var = module.running_var
    # 计算标准差，即sqrt(var) => std
    std = torch.sqrt(var)
    # 计算新的值
    new_weight = weight / std
    new_bias = bias - weight * mean / std
    new_mean = torch.zeros(mean.shape)
    new_var = torch.ones(var.shape)
    # 保存参数到模型
    module.weight = nn.Parameter(new_weight)
    module.bias = nn.Parameter(new_bias)
    module.running_mean = new_mean
    module.running_var = new_var


def transfer_bn2scale(net):
    """Auto transfer BatchNorm to Scale

    Arguments:
        net {torch.nn.Module} -- net need be processed
        state {OrderDict} -- checkpoint of net

    Returns:
        net, state -- processed net and state
    """
    print("Start transfer BatchNorm to Scale")
    for name, module in net.named_modules():
        if isinstance(module, nn.BatchNorm2d):
            bn2scale(module)
    print("Transfer done.")


# Ref: https://zhuanlan.zhihu.com/p/49329030
# fuse Conv-BN & Deconv-BN
def fuse_module(m):
    class DummyModule(nn.Module):
        def __init__(self):
            super().__init__()

        def forward(self, x):
            return x

    def fuse(conv, bn):
        w = conv.weight
        mean = bn.running_mean
        var_sqrt = torch.sqrt(bn.running_var + bn.eps)

        beta = bn.weight
        gamma = bn.bias

        if conv.bias is not None:
            b = conv.bias
        else:
            b = mean.new_zeros(mean.shape)

        w = w * (beta / var_sqrt).reshape([conv.out_channels, 1, 1, 1])
        b = (b - mean) / var_sqrt * beta + gamma
        if isinstance(conv, nn.Conv2d):
            fused_conv = nn.Conv2d(conv.in_channels,
                                   conv.out_channels,
                                   conv.kernel_size,
                                   conv.stride,
                                   conv.padding,
                                   bias=True)
        else:
            fused_conv = nn.ConvTranspose2d(conv.in_channels,
                                            conv.out_channels,
                                            conv.kernel_size,
                                            conv.stride,
                                            conv.padding,
                                            bias=True)
        fused_conv.weight = nn.Parameter(w)
        fused_conv.bias = nn.Parameter(b)
        return fused_conv

    children = list(m.named_children())
    c = None
    cn = None

    for name, child in children:
        if isinstance(child, nn.BatchNorm2d):
            bc = fuse(c, child)
            m._modules[cn] = bc
            m._modules[name] = DummyModule()
            c = None
        elif isinstance(child, (nn.Conv2d, nn.ConvTranspose2d)):
            c = child
            cn = name
        else:
            fuse_module(child)
