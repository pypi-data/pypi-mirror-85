import json
# This script contain func help generating a onnx-caffe index.
# Author:
#     Albert Dongz
# History:
#     2020.10.15 First Release
# Dependencies:
#     json
# Attention:
#     1. Nothing


def gen_index(json_file, onnx_model):
    """generate a onnx-caffe index

    Args:
        json_file (str): json file you want to save
        onnx_model (onnx_model): model load from onnx file
    """
    with open(json_file, 'w+') as f:
        index = list(
            map(
                lambda x: {
                    'operator': str(x.op_type),
                    'layer_num': int(list(x.output)[0]),
                    'param': list(x.input)
                }, list(onnx_model.graph.node)))
        json.dump(index, f)
