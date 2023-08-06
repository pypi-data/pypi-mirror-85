# Copyright 2019 Huawei Technologies Co., Ltd
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

"""Mul op"""
from mindspore.ops.op_info_register import op_info_register

@op_info_register("""{
    "op_name": "Mul",
    "imply_type": "AutoDiff",
    "fusion_type": "OPAQUE",
    "processor": "cuda",
    "attr": [
    ],
    "inputs": [
        {
            "index": 0,
            "dtype": [
                "float32", "float16"
            ],
            "format": [
                "DefaultFormat", "DefaultFormat"
            ],
            "name": "x"
        },
        {
            "index": 1,
            "dtype": [
                "float32", "float16"
            ],
            "format": [
                "DefaultFormat", "DefaultFormat"
            ],
            "name": "y"
        }
    ],
    "outputs": [
        {
            "index": 0,
            "dtype": [
                "float32", "float16"
            ],
            "format": [
                "DefaultFormat", "DefaultFormat"
            ],
            "name": "output"
        }
    ]
}""")
def _mul_akg():
    """Mul AutoDiff register"""
    return
