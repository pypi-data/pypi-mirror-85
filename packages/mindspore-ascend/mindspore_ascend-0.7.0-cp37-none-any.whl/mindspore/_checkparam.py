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
"""Check parameters."""
import re
import inspect
import math
from enum import Enum
from functools import reduce, wraps
from itertools import repeat
from collections.abc import Iterable

import numpy as np
from mindspore import log as logger
from .common import dtype as mstype


# Named string regular expression
_name_re = r"^\w+[0-9a-zA-Z\_\.]*$"


class Rel(Enum):
    """Numerical relationship between variables, logical relationship enumeration definition of range."""
    # scalar compare
    EQ = 1  # ==
    NE = 2  # !=
    LT = 3  # <
    LE = 4  # <=
    GT = 5  # >
    GE = 6  # >=
    # scalar range check
    INC_NEITHER = 7  # (), include neither
    INC_LEFT = 8     # [), include left
    INC_RIGHT = 9    # (], include right
    INC_BOTH = 10    # [], include both
    # collection in, not in
    IN = 11
    NOT_IN = 12

    @staticmethod
    def get_strs(rel):
        """Get value from rel_strs."""
        return rel_strs.get(rel, "")

    @staticmethod
    def get_fns(rel):
        """Get value from rel_fns."""
        return rel_fns.get(rel, lambda *args: False)


rel_fns = {
    # scalar compare
    Rel.EQ: lambda x, y: x == y,
    Rel.NE: lambda x, y: x != y,
    Rel.LT: lambda x, y: x < y,
    Rel.LE: lambda x, y: x <= y,
    Rel.GT: lambda x, y: x > y,
    Rel.GE: lambda x, y: x >= y,
    # scalar range check
    Rel.INC_NEITHER: lambda x, lower, upper: (lower < x < upper),
    Rel.INC_LEFT: lambda x, lower, upper: (lower <= x < upper),
    Rel.INC_RIGHT: lambda x, lower, upper: (lower < x <= upper),
    Rel.INC_BOTH: lambda x, lower, upper: (lower <= x <= upper),
    # collection in, not in
    Rel.IN: lambda x, y: x in y,
    Rel.NOT_IN: lambda x, y: x not in y,
}

rel_strs = {
    # scalar compare
    Rel.EQ: "equal to {}",
    Rel.NE: "not equal to {}",
    Rel.LT: "less than {}",
    Rel.LE: "less or equal to {}",
    Rel.GT: "greater than {}",
    Rel.GE: "greater or equal to {}",
    # scalar range check
    Rel.INC_NEITHER: "({}, {})",
    Rel.INC_LEFT: "[{}, {})",
    Rel.INC_RIGHT: "({}, {}]",
    Rel.INC_BOTH: "[{}, {}]",
    # collection in, not in
    Rel.IN: "in {}",
    Rel.NOT_IN: "not in {}",
}


