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
"""tbe common"""
import json
import os


class TBEException(Exception):
    """tbe exception class"""

    def __init__(self, err_msg):
        super().__init__(self)
        self.__error_msg = err_msg

    def __str__(self):
        return self.__error_msg


def get_ddk_version():
    """get ddk version"""
    ddk_version = os.environ.get("DDK_VERSION")
    if ddk_version is None:
        default_ddk_info_file = '/usr/local/HiAI/runtime/ddk_info'
        backup_ddk_info_file = '/usr/local/Ascend/fwkacllib/ddk_info'
        if os.path.exists(default_ddk_info_file):
            with open(default_ddk_info_file, "r") as fp:
                ddk_version = json.load(fp)["VERSION"]
        elif os.path.exists(backup_ddk_info_file):
            with open(backup_ddk_info_file, "r") as fp:
                ddk_version = json.load(fp)["VERSION"]
        else:
            ddk_version = "1.60.T17.B830"
    return ddk_version


def get_build_in_impl_path():
    """get build-in tbe implement path"""
    tbe_impl_path = os.environ.get("TBE_IMPL_PATH")
    if tbe_impl_path is None:
        default_install_path = '/usr/local/HiAI/runtime/ops/op_impl/built-in/ai_core/tbe/'
        backup_install_path = '/usr/local/Ascend/opp/op_impl/built-in/ai_core/tbe/'
        if os.path.exists(default_install_path):
            tbe_impl_path = default_install_path
        elif os.path.exists(backup_install_path):
            tbe_impl_path = backup_install_path
    if not tbe_impl_path:
        raise ValueError("Can not find the env TBE_IMPL_PATH")
    return tbe_impl_path


def _check_arg_info(item):
    """
    Check parameter Validity.

    Args:
        item (dict): A dict, to be checked.

    Raises:
        Exception: If specific keyword is not found.
    """
    if 'shape' not in item:
        raise ValueError("Json string Errors, key:shape not found.")
    if 'ori_shape' not in item:
        raise ValueError("Json string Errors, key:ori_shape not found.")
    if 'format' not in item or not item['format']:
        raise ValueError("Json string Errors, key:format not found.")
    if 'ori_format' not in item or not item['ori_format']:
        raise ValueError("Json string Errors, key:ori_format not found.")
    if 'dtype' not in item or not item['dtype']:
        raise ValueError("Json string Errors, key:dtype not found.")


def get_args(op_info, arg_type):
    """
    Parse args.

    Args:
        op_info (dict): Op info dict.
        arg_type (str): arg, to be parsed.

    Raises:
        Exception: If specific keyword is not found.
    """
    if arg_type not in op_info:
        raise ValueError("Json string Errors, key:{} not found.".format(arg_type))
    args = []
    if not op_info[arg_type]:
        return args
    if arg_type in ['inputs', 'outputs']:
        for item in op_info[arg_type]:
            arg = []
            for info in item:
                if 'valid' not in info:
                    raise ValueError("Json string Errors, key:valid not found.")
                if info['valid']:
                    _check_arg_info(info)
                    del info['valid']
                    del info['name']
                    if len(item) > 1:
                        arg.append(info)
                    else:
                        args.append(info)
                else:
                    if len(item) > 1:
                        arg.append(None)
                    else:
                        args.append(None)
            if len(item) > 1:
                args.append(arg)

    elif arg_type == 'attrs':
        for item in op_info[arg_type]:
            if item["valid"]:
                if 'value' not in item:
                    raise ValueError("Json string Errors, attr key:value not found.")
                if item["name"] != "isRef":
                    args.append(item['value'])

    return args


def check_kernel_info(kernel_info):
    if 'op_info' not in kernel_info or not kernel_info['op_info']:
        raise ValueError("Json string Errors, key:op_info not found.")
    if 'name' not in kernel_info['op_info'] or not kernel_info['op_info']['name']:
        raise ValueError("Json string Errors, key:name not found.")
    if 'kernel_name' not in kernel_info['op_info'] or not kernel_info['op_info']['kernel_name']:
        raise ValueError("Json string Errors, key:kernel_name not found.")
