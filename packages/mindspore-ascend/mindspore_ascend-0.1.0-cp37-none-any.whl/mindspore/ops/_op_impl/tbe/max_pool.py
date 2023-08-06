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

"""MaxPool op"""
from mindspore.ops.op_info_register import op_info_register


@op_info_register("""{
    "op_name": "MaxPool",
    "imply_type": "TBE",
    "fusion_type": "OPAQUE",
    "async_flag": false,
    "binfile_name": "max_pool.so",
    "compute_cost": 10,
    "kernel_name": "max_pool",
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
        },
        {
            "name": "data_format",
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
            "name": "input_data",
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
            "name": "output_data",
            "param_type": "required",
            "shape": "all"
        }
    ]
}""")
def _max_pool_tbe():
    """MaxPool TBE register"""
    return