class Validator:
    """validator for checking input parameters"""

    @staticmethod
    def check(arg_name, arg_value, value_name, value, rel=Rel.EQ, prim_name=None, excp_cls=ValueError):
        """
        Method for judging relation between two int values or list/tuple made up of ints.

        This method is not suitable for judging relation between floats, since it does not consider float error.
        """

        rel_fn = Rel.get_fns(rel)
        if not rel_fn(arg_value, value):
            rel_str = Rel.get_strs(rel).format(f'{value_name}: {value}')
            msg_prefix = f'For \'{prim_name}\' the' if prim_name else "The"
            raise excp_cls(f'{msg_prefix} `{arg_name}` should be {rel_str}, but got {arg_value}.')

    @staticmethod
    def check_integer(arg_name, arg_value, value, rel, prim_name):
        """Integer value judgment."""
        rel_fn = Rel.get_fns(rel)
        type_mismatch = not isinstance(arg_value, int) or isinstance(arg_value, bool)
        excp_cls = TypeError if type_mismatch else ValueError
        if type_mismatch or not rel_fn(arg_value, value):
            rel_str = Rel.get_strs(rel).format(value)
            msg_prefix = f'For \'{prim_name}\' the' if prim_name else "The"
            raise excp_cls(f'{msg_prefix} `{arg_name}` should be an int and must {rel_str}, but got `{arg_value}`'
                           f' with type `{type(arg_value).__name__}`.')
        return arg_value

    @staticmethod
    def check_number(arg_name, arg_value, value, rel, prim_name):
        """Number value judgment."""
        rel_fn = Rel.get_fns(rel)
        if not rel_fn(arg_value, value):
            rel_str = Rel.get_strs(rel).format(value)
            raise ValueError(f'For \'{prim_name}\' the `{arg_name}` must {rel_str}, but got {arg_value}.')
        return arg_value

    @staticmethod
    def check_int_range(arg_name, arg_value, lower_limit, upper_limit, rel, prim_name):
        """Method for checking whether an int value is in some range."""
        rel_fn = Rel.get_fns(rel)
        type_mismatch = not isinstance(arg_value, int)
        excp_cls = TypeError if type_mismatch else ValueError
        if type_mismatch or not rel_fn(arg_value, lower_limit, upper_limit):
            rel_str = Rel.get_strs(rel).format(lower_limit, upper_limit)
            raise excp_cls(f'For \'{prim_name}\' the `{arg_name}` should be an int in range {rel_str},'
                           f' but got `{arg_value}` with type `{type(arg_value).__name__}`.')
        return arg_value

    @staticmethod
    def check_number_range(arg_name, arg_value, lower_limit, upper_limit, rel, prim_name):
        """Method for checking whether a numeric value is in some range."""
        rel_fn = Rel.get_fns(rel)
        if not rel_fn(arg_value, lower_limit, upper_limit):
            rel_str = Rel.get_strs(rel).format(lower_limit, upper_limit)
            raise ValueError(f'For \'{prim_name}\' the `{arg_name}` should be in range {rel_str}, but got {arg_value}.')
        return arg_value

    @staticmethod
    def check_string(arg_name, arg_value, valid_values, prim_name):
        """Checks whether a string is in some value list"""
        if isinstance(arg_value, str) and arg_value in valid_values:
            return arg_value
        if len(valid_values) == 1:
            raise ValueError(f'For \'{prim_name}\' the `{arg_name}` should be str and must be {valid_values[0]},'
                             f' but got {arg_value}.')
        raise ValueError(f'For \'{prim_name}\' the `{arg_name}` should be str and must be one of {valid_values},'
                         f' but got {arg_value}.')

    @staticmethod
    def check_pad_value_by_mode(pad_mode, padding, prim_name):
        """Validates value of padding according to pad_mode"""
        if pad_mode != 'pad' and padding != 0:
            raise ValueError(f"For '{prim_name}', padding must be zero when pad_mode is '{pad_mode}'.")
        return padding

    @staticmethod
    def check_float_positive(arg_name, arg_value, prim_name):
        """Float type judgment."""
        msg_prefix = f'For \'{prim_name}\' the' if prim_name else "The"
        if isinstance(arg_value, float):
            if arg_value > 0:
                return arg_value
            raise ValueError(f"{msg_prefix} `{arg_name}` must be positive, but got {arg_value}.")
        raise TypeError(f"{msg_prefix} `{arg_name}` must be float.")

    @staticmethod
    def check_subclass(arg_name, type_, template_type, prim_name):
        """Checks whether some type is subclass of another type"""
        if not isinstance(template_type, Iterable):
            template_type = (template_type,)
        if not any([mstype.issubclass_(type_, x) for x in template_type]):
            type_str = (type(type_).__name__ if isinstance(type_, (tuple, list)) else "") + str(type_)
            raise TypeError(f'For \'{prim_name}\' the type of `{arg_name}` should be subclass'
                            f' of {",".join((str(x) for x in template_type))}, but got {type_str}.')

    @staticmethod
    def check_const_input(arg_name, arg_value, prim_name):
        """Checks valid value."""
        if arg_value is None:
            raise ValueError(f'For \'{prim_name}\' the `{arg_name}` must be a const input, but got {arg_value}.')

    @staticmethod
    def check_type_same(args, valid_values, prim_name):
        """Checks whether the types of inputs are the same."""
        def _check_tensor_type(arg):
            arg_key, arg_val = arg
            elem_type = arg_val
            if not elem_type in valid_values:
                type_names = []
                for t in valid_values:
                    type_names.append(str(t))
                types_info = '[' + ', '.join(type_names) + ']'
                raise TypeError(f'For \'{prim_name}\' type of `{arg_key}` should be in {types_info},'
                                f' but got {elem_type}.')
            return (arg_key, elem_type)

        def _check_types_same(arg1, arg2):
            arg1_name, arg1_type = arg1
            arg2_name, arg2_type = arg2
            if arg1_type != arg2_type:
                raise TypeError(f'For \'{prim_name}\' type of `{arg2_name}` should be same as `{arg1_name}`,'
                                f' but `{arg1_name}` with type {arg1_type} and `{arg2_name}` with type {arg2_type}.')
            return arg1

        elem_types = map(_check_tensor_type, args.items())
        reduce(_check_types_same, elem_types)

    @staticmethod
    def check_tensor_type_same(args, valid_values, prim_name):
        """Checks whether the element types of input tensors are the same."""
        tensor_types = [mstype.tensor_type(t) for t in valid_values]
        Validator.check_type_same(args, tensor_types, prim_name)

    @staticmethod
    def check_scalar_or_tensor_type_same(args, valid_values, prim_name, allow_mix=False):
        """
        Checks whether the types of inputs are the same. If the input args are tensors, checks their element types.

        If `allow_mix` is True, Tensor(float32) and float32 are type compatible, otherwise an exception will be raised.
        """

        def _check_argument_type(arg):
            arg_key, arg_val = arg
            if isinstance(arg_val, type(mstype.tensor)):
                arg_val = arg_val.element_type()
            if not arg_val in valid_values:
                raise TypeError(f'For \'{prim_name}\' the `{arg_key}` should be in {valid_values},'
                                f' but `{arg_key}` is {arg_val}.')
            return arg

        def _check_types_same(arg1, arg2):
            arg1_name, arg1_type = arg1
            arg2_name, arg2_type = arg2
            except_flag = False
            if isinstance(arg1_type, type(mstype.tensor)) and isinstance(arg2_type, type(mstype.tensor)):
                arg1_type = arg1_type.element_type()
                arg2_type = arg2_type.element_type()
            elif not (isinstance(arg1_type, type(mstype.tensor)) or isinstance(arg2_type, type(mstype.tensor))):
                pass
            elif allow_mix:
                arg1_type = arg1_type.element_type() if isinstance(arg1_type, type(mstype.tensor)) else arg1_type
                arg2_type = arg2_type.element_type() if isinstance(arg2_type, type(mstype.tensor)) else arg2_type
            else:
                except_flag = True

            if except_flag or arg1_type != arg2_type:
                raise TypeError(f'For \'{prim_name}\' type of `{arg2_name}` should be same as `{arg1_name}`,'
                                f' but `{arg1_name}` is {arg1_type} and `{arg2_name}` is {arg2_type}.')
            return arg1
        reduce(_check_types_same, map(_check_argument_type, args.items()))

    @staticmethod
    def check_value_type(arg_name, arg_value, valid_types, prim_name):
        """Checks whether a value is instance of some types."""
        valid_types = valid_types if isinstance(valid_types, Iterable) else (valid_types,)

        def raise_error_msg():
            """func for raising error message when check failed"""
            type_names = [t.__name__ for t in valid_types]
            num_types = len(valid_types)
            msg_prefix = f'For \'{prim_name}\' the' if prim_name else 'The'
            raise TypeError(f'{msg_prefix} type of `{arg_name}` should be {"one of " if num_types > 1 else ""}'
                            f'{type_names if num_types > 1 else type_names[0]}, but got {type(arg_value).__name__}.')

        # Notice: bool is subclass of int, so `check_value_type('x', True, [int])` will check fail, and
        #         `check_value_type('x', True, [bool, int])` will check pass
        if isinstance(arg_value, bool) and bool not in tuple(valid_types):
            raise_error_msg()
        if isinstance(arg_value, tuple(valid_types)):
            return arg_value
        raise_error_msg()

    @staticmethod
    def check_type_name(arg_name, arg_type, valid_types, prim_name):
        """Checks whether a type in some specified types"""
        valid_types = valid_types if isinstance(valid_types, Iterable) else (valid_types,)

        def get_typename(t):
            return t.__name__ if hasattr(t, '__name__') else str(t)

        if isinstance(arg_type, type(mstype.tensor)):
            arg_type = arg_type.element_type()

        if arg_type in valid_types:
            return arg_type
        type_names = [get_typename(t) for t in valid_types]
        msg_prefix = f'For \'{prim_name}\' the' if prim_name else 'The'
        if len(valid_types) == 1:
            raise TypeError(f'{msg_prefix} type of `{arg_name}` should be {type_names[0]},'
                            f' but got {get_typename(arg_type)}.')
        raise TypeError(f'{msg_prefix} type of `{arg_name}` should be one of {type_names},'
                        f' but got {get_typename(arg_type)}.')

    @staticmethod
    def check_float_legal_value(arg_name, arg_value, prim_name):
        """Checks whether a legal value of float type"""
        msg_prefix = f'For \'{prim_name}\' the' if prim_name else "The"
        if isinstance(arg_value, float):
            if math.isinf(arg_value) or math.isnan(arg_value):
                raise ValueError(f"{msg_prefix} `{arg_name}` must be legal value, but got {arg_value}.")
            return arg_value
        raise TypeError(f"{msg_prefix} `{arg_name}` must be float.")

    @staticmethod
    def check_reduce_shape(ori_shape, shape, axis, prim_name):
        """Checks whether shape is ori_shape reduced on axis"""
        axis = axis if isinstance(axis, Iterable) else (axis,)
        exp_shape = [ori_shape[i] for i in range(len(ori_shape)) if i not in axis]
        if list(shape) != exp_shape:
            raise ValueError(f'For {prim_name}, {ori_shape} reduce on {axis} should be '
                             f'{tuple(exp_shape)}, but got {shape}.')


