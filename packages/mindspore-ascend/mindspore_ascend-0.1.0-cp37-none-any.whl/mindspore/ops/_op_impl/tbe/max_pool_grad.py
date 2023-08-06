# Copyright 2020 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================

"""MaxPoolGrad op"""
from mindspore.ops.op_info_register import op_info_register


@op_info_register("""{
    "op_name": "MaxPoolGrad",
    "imply_type": "TBE",
    "fusion_type": "OPAQUE",
    "async_flag": false,
    "binfile_name": "max_pool_grad.so",
    "compute_cost": 10,
    "kernel_name": "max_pool_grad",
    "partial_flag": true,
    "attr": [
        {
            "name": "ksize",
            "param_type": "required",
            "type": "listInt",
            "value": "all"
        },
        {
            "name": "strides",
            "param_type": "required",
            "type": "listInt",
            "value": "all"
        },
        {
            "name": "padding",
            "param_type": "required",
            "type": "str",
            "value": "all"
        }
    ],
    "inputs": [
        {
            "index": 0,
            "dtype": [
                "float16"
            ],
            "format": [
                "NC1HWC0"
            ],
            "name": "x1",
            "need_compile": false,
            "param_type": "required",
            "shape": "all"
        },
        {
            "index": 1,
            "dtype": [
                "float16"
            ],
            "format": [
                "NC1HWC0"
            ],
            "name": "x2",
            "need_compile": false,
            "param_type": "required",
            "shape": "all"
        },
        {
            "index": 2,
            "dtype": [
                "float16"
            ],
            "format": [
                "NC1HWC0"
            ],
            "name": "grad",
            "need_compile": false,
            "param_type": "required",
            "shape": "all"
        }
    ],
    "outputs": [
        {
            "index": 0,
            "dtype": [
                "float16"
            ],
            "format": [
                "NC1HWC0"
            ],
            "name": "y",
            "param_type": "required"
        }
    ]
}""")
def _max_pool_grad_tbe():
    """MaxPoolGrad TBE register"""
    return
