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
# ==============================================================================
"""Validators for TensorOps.
"""
from functools import wraps
from mindspore._c_expression import typing


# POS_INT_MIN is used to limit values from starting from 0
POS_INT_MIN = 1
UINT8_MAX = 255
UINT8_MIN = 0
UINT32_MAX = 4294967295
UINT32_MIN = 0
UINT64_MAX = 18446744073709551615
UINT64_MIN = 0
INT32_MAX = 2147483647
INT32_MIN = -2147483648
INT64_MAX = 9223372036854775807
INT64_MIN = -9223372036854775808
FLOAT_MAX_INTEGER = 16777216
FLOAT_MIN_INTEGER = -16777216
DOUBLE_MAX_INTEGER = 9007199254740992
DOUBLE_MIN_INTEGER = -9007199254740992


def check_type(value, valid_type):
    if not isinstance(value, valid_type):
        raise ValueError("Wrong input type")


def check_value(value, valid_range):
    if value < valid_range[0] or value > valid_range[1]:
        raise ValueError("Input is not within the required range")


def check_range(values, valid_range):
    if not valid_range[0] <= values[0] <= values[1] <= valid_range[1]:
        raise ValueError("Input range is not valid")


def check_positive(value):
    if value <= 0:
        raise ValueError("Input must greater than 0")


def check_positive_float(value, valid_max=None):
    if value <= 0 or not isinstance(value, float) or (valid_max is not None and value > valid_max):
        raise ValueError("Input need to be a valid positive float.")


def check_bool(value):
    if not isinstance(value, bool):
        raise ValueError("Value needs to be a boolean.")


def check_2tuple(value):
    if not (isinstance(value, tuple) and len(value) == 2):
        raise ValueError("Value needs to be a 2-tuple.")


def check_list(value):
    if not isinstance(value, list):
        raise ValueError("The input needs to be a list.")


def check_uint8(value):
    if not isinstance(value, int):
        raise ValueError("The input needs to be a integer")
    check_value(value, [UINT8_MIN, UINT8_MAX])


def check_uint32(value):
    if not isinstance(value, int):
        raise ValueError("The input needs to be a integer")
    check_value(value, [UINT32_MIN, UINT32_MAX])


def check_pos_int32(value):
    """Checks for int values starting from 1"""
    if not isinstance(value, int):
        raise ValueError("The input needs to be a integer")
    check_value(value, [POS_INT_MIN, INT32_MAX])


def check_uint64(value):
    if not isinstance(value, int):
        raise ValueError("The input needs to be a integer")
    check_value(value, [UINT64_MIN, UINT64_MAX])


def check_pos_int64(value):
    if not isinstance(value, int):
        raise ValueError("The input needs to be a integer")
    check_value(value, [UINT64_MIN, INT64_MAX])


def check_pos_float32(value):
    check_value(value, [UINT32_MIN, FLOAT_MAX_INTEGER])


def check_pos_float64(value):
    check_value(value, [UINT64_MIN, DOUBLE_MAX_INTEGER])


def check_one_hot_op(method):
    """Wrapper method to check the parameters of one hot op."""

    @wraps(method)
    def new_method(self, *args, **kwargs):
        args = (list(args) + 2 * [None])[:2]
        num_classes, smoothing_rate = args
        if "num_classes" in kwargs:
            num_classes = kwargs.get("num_classes")
        if "smoothing_rate" in kwargs:
            smoothing_rate = kwargs.get("smoothing_rate")

        if num_classes is None:
            raise ValueError("num_classes")
        check_pos_int32(num_classes)
        kwargs["num_classes"] = num_classes
        if smoothing_rate is not None:
            check_value(smoothing_rate, [0., 1.])
            kwargs["smoothing_rate"] = smoothing_rate

        return method(self, **kwargs)

    return new_method


def check_num_classes(method):
    """Wrapper method to check the parameters of number of classes."""

    @wraps(method)
    def new_method(self, *args, **kwargs):
        num_classes = (list(args) + [None])[0]
        if "num_classes" in kwargs:
            num_classes = kwargs.get("num_classes")
        if num_classes is None:
            raise ValueError("num_classes is not provided.")

        check_pos_int32(num_classes)
        kwargs["num_classes"] = num_classes

        return method(self, **kwargs)

    return new_method


def check_de_type(method):
    """Wrapper method to check the parameters of data type."""

    @wraps(method)
    def new_method(self, *args, **kwargs):
        data_type = (list(args) + [None])[0]
        if "data_type" in kwargs:
            data_type = kwargs.get("data_type")

        if data_type is None:
            raise ValueError("data_type is not provided.")
        if not isinstance(data_type, typing.Type):
            raise TypeError("data_type is not a MindSpore data type.")
        kwargs["data_type"] = data_type

        return method(self, **kwargs)

    return new_method