class ParamValidator:
    """Parameter validator. NOTICE: this class will be replaced by `class Validator`"""

    @staticmethod
    def equal(arg_name, arg_value, cond_str, cond):
        """Judging valid value."""
        if not cond:
            raise ValueError(f'The `{arg_name}` must be {cond_str}, but got {arg_value}.')

    @staticmethod
    def check(arg_name, arg_value, value_name, value, rel=Rel.EQ):
        """This method is only used for check int values, since when compare float values,
        we need consider float error."""
        rel_fn = Rel.get_fns(rel)
        if not rel_fn(arg_value, value):
            rel_str = Rel.get_strs(rel).format(f'{value_name}: {value}')
            raise ValueError(f'The `{arg_name}` should be {rel_str}, but got {arg_value}.')

    @staticmethod
    def check_integer(arg_name, arg_value, value, rel):
        """Integer value judgment."""
        rel_fn = Rel.get_fns(rel)
        type_mismatch = not isinstance(arg_value, int) or isinstance(arg_value, bool)
        if type_mismatch or not rel_fn(arg_value, value):
            rel_str = Rel.get_strs(rel).format(value)
            raise ValueError(f'The `{arg_name}` should be an int and must {rel_str}, but got {arg_value}.')
        return arg_value

    @staticmethod
    def check_shape_length(arg_name, arg_value, value, rel):
        """Shape length judgment."""
        rel_fn = Rel.get_fns(rel)
        type_mismatch = not isinstance(arg_value, int)
        if type_mismatch or not rel_fn(arg_value, value):
            rel_str = Rel.get_strs(rel).format(value)
            raise ValueError(f'The length of `{arg_name}` should be an int and must {rel_str}, but got {arg_value}')
        return arg_value

    @staticmethod
    def check_int_range(arg_name, arg_value, lower_limit, upper_limit, rel):
        """This method is only used for check int values,
        since when compare float values, we need consider float error."""
        rel_fn = Rel.get_fns(rel)
        type_mismatch = not isinstance(arg_value, int)
        if type_mismatch or not rel_fn(arg_value, lower_limit, upper_limit):
            rel_str = Rel.get_strs(rel).format(lower_limit, upper_limit)
            raise ValueError(f'The `{arg_name}` should be an int in range {rel_str}, but got {arg_value}.')
        return arg_value

    @staticmethod
    def check_isinstance(arg_name, arg_value, classes):
        """Check arg isinstance of classes"""
        if not isinstance(arg_value, classes):
            raise ValueError(f'The `{arg_name}` should be isinstance of {classes}, but got {arg_value}.')
        return arg_value

    @staticmethod
    def check_number_range(arg_name, arg_value, lower_limit, upper_limit, rel):
        """Is it necessary to consider error when comparing float values."""
        rel_fn = Rel.get_fns(rel)
        if not rel_fn(arg_value, lower_limit, upper_limit):
            rel_str = Rel.get_strs(rel).format(lower_limit, upper_limit)
            raise ValueError(f'The `{arg_name}` should be in range {rel_str}, but got {arg_value}.')
        return arg_value

    @staticmethod
    def check_subclass(arg_name, type_, template_type, with_type_of=True):
        """Check whether some type is subclass of another type"""
        if not isinstance(template_type, Iterable):
            template_type = (template_type,)
        if not any([mstype.issubclass_(type_, x) for x in template_type]):
            type_str = (type(type_).__name__ if isinstance(type_, (tuple, list)) else "") + str(type_)
            raise TypeError(f'The {"type of" if with_type_of else ""} `{arg_name}` should be subclass'
                            f' of {",".join((str(x) for x in template_type))}, but got {type_str}.')

    @staticmethod
    def check_args_tensor(args):
        """Check whether args are all tensor."""
        if not isinstance(args, dict):
            raise TypeError("The args should be a dict.")
        for arg, value in args.items():
            ParamValidator.check_subclass(arg, value, mstype.tensor)

    @staticmethod
    def check_bool(arg_name, arg_value):
        """Check arg isinstance of bool"""
        if not isinstance(arg_value, bool):
            raise ValueError(f'The `{arg_name}` should be isinstance of bool, but got {arg_value}.')
        return arg_value

    @staticmethod
    def check_type(arg_name, arg_value, valid_types):
        """Type checking."""
        def raise_error_msg():
            """func for raising error message when check failed"""
            type_names = [t.__name__ for t in valid_types]
            num_types = len(valid_types)
            raise TypeError(f'The type of `{arg_name}` should be {"one of " if num_types > 1 else ""}'
                            f'{type_names if num_types > 1 else type_names[0]}, but got {type(arg_value).__name__}.')

        if isinstance(arg_value, type(mstype.tensor)):
            arg_value = arg_value.element_type()
        # Notice: bool is subclass of int, so `check_type('x', True, [int])` will check fail, and
        #         `check_type('x', True, [bool, int])` will check pass
        if isinstance(arg_value, bool) and bool not in tuple(valid_types):
            raise_error_msg()
        if isinstance(arg_value, tuple(valid_types)):
            return arg_value
        raise_error_msg()

    @staticmethod
    def check_typename(arg_name, arg_type, valid_types):
        """Does it contain the _name_ attribute."""

        def get_typename(t):
            return t.__name__ if hasattr(t, '__name__') else str(t)

        if isinstance(arg_type, type(mstype.tensor)):
            arg_type = arg_type.element_type()

        if arg_type in valid_types:
            return arg_type
        type_names = [get_typename(t) for t in valid_types]
        if len(valid_types) == 1:
            raise ValueError(f'The type of `{arg_name}` should be {type_names[0]},'
                             f' but got {get_typename(arg_type)}.')
        raise ValueError(f'The type of `{arg_name}` should be one of {type_names},'
                         f' but got {get_typename(arg_type)}.')

    @staticmethod
    def check_string(arg_name, arg_value, valid_values):
        """String type judgment."""
        if isinstance(arg_value, str) and arg_value in valid_values:
            return arg_value
        if len(valid_values) == 1:
            raise ValueError(f'The `{arg_name}` should be str and must be {valid_values[0]},'
                             f' but got {arg_value}.')
        raise ValueError(f'The `{arg_name}` should be str and must be one of {valid_values},'
                         f' but got {arg_value}.')

    @staticmethod
    def check_type_same(args, valid_values):
        """Determine whether the types are the same."""
        name = list(args.keys())[0]
        value = list(args.values())[0]
        if isinstance(value, type(mstype.tensor)):
            value = value.element_type()
        for arg_name, arg_value in args.items():
            if isinstance(arg_value, type(mstype.tensor)):
                arg_value = arg_value.element_type()

            if arg_value not in valid_values:
                raise TypeError(f'The `{arg_name}` should be in {valid_values},'
                                f' but `{arg_name}` is {arg_value}.')
            if arg_value != value:
                raise TypeError(f'`{arg_name}` should be same as `{name}`,'
                                f' but `{arg_name}` is {arg_value}, `{name}` is {value}.')

    @staticmethod
    def check_two_types_same(arg1_name, arg1_type, arg2_name, arg2_type):
        """Determine whether the types of two variables are the same."""
        if arg1_type != arg2_type:
            raise TypeError(f'The type of `{arg1_name}` and `{arg2_name}` should be same.')

    @staticmethod
    def check_value_on_integer(arg_name, arg_value, value, rel):
        """Judging integer type."""
        rel_fn = Rel.get_fns(rel)
        type_match = isinstance(arg_value, int)
        if type_match and (not rel_fn(arg_value, value)):
            rel_str = Rel.get_strs(rel).format(value)
            raise ValueError(f'The `{arg_name}` should be an int and must {rel_str}, but got {arg_value}.')
        return arg_value

    @staticmethod
    def check_param_equal(param1_name, param1_value, param2_name, param2_value):
        """Judging the equality of parameters."""
        if param1_value != param2_value:
            raise ValueError(f"`{param1_name}` must equal `{param2_name}`,"
                             f" but got `{param1_name}` = {param1_value},"
                             f" `{param2_name}` = {param2_value}.")

    @staticmethod
    def check_const_input(arg_name, arg_value):
        """Check valid value."""
        if arg_value is None:
            raise ValueError(f'The `{arg_name}` must be a const input, but got {arg_value}.')

    @staticmethod
    def check_float_positive(arg_name, arg_value):
        """Float type judgment."""
        if isinstance(arg_value, float):
            if arg_value > 0:
                return arg_value
            raise ValueError(f"The `{arg_name}` must be positive, but got {arg_value}.")

        raise TypeError(f"`{arg_name}` must be float!")

    @staticmethod
    def check_pad_value_by_mode(op_name, pad_mode, padding):
        """Validate value of padding according to pad_mode"""
        if pad_mode != 'pad' and padding != 0:
            raise ValueError(f"For op '{op_name}', padding must be zero when pad_mode is '{pad_mode}'.")
        return padding

    @staticmethod
    def check_empty_shape_input(arg_name, arg_value):
        """Check zeros value."""
        if 0 in arg_value:
            raise ValueError(f"Input `{arg_name}` cannot be empty.")

    @staticmethod
    def check_scalar_shape_input(arg_name, arg_value):
        """Check scalar shape input."""
        if arg_value != []:
            raise ValueError(f"Input `{arg_name}` shape should be (). got {arg_value}")


