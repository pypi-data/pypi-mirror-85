# This script contain functions help quantization
# Author:
#     Albert Dongz
# History:
#     2020.7.16 First Release
# Dependencies:
#     PyTorch
# Attention:
#     1. Nothing

import json

from tqdm import tqdm
from .operators import *
from .utils import *

# global var
quant_layer_list = []


def quant_ops_switch(name, module, bit_width, logger):
    """quantization operators switch func

    Args:
        name (str): module name
        module (nn.module): module object
        bit_width (int): quantize bit width
        logger (logger): logger for logging

    Returns:
        QuantClass: specific QuantClass for specific layer type
    """
    if isinstance(module, TorchFuncTuple):
        quant_layer = QuantTorchFunc(name, module, bit_width, logger)
    elif isinstance(module, (nn.Conv1d, nn.Conv2d, nn.Conv3d)):
        quant_layer = QuantConv(name, module, bit_width, logger)
    elif isinstance(module, nn.Linear):
        quant_layer = QuantLinear(name, module, bit_width, logger)
    # elif isinstance(module, (nn.BatchNorm1d, nn.BatchNorm2d, nn.BatchNorm3d)):
    #     quant_layer = QuantBatchNorm(name, module, bit_width, logger)
    elif isinstance(module, (nn.LayerNorm)):
        quant_layer = QuantLayerNorm(name, module, bit_width, logger)
    elif isinstance(module, nn.ReLU):
        quant_layer = QuantRelu(name, module, bit_width, logger)
    elif isinstance(module, nn.PReLU):
        quant_layer = QuantPRelu(name, module, bit_width, logger)
    elif isinstance(module, nn.LeakyReLU):
        quant_layer = QuantLRelu(name, module, bit_width, logger)
    elif isinstance(
            module,
        (nn.AdaptiveAvgPool1d, nn.AdaptiveAvgPool2d, nn.AdaptiveAvgPool3d)):
        quant_layer = QuantAdaptiveAvgPool(name, module, bit_width, logger)
    elif isinstance(module, nn.Upsample):
        quant_layer = QuantUpsample(name, module, bit_width, logger)
    elif isinstance(
            module,
        (nn.ConvTranspose1d, nn.ConvTranspose2d, nn.ConvTranspose3d)):
        quant_layer = QuantConvTranspose(name, module, bit_width, logger)
    else:
        quant_layer = None

    return quant_layer


def quantize(model,
             bit_width,
             data_loader,
             path,
             fuse_norm=True,
             is_debug=False,
             to_onnx=False):
    """quantize main func

    Args:
        model (nn.module): Pytorch model
        bit_width (int): Quantize bit width
        data_loader (Dataloader): model data_loader
        path (str): log path for saving quant params, quantized model, log file, etc.
        fuse_norm (bool, optional): if True, fuse normalization module in model. Defaults to True.
        is_debug (bool, optional): if True, turn on debug mode and generate figure of layer stats. Defaults to False.
    """
    # init abstract log path and logger
    logger, log_path = lognow(path)
    # fuse normalization layer
    if fuse_norm:
        fuse_module(model)
    # if debug
    if is_debug:
        logger.warning("Debug Mode:")
        # make figs log dirs
        log_figs_path = os.path.normpath(log_path + '/figs/')
        os.makedirs(log_figs_path)
        logger.warning("Init quant_layer_list.")
        logger.warning("Draw histograms figure of input.")
        quant_input = QuantInput("input", None, bit_width, logger, log_path,
                                 data_loader)
        quant_input.debug_input()
        logger.warning("Draw histograms figure of weight.")
        logger.warning("Add get_activation hook.")
        for name, module in model.named_modules():
            # if bool(list(module.children())) is False, then module can't be container
            if not list(module.children()):
                quant_layer = QuantDebug(name, module, bit_width, logger,
                                         log_path)
                quant_layer_list.append(quant_layer)
                quant_layer.quantize_weight()
                quant_layer.register_get_activation_hook()

        logger.warning("Init boundary.")
        for i, metadata in enumerate(tqdm(data_loader)):
            image = metadata[0].cuda()
            model(image)
            for layer in quant_layer_list:
                layer.init_boundary()

        logger.warning("Init histograms of activation.")
        for i, metadata in enumerate(tqdm(data_loader)):
            image = metadata[0].cuda()
            model(image)
            for layer in quant_layer_list:
                layer.init_histograms()

        logger.warning("Draw histograms figure of activation.")
        for layer in quant_layer_list:
            layer.quantize_activation()
    else:
        logger.info("Init quant_layer_list.")
        logger.info("Quantize the input.")
        quant_input = QuantInput("input", None, bit_width, logger, log_path,
                                 data_loader)
        quant_input.quantize_input()
        logger.info("Add get_activation hook.")
        logger.info("Quantize the weight.")
        for name, module in model.named_modules():
            quant_layer = quant_ops_switch(name, module, bit_width, logger)
            if quant_layer:
                quant_layer_list.append(quant_layer)
                quant_layer.quantize_weight()
                quant_layer.register_get_activation_hook()
        # save quantized weight
        torch.save(model.state_dict(), log_path + '/quantized.pth')

        logger.info("Collect histograms of activations.")
        for i, metadata in enumerate(tqdm(data_loader)):
            image = metadata[0].cuda()
            model(image)
            for layer in quant_layer_list:
                layer.init_histograms()

        logger.info("Quantize the activation.")
        for layer in quant_layer_list:
            layer.quantize_activation()

        logger.info("Turn on eval mode.")
        for layer in quant_layer_list:
            layer.eval_mode()

        # insert quant_input to quant_layer_list
        quant_layer_list.insert(0, quant_input)

        # save quant_params
        fl_dict = {}
        for layer in quant_layer_list:
            fl_dict[layer.name] = {}
            fl_dict[layer.name]['weight_fl'] = int(layer.weight_fl)
            fl_dict[layer.name]['activation_fl'] = int(layer.activation_fl)
        with open(log_path + '/quant_params.json', 'w+') as file:
            json.dump(fl_dict, file)


def quantize_parallel(net, bit_width, data_loader, logger, log_path):
    logger.info("Init quant_layer_list.")
    logger.info("Add get_activation hook.")
    logger.info("Quantize the weight.")
    for name, module in net.named_modules():
        quant_layer = op_switch(name, module, bit_width)
        if quant_layer:
            quant_layer_list.append(quant_layer)
    pool = Pool()
    pool.map(lambda x: x.quantize_weight(), quant_layer_list)
    pool.map(lambda x: x.register_get_activation_hook(), quant_layer_list)
    pool.close()
    pool.join()
    torch.save(net.state_dict(), log_path + '/quantized.pth')

    logger.debug("Debug Mode: init boundary")
    if True:
        for i, (image, index) in enumerate(tqdm(data_loader)):
            image = image.cuda()
            net(image)
            pool = Pool()
            pool.map(lambda x: x.init_boundary(), quant_layer_list)
            pool.close()
            pool.join()

    logger.info("Collect histograms of activations.")
    for i, (image, index) in enumerate(tqdm(data_loader)):
        image = image.cuda()
        net(image)
        pool = Pool(12)
        pool.map(lambda x: x.init_histograms(), quant_layer_list)
        pool.close()
        pool.join()

    logger.info("Quantize the activation.")
    pool = Pool()
    pool.map(lambda x: x.quantize_activation(), quant_layer_list)
    pool.close()
    pool.join()