def check_int(input_param):
    """Int type judgment."""
    if isinstance(input_param, int) and not isinstance(input_param, bool):
        return input_param
    raise TypeError("Input type must be int!")


def check_int_positive(input_param):
    """Int type judgment."""
    if isinstance(input_param, bool):
        raise TypeError("Input type must be int cannot be bool!")
    if isinstance(input_param, int):
        if input_param > 0:
            return input_param
        raise ValueError("The input_param must be positive, but got input_param {}.".format(input_param))
    raise TypeError("Input type must be int cannot be {}!".format(type(input_param)))


def check_int_non_negative(input_param):
    """Non_negative type judgment."""
    if isinstance(input_param, bool):
        raise TypeError("Input type must be int cannot be bool!")
    if isinstance(input_param, int):
        if input_param >= 0:
            return input_param
        raise ValueError("The input_param must be non_negative, but got input_param {}.".format(input_param))
    raise TypeError("Input type must be int cannot be {}!".format(type(input_param)))


def check_int_zero_one(input_param):
    """Judge whether it is 0 or 1."""
    if input_param in (0, 1):
        return input_param
    raise ValueError("The data must be 0 or 1.")


def check_bool(input_param):
    """Bool type judgment."""
    if isinstance(input_param, bool):
        return input_param
    raise TypeError("Input type must be bool!")


def check_string(input_param, valid_values):
    """String type judgment."""
    if isinstance(input_param, str) and input_param in valid_values:
        return input_param
    if len(valid_values) == 1:
        raise ValueError(f'Input should be str and must be {valid_values[0]},'
                         f' but got {input_param}.')
    raise ValueError(f'Input should be str and must be one of {valid_values},'
                     f' but got {input_param}.')


def check_input_format(input_param):
    """Judge input format."""
    if input_param == "NCHW":
        return input_param
    raise ValueError("The data format must be NCHW.")


def check_padding(padding):
    """Check padding."""
    if padding >= 0:
        return padding
    raise ValueError("The padding must be at least 0,"" but got padding {}.".format(padding))


def check_padmode(mode):
    """Check padmode."""
    if mode in ("same", "valid", "pad"):
        return mode
    raise ValueError("The pad mode must be same or valid or pad,"" but got mode {}.".format(mode))


def check_tensor_supported_type(dtype):
    """Check tensor dtype."""
    if dtype in (mstype.int32, mstype.float32):
        return dtype
    raise ValueError("The dtype must be mstype.int32 or mstype.float32, but got mstype {}.".format(dtype))


def _expand_tuple(n_dimensions):
    """To expand a number to tuple."""

    def convert(m):
        if not isinstance(m, tuple):
            if isinstance(m, int):
                return tuple(repeat(m, n_dimensions))
            raise TypeError("Input type must be int or tuple.")

        if not len(m) is n_dimensions:
            raise TypeError("Input dimension is incorrect.")

        for i in m:
            if not isinstance(i, int):
                raise TypeError("Incorrect type inside of a tuple!")
        return m

    return convert


def check_input_data(*data, data_class):
    """Input data check."""
    for item in data:
        if isinstance(item, (list, tuple)):
            for v in item:
                check_input_data(v, data_class=data_class)
        else:
            if not isinstance(item, data_class):
                raise ValueError(f'Please provide as model inputs'
                                 f' either a single'
                                 f' or a list of {data_class.__name__},'
                                 f' but got part data type is {str(type(item))}.')
            if item.size() == 0:
                msg = "Please provide non-empty data."
                logger.error(msg)
                raise ValueError(msg)


def check_output_data(data):
    """Output data check."""
    if data is None:
        raise RuntimeError('Executor return data ' + str(data) + ', please check your net or input data.')


once = _expand_tuple(1)
twice = _expand_tuple(2)
triple = _expand_tuple(3)
valid_data_types = (int, float, np.int8, np.int16, np.int32, np.int64,
                    np.uint8, np.uint16, np.uint32, np.uint64, np.float16,
                    np.float32, np.float64, bool, np.bool_)


def check_type(arg_name, arg_value, valid_types):
    """Check value type."""
    # if input type is Tensor ,get element type
    if isinstance(arg_value, type(mstype.tensor)):
        arg_value = arg_value.element_type()

    # First, check if arg_value has argvalid_types
    if isinstance(arg_value, tuple(valid_types)):
        return type(arg_value).__name__

    # Second, wrap arg_value with numpy array so that it can be checked through numpy api
    if isinstance(arg_value, (list, tuple)):
        arg_value = np.array(arg_value)

    # Thirdly, check the data type by numpy's dtype api
    valid = False
    if isinstance(arg_value, np.ndarray):
        valid = arg_value.dtype in valid_data_types

    # Notice: bool is subclass of int, so `check_type('x', True, [int])` will check fail, and
    #         `check_type('x', True, [bool, int])` will check pass
    if isinstance(arg_value, bool) and bool not in tuple(valid_types):
        valid = False

    if not valid:
        type_names = [t.__name__ for t in valid_types]
        if len(valid_types) == 1:
            raise TypeError(f'The type of `{arg_name}` should be {type_names[0]},'
                            f' but got {type(arg_value).__name__}.')
        raise TypeError(f'The type of `{arg_name}` should be one of {type_names},'
                        f' but got {type(arg_value).__name__}.')

    return type(arg_value).__name__


def check_typename(arg_name, arg_type, valid_types):
    """Check type name."""

    def get_typename(t):
        return t.__name__ if hasattr(t, '__name__') else str(t)

    if isinstance(arg_type, type(mstype.tensor)):
        arg_type = arg_type.element_type()

    if arg_type in valid_types:
        return arg_type
    if isinstance(arg_type, tuple(valid_types)):
        return arg_type
    type_names = [get_typename(t) for t in valid_types]
    if len(valid_types) == 1:
        raise TypeError(f'The type of `{arg_name}` should be {type_names[0]},'
                        f' but got {get_typename(arg_type)}.')
    raise TypeError(f'The type of `{arg_name}` should be one of {type_names},'
                    f' but got {get_typename(arg_type)}.')


def check_shape(arg_name, arg_value):
    """Check shape."""
    # First, check if shape is a tuple
    if not isinstance(arg_value, tuple):
        raise TypeError(f'The type of `{arg_name}` should be one of {tuple.__name__},'
                        f' but got {type(arg_value).__name__}.')

    # Second, wrap arg_value with numpy array so that it can be checked through numpy api
    arg_value = np.array(arg_value)

    # shape can not be ()
    if arg_value.size == 0:
        raise ValueError('Shape can not be empty.')

    # shape's dimension should be 1
    if arg_value.ndim != 1:
        raise ValueError('Shape of tensor should be 1-dim vector, but got {}-dim.'.format(arg_value.ndim))

    # Thirdly, check each element's type of the shape
    valid_types = (int, np.int8, np.int16, np.int32, np.int64,
                   np.uint8, np.uint16, np.uint32, np.uint64)
    for dim_size in arg_value:
        if not isinstance(dim_size, valid_types) or dim_size <= 0:
            raise ValueError('Every dimension size of the tensor shape should be a positive integer,'
                             ' but got {}.'.format(dim_size))


def _check_str_by_regular(target, reg=None, flag=re.ASCII):
    if reg is None:
        reg = _name_re
    if re.match(reg, target, flag) is None:
        raise ValueError("'{}' is illegal, it should be match regular'{}' by flags'{}'".format(target, reg, flag))
    return True


def args_type_check(*type_args, **type_kwargs):
    """Check whether input data type is correct."""

    def type_check(func):
        sig = inspect.signature(func)
        bound_types = sig.bind_partial(*type_args, **type_kwargs).arguments

        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal bound_types
            bound_values = sig.bind(*args, **kwargs)
            argument_dict = bound_values.arguments
            if "kwargs" in bound_types:
                bound_types = bound_types["kwargs"]
            if "kwargs" in argument_dict:
                argument_dict = argument_dict["kwargs"]
            for name, value in argument_dict.items():
                if name in bound_types:
                    if value is not None and not isinstance(value, bound_types[name]):
                        raise TypeError('Argument {} must be {}'.format(name, bound_types[name]))
            return func(*args, **kwargs)

        return wrapper

    return type_check
