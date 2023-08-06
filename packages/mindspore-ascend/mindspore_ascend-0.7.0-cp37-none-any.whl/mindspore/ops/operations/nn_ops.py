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

"""Operators for nn."""

import math
import operator
from functools import reduce

import numpy as np

from ... import context
from ..._c_expression import signature_rw as sig_rw
from ..._c_expression import signature_kind as sig_kind
from ..._c_expression import signature_dtype as sig_dtype
from ..._checkparam import Validator as validator
from ..._checkparam import Rel
from ...common import dtype as mstype
from ..primitive import Primitive, PrimitiveWithInfer, prim_attr_register
from ..operations.math_ops import _infer_shape_reduce


def _check_positive_int_or_tuple(arg_name, arg_value, prim_name, allow_four=False, ret_four=False):
    """
    Checks whether an argument is a positive int or tuple with 2 or 4(when allow_four is True) positive int elements.
    """

    def _raise_message():
        raise ValueError(f"For '{prim_name}' attr '{arg_name}' should be an positive int number or a tuple of two "
                         f"{'or four ' if allow_four else ''}positive int numbers, but got {arg_value}")

    def _get_return_value():
        if isinstance(arg_value, int):
            ret = (1, 1, arg_value, arg_value) if ret_four else (arg_value, arg_value)
        elif len(arg_value) == 2:
            ret = (1, 1, arg_value[0], arg_value[1]) if ret_four else arg_value
        elif len(arg_value) == 4:
            if not allow_four:
                _raise_message()
            ret = arg_value if ret_four else (arg_value[2], arg_value[3])
        else:
            _raise_message()
        return ret

    validator.check_value_type(arg_name, arg_value, (int, tuple), prim_name)
    ret_value = _get_return_value()
    for item in ret_value:
        if isinstance(item, int) and item > 0:
            continue
        _raise_message()
    return ret_value


class Flatten(PrimitiveWithInfer):
    r"""
    Flattens a tensor without changing its batch size on the 0-th axis.

    Inputs:
        - **input_x** (Tensor) - Tensor of shape :math:`(N, \ldots)` to be flattened.

    Outputs:
        Tensor, the shape of the output tensor is :math:`(N, X)`, where :math:`X` is
        the product of the remaining dimension.

    Examples:
        >>> input_tensor = Tensor(np.ones(shape=[1, 2, 3, 4]), mindspore.float32)
        >>> flatten = P.Flatten()
        >>> output = flatten(input_tensor)
        >>> assert output.shape == (1, 24)
    """

    @prim_attr_register
    def __init__(self):
        pass

    def infer_shape(self, input_x):
        validator.check_integer('input_x rank', len(input_x), 1, Rel.GE, self.name)
        prod = 1 if len(input_x) == 1 else reduce(operator.mul, input_x[1:])
        return input_x[0], prod

    def infer_dtype(self, input_x):
        validator.check_subclass("input_x", input_x, mstype.tensor, self.name)
        return input_x


class Softmax(PrimitiveWithInfer):
    r"""
    Softmax operation.

    Applies the Softmax operation to the input tensor on the specified axis.
    Suppose a slice in the given aixs :math:`x` then for each element :math:`x_i`
    the Softmax function is shown as follows:

    .. math::
        \text{output}(x_i) = \frac{exp(x_i)}{\sum_{j = 0}^{N-1}\exp(x_j)},

    where :math:`N` is the length of the tensor.

    Args:
        axis (Union[int, tuple]): The axis to do the Softmax operation. Default: -1.

    Inputs:
        - **logits** (Tensor) - The input of Softmax, with float16 or float32 data type.

    Outputs:
        Tensor, with the same type and shape as the logits.

    Examples:
        >>> input_x = Tensor(np.array([1, 2, 3, 4, 5]), mindspore.float32)
        >>> softmax = P.Softmax()
        >>> softmax(input_x)
        [0.01165623, 0.03168492, 0.08612854, 0.23412167, 0.6364086]
    """

    @prim_attr_register
    def __init__(self, axis=-1):
        self.init_prim_io_names(inputs=['x'], outputs=['output'])
        validator.check_value_type("axis", axis, [int, tuple], self.name)
        if isinstance(axis, int):
            self.add_prim_attr('axis', (axis,))
        for item in self.axis:
            validator.check_value_type("item of axis", item, [int], self.name)

    def infer_shape(self, logits):
        validator.check_integer("length of axis", len(self.axis), 1, Rel.GE, self.name)
        rank = len(logits)
        for axis_v in self.axis:
            validator.check_int_range("axis", axis_v, -rank, rank, Rel.INC_LEFT, self.name)
        return logits

    def infer_dtype(self, logits):
        validator.check_subclass("logits", logits, mstype.tensor, self.name)
        validator.check_tensor_type_same({"logits": logits}, mstype.float_type, self.name)
        return logits


class LogSoftmax(PrimitiveWithInfer):
    r"""
    Log Softmax activation function.

    Applies the Log Softmax function to the input tensor on the specified axis.
    Suppose a slice in the given aixs :math:`x` then for each element :math:`x_i`
    the Log Softmax function is shown as follows:

    .. math::
        \text{output}(x_i) = \log \left(\frac{exp(x_i)} {\sum_{j = 0}^{N-1}\exp(x_j)}\right),

    where :math:`N` is the length of the Tensor.

    Args:
        axis (int): The axis to do the Log softmax operation. Default: -1.

    Inputs:
        - **logits** (Tensor) - The input of Log Softmax, with float16 or float32 data type.

    Outputs:
        Tensor, with the same type and shape as the logits.

    Examples:
        >>> input_x = Tensor(np.array([1, 2, 3, 4, 5]), mindspore.float32)
        >>> log_softmax = P.LogSoftmax()
        >>> log_softmax(input_x)
        [-4.4519143, -3.4519143, -2.4519143, -1.4519144, -0.4519144]
    """

    @prim_attr_register
    def __init__(self, axis=-1):
        validator.check_value_type("axis", axis, [int], self.name)

    def infer_shape(self, logits):
        rank = len(logits)
        validator.check_int_range('axis', self.axis, -rank, rank, Rel.INC_LEFT, self.name)
        return logits

    def infer_dtype(self, logits):
        validator.check_subclass("logits", logits, mstype.tensor, self.name)
        validator.check_tensor_type_same({"logits": logits}, mstype.float_type, self.name)
        return logits


class Softplus(PrimitiveWithInfer):
    r"""
    Softplus activation function.

    Softplus is a smooth approximation to the ReLU function.
    The function is shown as follows:

    .. math::
        \text{output} = \log(1 + \exp(\text{input_x})),

    Inputs:
        - **input_x** (Tensor) - The input tensor whose data type should be float.

    Outputs:
        Tensor, with the same type and shape as the `input_x`.

    Examples:
        >>> input_x = Tensor(np.array([1, 2, 3, 4, 5]), mindspore.float32)
        >>> softplus = P.Softplus()
        >>> softplus(input_x)
        [1.3132615, 2.126928, 3.0485873, 4.01815, 5.0067153]
    """

    @prim_attr_register
    def __init__(self):
        """init Softplus"""
        self.init_prim_io_names(inputs=['x'], outputs=['output'])

    def infer_shape(self, input_x):
        return input_x

    def infer_dtype(self, input_x):
        validator.check_tensor_type_same({'input_x': input_x}, mstype.float_type, self.name)
        return input_x


class Softsign(PrimitiveWithInfer):
    r"""
    Softsign activation function.

    The function is shown as follows:

    .. math::
        \text{output} = \frac{\text{input_x}}{1 + \abs{\text{input_x}}},

    Inputs:
        - **input_x** (Tensor) - The input tensor whose data type should be float16 or float32.

    Outputs:
        Tensor, with the same type and shape as the `input_x`.

    Examples:
        >>> input_x = Tensor(np.array([0, -1, 2, 30, -30]), mindspore.float32)
        >>> softsign = P.Softsign()
        >>> softsign(input_x)
        [0. -0.5 0.6666667 0.9677419 -0.9677419]
    """

    @prim_attr_register
    def __init__(self):
        """init Softsign"""
        self.init_prim_io_names(inputs=['x'], outputs=['output'])

    def infer_shape(self, input_x):
        return input_x

    def infer_dtype(self, input_x):
        validator.check_tensor_type_same({'input_x': input_x}, [mstype.float16, mstype.float32], self.name)
        return input_x


class ReLU(PrimitiveWithInfer):
    r"""
    Computes ReLU(Rectified Linear Unit) of input tensor element-wise.

    It returns :math:`\max(x,\  0)` element-wise.

    Inputs:
        - **input_x** (Tensor) - The input tensor.

    Outputs:
        Tensor, with the same type and shape as the `input_x`.

    Examples:
        >>> input_x = Tensor(np.array([[-1.0, 4.0, -8.0], [2.0, -5.0, 9.0]]), mindspore.float32)
        >>> relu = P.ReLU()
        >>> result = relu(input_x)
        [[0, 4.0, 0.0], [2.0, 0.0, 9.0]]
    """

    @prim_attr_register
    def __init__(self):
        """init ReLU"""
        self.init_prim_io_names(inputs=['x'], outputs=['output'])

    def infer_shape(self, input_x):
        return input_x

    def infer_dtype(self, input_x):
        validator.check_tensor_type_same({'input_x': input_x}, mstype.number_type, self.name)
        return input_x


class ReLU6(PrimitiveWithInfer):
    r"""
    Computes ReLU(Rectified Linear Unit) upper bounded by 6 of input tensor element-wise.

    It returns :math:`\min(\max(0,x), 6)` element-wise.

    Inputs:
        - **input_x** (Tensor) - The input tensor. With float16 or float32 data type.

    Outputs:
        Tensor, with the same type and shape as the `input_x`.

    Examples:
        >>> input_x = Tensor(np.array([[-1.0, 4.0, -8.0], [2.0, -5.0, 9.0]]), mindspore.float32)
        >>> relu6 = P.ReLU6()
        >>> result = relu6(input_x)
    """

    @prim_attr_register
    def __init__(self):
        """init ReLU6"""
        self.init_prim_io_names(inputs=['x'], outputs=['output'])

    def infer_shape(self, input_x):
        return input_x

    def infer_dtype(self, input_x):
        validator.check_tensor_type_same({'input_x': input_x}, (mstype.float16, mstype.float32), self.name)
        return input_x


class ReLUV2(PrimitiveWithInfer):
    r"""
    Computes ReLU(Rectified Linear Unit) of input tensor element-wise.

    It returns :math:`\max(x,\  0)` element-wise.

    Inputs:
        - **input_x** (Tensor) - The input tensor should be a 4-D tensor.

    Outputs:
        - **output** (Tensor) - Has the same type and shape as the `input_x`.
        - **mask** (Tensor) - A tensor whose data type must be uint8.

    Examples:
        >>> input_x = Tensor(np.array([[[[1, -2], [-3, 4]], [[-5, 6], [7, -8]]]]), mindspore.float32)
        >>> relu_v2 = P.ReLUV2()
        >>> output = relu_v2(input_x)
        ([[[[1., 0.], [0., 4.]], [[0., 6.], [7., 0.]]]],
         [[[[1, 0], [2, 0]], [[2, 0], [1, 0]]]])
    """

    @prim_attr_register
    def __init__(self):
        """init ReLUV2"""
        self.init_prim_io_names(inputs=['x'], outputs=['output', 'mask'])

    def __infer__(self, input_x):
        input_shape = list(input_x['shape'])
        input_dtype = input_x['dtype']
        mask_shape = []
        if len(input_shape) != 4:
            raise ValueError("The `input_x` should be a 4-D tensor, "
                             f"but got a {len(input_shape)}-D tensor whose shape is {input_shape}")
        for i in enumerate(input_shape):
            if i[0] == 1:
                if input_dtype == mstype.uint8 and input_dtype == mstype.int8:
                    mask_shape.append((input_shape[1] + 31) // 32)
                else:
                    mask_shape.append((input_shape[1] + 15) // 16)
            else:
                mask_shape.append(i[1])
        if input_dtype == mstype.uint8 and input_dtype == mstype.int8:
            mask_shape.append(4)
        else:
            mask_shape.append(2)

        output_shape = (input_x['shape'], mask_shape)
        validator.check_subclass("input_x", input_dtype, mstype.tensor, self.name)
        validator.check_tensor_type_same({'input_x': input_dtype}, mstype.number_type, self.name)
        mask_dtype = mstype.uint8
        output_dtype = (input_dtype, mask_dtype)

        return {'shape': output_shape,
                'dtype': output_dtype,
                'value': None}


class Elu(PrimitiveWithInfer):
    r"""
    Computes exponential linear: `alpha * (exp(x) - 1)` if x < 0, `x` otherwise.
    The data type of input tensor should be float.

    Args:
        alpha (float): The coefficient of negative factor whose type is float,
            only support '1.0' currently. Default: 1.0.

    Inputs:
        - **input_x** (Tensor) - The input tensor whose data type should be float.

    Outputs:
        Tensor, has the same shape and data type as `input_x`.

    Examples:
        >>> input_x = Tensor(np.array([[-1.0, 4.0, -8.0], [2.0, -5.0, 9.0]]), mindspore.float32)
        >>> elu = P.Elu()
        >>> result = elu(input_x)
        Tensor([[-0.632  4.0   -0.999]
                [2.0    -0.993  9.0  ]], shape=(2, 3), dtype=mindspore.float32)
    """

    @prim_attr_register
    def __init__(self, alpha=1.0):
        """Init Elu"""
        validator.check_value_type("alpha", alpha, [float], self.name)
        validator.check_number("alpha", alpha, 1.0, Rel.EQ, self.name)

    def infer_shape(self, input_x):
        return input_x

    def infer_dtype(self, input_x):
        validator.check_tensor_type_same({'input_x': input_x}, mstype.float_type, self.name)
        return input_x


class HSwish(PrimitiveWithInfer):
    r"""
    Hard swish activation function.

    Applies hswish-type activation element-wise. The input is a Tensor with any valid shape.

    Hard swish is defined as:

    .. math::
        \text{hswish}(x_{i}) = x_{i} * \frac{ReLU6(x_{i} + 3)}{6},

    where :math:`x_{i}` is the :math:`i`-th slice in the given dimension of the input Tensor.

    Inputs:
        - **input_data** (Tensor) - The input of HSwish, data type should be float16 or float32.

    Outputs:
        Tensor, with the same type and shape as the `input_data`.

    Examples:
        >>> hswish = P.HSwish()
        >>> input_x = Tensor(np.array([-1, -2, 0, 2, 1]), mindspore.float16)
        >>> result = hswish(input_x)
    """

    @prim_attr_register
    def __init__(self):
        self.init_prim_io_names(inputs=['x'], outputs=['output'])

    def infer_shape(self, xshape):
        return xshape

    def infer_dtype(self, x_dtype):
        validator.check_tensor_type_same({"x": x_dtype}, (mstype.float16, mstype.float32), self.name)
        return x_dtype


class Sigmoid(PrimitiveWithInfer):
    r"""
    Sigmoid activation function.

    Computes Sigmoid of input element-wise. The Sigmoid function is defined as:

    .. math::
        \text{sigmoid}(x_i) = \frac{1}{1 + exp(-x_i)},

    where :math:`x_i` is the element of the input.

    Inputs:
        - **input_x** (Tensor) - The input of Sigmoid, data type should be float16 or float32.

    Outputs:
        Tensor, with the same type and shape as the input_x.

    Examples:
        >>> input_x = Tensor(np.array([1, 2, 3, 4, 5]), mindspore.float32)
        >>> sigmoid = P.Sigmoid()
        >>> sigmoid(input_x)
        [0.73105866, 0.880797, 0.9525742, 0.98201376, 0.9933071]
    """

    @prim_attr_register
    def __init__(self):
        self.init_prim_io_names(inputs=['x'], outputs=['output'])

    def infer_shape(self, input_x):
        return input_x

    def infer_dtype(self, input_x):
        validator.check_tensor_type_same({"input_x": input_x}, (mstype.float16, mstype.float32), self.name)
        return input_x


class HSigmoid(PrimitiveWithInfer):
    r"""
    Hard sigmoid activation function.

    Applies hard sigmoid activation element-wise. The input is a Tensor with any valid shape.

    Hard sigmoid is defined as:

    .. math::
        \text{hsigmoid}(x_{i}) = max(0, min(1, \frac{x_{i} + 3}{6})),

    where :math:`x_{i}` is the :math:`i`-th slice in the given dimension of the input Tensor.

    Inputs:
        - **input_data** (Tensor) - The input of HSigmoid, data type should be float16 or float32.

    Outputs:
        Tensor, with the same type and shape as the `input_data`.

    Examples:
        >>> hsigmoid = P.HSigmoid()
        >>> input_x = Tensor(np.array([-1, -2, 0, 2, 1]), mindspore.float16)
        >>> result = hsigmoid(input_x)
    """

    @prim_attr_register
    def __init__(self):
        self.init_prim_io_names(inputs=['x'], outputs=['output'])

    def infer_shape(self, x_shape):
        return x_shape

    def infer_dtype(self, x_dtype):
        validator.check_tensor_type_same({"x": x_dtype}, (mstype.float16, mstype.float32), self.name)
        return x_dtype


class Tanh(PrimitiveWithInfer):
    r"""
    Tanh activation function.

    Computes hyperbolic tangent of input element-wise. The Tanh function is defined as:

    .. math::
        tanh(x_i) = \frac{\exp(x_i) - \exp(-x_i)}{\exp(x_i) + \exp(-x_i)} = \frac{\exp(2x_i) - 1}{\exp(2x_i) + 1},

    where :math:`x_i` is an element of the input Tensor.

    Inputs:
        - **input_x** (Tensor) - The input of Tanh.

    Outputs:
        Tensor, with the same type and shape as the input_x.

    Examples:
        >>> input_x = Tensor(np.array([1, 2, 3, 4, 5]), mindspore.float32)
        >>> tanh = P.Tanh()
        >>> tanh(input_x)
        [0.7615941, 0.9640276, 0.9950548, 0.9993293, 0.99990916]
    """

    @prim_attr_register
    def __init__(self):
        pass

    def infer_shape(self, input_x):
        return input_x

    def infer_dtype(self, input_x):
        validator.check_subclass("input_x", input_x, mstype.tensor, self.name)
        return input_x


class FusedBatchNorm(Primitive):
    r"""
    FusedBatchNorm is a BatchNorm that moving mean and moving variance will be computed instead of being loaded.

    Batch Normalization is widely used in convolutional networks. This operation applies
    Batch Normalization over input to avoid internal covariate shift as described in the
    paper `Batch Normalization: Accelerating Deep Network Training by Reducing Internal
    Covariate Shift <https://arxiv.org/abs/1502.03167>`_. It rescales and recenters the
    feature using a mini-batch of data and the learned parameters which can be described
    in the following formula.

    .. math::
        y = \frac{x - mean}{\sqrt{variance + \epsilon}} * \gamma + \beta

    where :math:`\gamma` is scale, :math:`\beta` is bias, :math:`\epsilon` is epsilon.

    Args:
        mode (int): Mode of batch normalization, value is 0 or 1. Default: 0.
        epsilon (float): A small value added for numerical stability. Default: 1e-5.
        momentum (float): The hyper parameter to compute moving average for running_mean and running_var
            (e.g. :math:`new\_running\_mean = momentum * running\_mean + (1 - momentum) * current\_mean`).
            Momentum value should be [0, 1]. Default: 0.9.

    Inputs:
        - **input_x** (Tensor) - Tensor of shape :math:`(N, C)`.
        - **scale** (Tensor) - Tensor of shape :math:`(C,)`.
        - **bias** (Tensor) - Tensor of shape :math:`(C,)`.
        - **mean** (Tensor) - Tensor of shape :math:`(C,)`.
        - **variance** (Tensor) - Tensor of shape :math:`(C,)`.

    Outputs:
        Tuple of 5 Tensor, the normalized input and the updated parameters.

        - **output_x** (Tensor) - The same type and shape as the `input_x`.
        - **updated_scale** (Tensor) - Tensor of shape :math:`(C,)`.
        - **updated_bias** (Tensor) - Tensor of shape :math:`(C,)`.
        - **updated_moving_mean** (Tensor) - Tensor of shape :math:`(C,)`.
        - **updated_moving_variance** (Tensor) - Tensor of shape :math:`(C,)`.

    Examples:
        >>> input_x = Tensor(np.ones([128, 64, 32, 64]), mindspore.float32)
        >>> scale = Tensor(np.ones([64]), mindspore.float32)
        >>> bias = Tensor(np.ones([64]), mindspore.float32)
        >>> mean = Tensor(np.ones([64]), mindspore.float32)
        >>> variance = Tensor(np.ones([64]), mindspore.float32)
        >>> op = P.FusedBatchNorm()
        >>> output = op(input_x, scale, bias, mean, variance)
    """

    @prim_attr_register
    def __init__(self, mode=0, epsilon=1e-5, momentum=0.1):
        self.init_prim_io_names(inputs=['x', 'scale', 'b', 'mean', 'variance'],
                                outputs=['y', 'running_mean', 'running_variance', 'save_mean', 'save_inv_variance'])
        self.mode = validator.check_integer('mode', mode, [0, 1], Rel.IN, self.name)
        self.epsilon = validator.check_number_range('epsilon', epsilon, 0, 1, Rel.INC_RIGHT, self.name)
        self.momentum = validator.check_number_range('momentum', momentum, 0, 1, Rel.INC_BOTH, self.name)
        self._update_parameter = True


class FusedBatchNormEx(PrimitiveWithInfer):
    r"""
    FusedBatchNormEx is an extension of FusedBatchNorm, FusedBatchNormEx has one more output(output reserve)
    than FusedBatchNorm, reserve will be used in backpropagation phase. FusedBatchNorm is a BatchNorm that
    moving mean and moving variance will be computed instead of being loaded.

    Batch Normalization is widely used in convolutional networks. This operation applies
    Batch Normalization over input to avoid internal covariate shift as described in the
    paper `Batch Normalization: Accelerating Deep Network Training by Reducing Internal
    Covariate Shift <https://arxiv.org/abs/1502.03167>`_. It rescales and recenters the
    feature using a mini-batch of data and the learned parameters which can be described
    in the following formula.

    .. math::
        y = \frac{x - mean}{\sqrt{variance + \epsilon}} * \gamma + \beta

    where :math:`\gamma` is scale, :math:`\beta` is bias, :math:`\epsilon` is epsilon.

    Args:
        mode (int): Mode of batch normalization, value is 0 or 1. Default: 0.
        epsilon (float): A small value added for numerical stability. Default: 1e-5.
        momentum (float): The hyper parameter to compute moving average for running_mean and running_var
            (e.g. :math:`new\_running\_mean = momentum * running\_mean + (1 - momentum) * current\_mean`).
            Momentum value should be [0, 1]. Default: 0.9.

    Inputs:
        - **input_x** (Tensor) - The input of FusedBatchNormEx, Tensor of shape :math:`(N, C)`,
                                 data type: float16 or float32.
        - **scale** (Tensor) - Parameter scale, same with gamma above-mentioned, Tensor of shape :math:`(C,)`,
                               data type: float32.
        - **bias** (Tensor) - Parameter bias, same with beta above-mentioned, Tensor of shape :math:`(C,)`,
                              data type: float32.
        - **mean** (Tensor) - mean value, Tensor of shape :math:`(C,)`, data type: float32.
        - **variance** (Tensor) - variance value, Tensor of shape :math:`(C,)`, data type: float32.

    Outputs:
        Tuple of 6 Tensor, the normalized input, the updated parameters and reserve.

        - **output_x** (Tensor) - The input of FusedBatchNormEx, same type and shape as the `input_x`.
        - **updated_scale** (Tensor) - Updated parameter scale, Tensor of shape :math:`(C,)`, data type: float32.
        - **updated_bias** (Tensor) - Updated parameter bias, Tensor of shape :math:`(C,)`, data type: float32.
        - **updated_moving_mean** (Tensor) - Updated mean value, Tensor of shape :math:`(C,)`, data type: float32.
        - **updated_moving_variance** (Tensor) - Updated variance value, Tensor of shape :math:`(C,)`,
                                                 data type: float32.
        - **reserve** (Tensor) - reserve space, Tensor of shape :math:`(C,)`, data type: float32.

    Examples:
        >>> input_x = Tensor(np.ones([128, 64, 32, 64]), mindspore.float32)
        >>> scale = Tensor(np.ones([64]), mindspore.float32)
        >>> bias = Tensor(np.ones([64]), mindspore.float32)
        >>> mean = Tensor(np.ones([64]), mindspore.float32)
        >>> variance = Tensor(np.ones([64]), mindspore.float32)
        >>> op = P.FusedBatchNormEx()
        >>> output = op(input_x, scale, bias, mean, variance)
    """
    __mindspore_signature__ = (
        ('input_x', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T2),
        ('scale', sig_rw.RW_WRITE, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('bias', sig_rw.RW_WRITE, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('mean', sig_rw.RW_WRITE, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('variance', sig_rw.RW_WRITE, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
    )

    @prim_attr_register
    def __init__(self, mode=0, epsilon=1e-5, momentum=0.1):
        self.init_prim_io_names(inputs=['x', 'scale', 'b', 'mean', 'variance'],
                                outputs=['y', 'save_scale', 'save_bias', 'save_mean', 'save_inv_variance', 'reserve'])
        self.mode = validator.check_integer('mode', mode, [0, 1], Rel.IN, self.name)
        self.epsilon = validator.check_number_range('epsilon', epsilon, 0, 1, Rel.INC_RIGHT, self.name)
        self.momentum = validator.check_number_range('momentum', momentum, 0, 1, Rel.INC_BOTH, self.name)
        self._update_parameter = True
        self.add_prim_attr('data_format', "NCHW")

    def infer_shape(self, input_x, scale, bias, mean, variance):
        validator.check_integer("scale rank", len(scale), 1, Rel.EQ, self.name)
        validator.check("scale shape", scale, "bias shape", bias, Rel.EQ, self.name)
        validator.check("scale shape[0]", scale[0], "input_x shape[1]", input_x[1], Rel.EQ, self.name)
        validator.check_integer("mean rank", len(mean), 1, Rel.EQ, self.name)
        validator.check("mean shape", mean, "variance shape", variance, Rel.EQ, self.name)
        validator.check("mean shape", mean, "scale shape", scale, Rel.EQ, self.name)
        return (input_x, scale, scale, scale, scale, scale)

    def infer_dtype(self, input_x, scale, bias, mean, variance):
        validator.check_tensor_type_same({"input_x": input_x}, [mstype.float16, mstype.float32], self.name)
        args = {"scale": scale, "bias": bias}
        validator.check_tensor_type_same(args, [mstype.float32], self.name)
        args_moving = {"mean": mean, "variance": variance}
        valid_types = [mstype.tensor_type(mstype.float32)]
        validator.check_type_same(args_moving, valid_types, self.name)
        return (input_x, scale, scale, scale, scale, scale)


class BNTrainingReduce(PrimitiveWithInfer):
    """
    reduce sum at axis [0, 2, 3].

    Inputs:
        - **x** (Tensor)  - Tensor of shape :math:`(N, C)`.

    Outputs:
        - **sum** (Tensor) - Tensor of shape :math:`(C,)`.
        - **square_sum** (Tensor) - Tensor of shape :math:`(C,)`.

    """

    @prim_attr_register
    def __init__(self):
        self.init_prim_io_names(inputs=['x'], outputs=['sum', 'square_sum'])

    def infer_shape(self, x_shape):
        validator.check_integer("x rank", len(x_shape), 4, Rel.EQ, self.name)
        return ([x_shape[1]], [x_shape[1]])

    def infer_dtype(self, x_type):
        return (x_type, x_type)


class BNTrainingUpdate(PrimitiveWithInfer):
    """
    primitive operator of bn_training_update's register and info descriptor
    """
    @prim_attr_register
    def __init__(self, isRef=True, epsilon=1e-5, factor=0.1):
        self.init_prim_io_names(inputs=['x', 'sum', 'square_sum', 'scale', 'b', 'mean', 'variance'],
                                outputs=['y', 'running_mean', 'running_variance', 'save_mean', 'save_inv_variance'])
        #self.isRef = validator.check_integer('isRef', isRef, [0, 1], Rel.IN)
        self.epsilon = validator.check_number_range('epsilon', epsilon, 0, 1, Rel.INC_RIGHT, 'BNTrainingUpdate')
        self.factor = validator.check_number_range('factor', factor, 0, 1, Rel.INC_BOTH, 'BNTrainingUpdate')

    def infer_shape(self, x, sum, square_sum, scale, b, mean, variance):
        return (x, variance, variance, variance, variance)

    def infer_dtype(self, x, sum, square_sum, scale, b, mean, variance):
        return (x, variance, variance, variance, variance)


class BatchNorm(PrimitiveWithInfer):
    r"""
    Batch Normalization for input data and updated parameters.

    Batch Normalization is widely used in convolutional neural networks. This operation
    applies Batch Normalization over input to avoid internal covariate shift as described
    in the paper `Batch Normalization: Accelerating Deep Network Training by Reducing Internal
    Covariate Shift <https://arxiv.org/abs/1502.03167>`_. It rescales and recenters the
    features using a mini-batch of data and the learned parameters which can be described
    in the following formula,

    .. math::
        y = \frac{x - mean}{\sqrt{variance + \epsilon}} * \gamma + \beta

    where :math:`\gamma` is scale, :math:`\beta` is bias, :math:`\epsilon` is epsilon.

    Args:
        is_training (bool): If `is_training` is True, `mean` and `variance` are computed during training.
            If `is_training` is False, they're loaded from checkpoint during inference. Default: False.
        epsilon (float): A small value added for numerical stability. Default: 1e-5.

    Inputs:
        - **input_x** (Tensor) - Tensor of shape :math:`(N, C)`, with float16 or float32 data type.
        - **scale** (Tensor) - Tensor of shape :math:`(C,)`, with float16 or float32 data type.
        - **bias** (Tensor) - Tensor of shape :math:`(C,)`, has the same data type with `scale`.
        - **mean** (Tensor) - Tensor of shape :math:`(C,)`, with float16 or float32 data type.
        - **variance** (Tensor) - Tensor of shape :math:`(C,)`, has the same data type with `mean`.

    Outputs:
        Tuple of 5 Tensor, the normalized inputs and the updated parameters.

        - **output_x** (Tensor) - The same type and shape as the input_x. The shape is :math:`(N, C)`.
        - **updated_scale** (Tensor) - Tensor of shape :math:`(C,)`.
        - **updated_bias** (Tensor) - Tensor of shape :math:`(C,)`.
        - **reserve_space_1** (Tensor) - Tensor of shape :math:`(C,)`.
        - **reserve_space_2** (Tensor) - Tensor of shape :math:`(C,)`.

    Examples:
        >>> input_x = Tensor(np.ones([128, 64, 32, 64]), mindspore.float32)
        >>> scale = Tensor(np.ones([64]), mindspore.float32)
        >>> bias = Tensor(np.ones([64]), mindspore.float32)
        >>> mean = Tensor(np.ones([64]), mindspore.float32)
        >>> variance = Tensor(np.ones([64]), mindspore.float32)
        >>> batch_norm = P.BatchNorm()
        >>> output = batch_norm(input_x, scale, bias, mean, variance)
    """

    @prim_attr_register
    def __init__(self, is_training=False, epsilon=1e-5):
        validator.check_value_type('is_training', is_training, (bool,), self.name)
        validator.check_number_range('epsilon', epsilon, 0, 1, Rel.INC_RIGHT, self.name)
        self.add_prim_attr('data_format', "NCHW")
        self.init_prim_io_names(inputs=['x', 'scale', 'offset', 'mean', 'variance'],
                                outputs=['y', 'batch_mean', 'batch_variance', 'reserve_space_1', 'reserve_space_2'])

    def infer_shape(self, input_x, scale, bias, mean, variance):
        validator.check_integer("scale rank", len(scale), 1, Rel.EQ, self.name)
        validator.check("scale shape", scale, "bias shape", bias, Rel.EQ, self.name)
        validator.check("scale shape[0]", scale[0], "input_x shape[1]", input_x[1], Rel.EQ, self.name)
        if not self.is_training:
            validator.check_integer("mean rank", len(mean), 1, Rel.EQ, self.name)
            validator.check("mean shape", mean, "variance shape", variance, Rel.EQ, self.name)
            validator.check("mean shape", mean, "scale shape", scale, Rel.EQ, self.name)
        return (input_x, scale, scale, scale, scale)

    def infer_dtype(self, input_x, scale, bias, mean, variance):
        validator.check_tensor_type_same({"input_x": input_x}, [mstype.float16, mstype.float32], self.name)
        args = {"scale": scale, "bias": bias}
        validator.check_tensor_type_same(args, [mstype.float16, mstype.float32], self.name)
        args_moving = {"mean": mean, "variance": variance}
        if self.is_training:
            valid_types = [mstype.tensor_type(mstype.float16), mstype.tensor_type(mstype.float32), None]
            validator.check_type_same(args_moving, valid_types, self.name)
        else:
            args_moving = {"mean": mean, "variance": variance}
            validator.check_tensor_type_same(args_moving, [mstype.float16, mstype.float32], self.name)
        return (input_x, scale, bias, input_x, input_x)


class Conv2D(PrimitiveWithInfer):
    r"""
    2D convolution layer.

    Applies a 2D convolution over an input tensor which is typically of shape :math:`(N, C_{in}, H_{in}, W_{in})`,
    where :math:`N` is batch size and :math:`C_{in}` is channel number. For each batch of shape
    :math:`(C_{in}, H_{in}, W_{in})`, the formula is defined as:

    .. math::

        out_j = \sum_{i=0}^{C_{in} - 1} ccor(W_{ij}, X_i) + b_j,

    where :math:`ccor` is the cross correlation operator, :math:`C_{in}` is the input channel number, :math:`j` ranges
    from :math:`0` to :math:`C_{out} - 1`, :math:`W_{ij}` corresponds to the :math:`i`-th channel of the :math:`j`-th
    filter and :math:`out_{j}` corresponds to the :math:`j`-th channel of the output. :math:`W_{ij}` is a slice
    of kernel and it has shape :math:`(\text{ks_h}, \text{ks_w})`, where :math:`\text{ks_h}` and
    :math:`\text{ks_w}` are the height and width of the convolution kernel. The full kernel has shape
    :math:`(C_{out}, C_{in} // \text{group}, \text{ks_h}, \text{ks_w})`, where group is the group number
    to split the input in the channel dimension.

    If the 'pad_mode' is set to be "valid", the output height and width will be
    :math:`\left \lfloor{1 + \frac{H_{in} + 2 \times \text{padding} - \text{ks_h} -
    (\text{ks_h} - 1) \times (\text{dilation} - 1) }{\text{stride}}} \right \rfloor` and
    :math:`\left \lfloor{1 + \frac{W_{in} + 2 \times \text{padding} - \text{ks_w} -
    (\text{ks_w} - 1) \times (\text{dilation} - 1) }{\text{stride}}} \right \rfloor` respectively.


    The first introduction can be found in paper `Gradient Based Learning Applied to Document Recognition
    <http://vision.stanford.edu/cs598_spring07/papers/Lecun98.pdf>`_. More detailed introduction can be found here:
    http://cs231n.github.io/convolutional-networks/.

    Args:
        out_channel (int): The dimension of the output.
        kernel_size (Union[int, tuple[int]]): The kernel size of the 2D convolution.
        mode (int): 0 Math convolutiuon, 1 cross-correlation convolution ,
                       2 deconvolution, 3 depthwise convolution. Default: 1.
        pad_mode (str): "valid", "same", "pad" the mode to fill padding. Default: "valid".
        pad (Union(int, tuple[int])): The pad value to fill. Default: 0. If `pad` is one integer, the padding of
                    top, bottom, left and right is same, equal to pad. If `pad` is tuple with four integer, the padding
                    of top, bottom, left and right equal to pad[0], pad[1], pad[2], pad[3] with corresponding.
        stride (Union(int, tuple[int])): The stride to apply conv filter. Default: 1.
        dilation (Union(int, tuple[int])): Specify the space to use between kernel elements. Default: 1.
        group (int): Split input into groups. Default: 1.

    Returns:
        Tensor, the value that applied 2D convolution.

    Inputs:
        - **input** (Tensor) - Tensor of shape :math:`(N, C_{in}, H_{in}, W_{in})`.
        - **weight** (Tensor) - Set size of kernel is :math:`(K_1, K_2)`, then the shape is
          :math:`(C_{out}, C_{in}, K_1, K_2)`.

    Outputs:
        Tensor of shape :math:`(N, C_{out}, H_{out}, W_{out})`.

    Examples:
        >>> input = Tensor(np.ones([10, 32, 32, 32]), mindspore.float32)
        >>> weight = Tensor(np.ones([32, 32, 3, 3]), mindspore.float32)
        >>> conv2d = P.Conv2D(out_channel=32, kernel_size=3)
        >>> conv2d(input, weight)
    """

    @prim_attr_register
    def __init__(self,
                 out_channel,
                 kernel_size,
                 mode=1,
                 pad_mode="valid",
                 pad=0,
                 stride=1,
                 dilation=1,
                 group=1):
        """init Conv2D"""
        self.init_prim_io_names(inputs=['x', 'w'], outputs=['output'])
        self.kernel_size = _check_positive_int_or_tuple('kernel_size', kernel_size, self.name)
        self.stride = _check_positive_int_or_tuple('stride', stride, self.name, allow_four=True, ret_four=True)
        self.add_prim_attr('stride', self.stride)
        self.dilation = _check_positive_int_or_tuple('dilation', dilation, self.name, allow_four=True, ret_four=True)
        self.add_prim_attr('dilation', self.dilation)
        validator.check_value_type('pad', pad, (int, tuple), self.name)
        if isinstance(pad, int):
            pad = (pad,) * 4
        else:
            validator.check_integer('pad size', len(pad), 4, Rel.EQ, self.name)
        self.padding = pad
        self.pad_mode = validator.check_string('pad_mode', pad_mode, ['valid', 'same', 'pad'], self.name)

        if pad_mode != 'pad' and pad != (0, 0, 0, 0):
            raise ValueError(f"For '{self.name}', padding must be zero when pad_mode is '{pad_mode}'.")
        if self.pad_mode == 'pad':
            for item in pad:
                validator.check_integer('pad item', item, 0, Rel.GE, self.name)

        self.mode = validator.check_integer('mode', mode, 1, Rel.EQ, self.name)
        self.add_prim_attr('data_format', "NCHW")
        self.out_channel = validator.check_integer('out_channel', out_channel, 0, Rel.GT, self.name)
        self.group = validator.check_integer('group', group, 0, Rel.GT, self.name)
        self.add_prim_attr('offset_a', 0)

    def infer_shape(self, x_shape, w_shape, b_shape=None):
        validator.check_integer("weight rank", len(w_shape), 4, Rel.EQ, self.name)
        validator.check_integer("x rank", len(x_shape), 4, Rel.EQ, self.name)
        validator.check(f"x_shape[1] / group", x_shape[1] // self.group, "w_shape[1]", w_shape[1], Rel.EQ, self.name)
        validator.check('out_channel', self.out_channel, 'w_shape[0]', w_shape[0], Rel.EQ, self.name)
        validator.check('kernel_size', self.kernel_size, 'w_shape[2:4]', tuple(w_shape[2:4]), Rel.EQ, self.name)

        kernel_size_h = w_shape[2]
        kernel_size_w = w_shape[3]
        stride_h = self.stride[2]
        stride_w = self.stride[3]
        dilation_h = self.dilation[2]
        dilation_w = self.dilation[3]

        if self.pad_mode == "valid":
            h_out = math.ceil((x_shape[2] - dilation_h * (kernel_size_h - 1)) / stride_h)
            w_out = math.ceil((x_shape[3] - dilation_w * (kernel_size_w - 1)) / stride_w)
            pad_top, pad_bottom, pad_left, pad_right = 0, 0, 0, 0
        elif self.pad_mode == "same":
            h_out = math.ceil(x_shape[2] / stride_h)
            w_out = math.ceil(x_shape[3] / stride_w)

            pad_needed_h = max(0, (h_out - 1) * stride_h + dilation_h * (kernel_size_h - 1) + 1 - x_shape[2])
            pad_top = math.floor(pad_needed_h / 2)
            pad_bottom = pad_needed_h - pad_top

            pad_needed_w = max(0, (w_out - 1) * stride_w + dilation_w * (kernel_size_w - 1) + 1 - x_shape[3])
            pad_left = math.floor(pad_needed_w / 2)
            pad_right = pad_needed_w - pad_left
        elif self.pad_mode == 'pad':
            pad_top, pad_bottom, pad_left, pad_right = self.padding

            h_out = 1 + (x_shape[2] + pad_top + pad_bottom - kernel_size_h - (kernel_size_h - 1) * (dilation_h - 1)) \
                / stride_h
            w_out = 1 + (x_shape[3] + pad_left + pad_right - kernel_size_w - (kernel_size_w - 1) * (dilation_w - 1)) \
                / stride_w
            h_out = math.floor(h_out)
            w_out = math.floor(w_out)

        self.pad_list = [pad_top, pad_bottom, pad_left, pad_right]
        self.add_prim_attr('pad_list', (pad_top, pad_bottom, pad_left, pad_right))
        out_channel = self.out_channel
        out_shape = [x_shape[0], out_channel, h_out, w_out]
        return out_shape

    def infer_dtype(self, x_dtype, w_dtype, b_dtype=None):
        args = {'x': x_dtype, 'w': w_dtype}
        valid_types = [mstype.int8, mstype.int32, mstype.float16, mstype.float32]
        validator.check_tensor_type_same(args, valid_types, self.name)
        if x_dtype.element_type() == mstype.int8:
            return mstype.tensor_type(mstype.int32)
        return x_dtype


class DepthwiseConv2dNative(PrimitiveWithInfer):
    r"""
    Returns the depth-wise convolution value for the input.

    Applies depthwise conv2d for the input, which will generate more channels with channel_multiplier.
    Given an input tensor of shape :math:`(N, C_{in}, H_{in}, W_{in})` where :math:`N` is the batch size and a
    filter tensor with kernel size :math:`(ks_{h}, ks_{w})`, containing :math:`C_{in} * \text{channel_multiplier}`
    convolutional filters of depth 1; it applies different filters to each input channel (channel_multiplier channels
    for each with default value 1), then concatenates the results together. The output has
    :math:`\text{in_channels} * \text{channel_multiplier}` channels.

    Args:
        channel_multiplier (int): The multipiler for the original output conv.
        kernel_size (Union[int, tuple[int]]): The size of the conv kernel.
        mode (int): 0 Math convolution, 1 cross-correlation convolution ,
                       2 deconvolution, 3 depthwise convolution. Default: 3.
        pad_mode (str): "valid", "same", "pad" the mode to fill padding. Default: "valid".
        pad (int): The pad value to fill. Default: 0.
        stride (Union[int, tuple[int]]): The stride to apply conv filter. Default: 1.
        dilation (Union[int, tuple[int]]): Specifies the dilation rate to use for dilated convolution. Default: 1.
        group (int): Splits input into groups. Default: 1.

    Inputs:
        - **input** (Tensor) - Tensor of shape :math:`(N, C_{in}, H_{in}, W_{in})`.
        - **weight** (Tensor) - Set size of kernel is :math:`(K_1, K_2)`, then the shape is
          :math:`(K, C_{in}, K_1, K_2)`, `K` must be 1.

    Outputs:
        Tensor of shape :math:`(N, C_{in} * \text{channel_multiplier}, H_{out}, W_{out})`.

    Examples:
        >>> input = Tensor(np.ones([10, 32, 32, 32]), mindspore.float32)
        >>> weight = Tensor(np.ones([1, 32, 3, 3]), mindspore.float32)
        >>> depthwise_conv2d = P.DepthwiseConv2dNative(channel_multiplier = 3, kernel_size = (3, 3))
        >>> output = depthwise_conv2d(input, weight)
        >>> assert output.shape == (10, 96, 30, 30)
    """

    @prim_attr_register
    def __init__(self,
                 channel_multiplier,
                 kernel_size,
                 mode=3,
                 pad_mode="valid",
                 pad=0,
                 stride=1,
                 dilation=1,
                 group=1):
        """init DepthwiseConv2dNative"""
        self.init_prim_io_names(inputs=['x', 'w'], outputs=['output'])
        self.kernel_size = _check_positive_int_or_tuple('kernel_size', kernel_size, self.name)
        self.stride = _check_positive_int_or_tuple('stride', stride, self.name)
        if self.stride[0] != self.stride[1]:
            raise ValueError("The height and width of stride should be equal,"
                             f"but got height:{self.stride[0]},  width:{self.stride[1]}")
        self.add_prim_attr('stride', (1, 1, self.stride[0], self.stride[1]))

        self.dilation = _check_positive_int_or_tuple('dilation', dilation, self.name)
        if self.dilation[0] != self.dilation[1]:
            raise ValueError("The height and width of dilation should be equal,"
                             f"but got height:{self.dilation[0]},  width:{self.dilation[1]}")
        self.add_prim_attr('dilation', (1, 1, self.dilation[0], self.dilation[1]))
        validator.check_value_type('pad', pad, (int,), self.name)
        self.pad_mode = validator.check_string('pad_mode', pad_mode, ['valid', 'same', 'pad'], self.name)
        self.pad = validator.check_pad_value_by_mode(pad_mode, pad, self.name)
        self.mode = validator.check_integer("mode", mode, 3, Rel.EQ, self.name)
        self.add_prim_attr('data_format', "NCHW")
        self.channel_multiplier = validator.check_integer("channel_multiplier", channel_multiplier, 0, Rel.GT,
                                                          self.name)
        self.group = validator.check_integer("group", group, 0, Rel.GT, self.name)
        self.add_prim_attr('offset_a', 0)

    def infer_shape(self, x_shape, w_shape, b_shape=None):
        validator.check_integer("weight rank", len(w_shape), 4, Rel.EQ, self.name)
        validator.check_integer("x rank", len(x_shape), 4, Rel.EQ, self.name)
        validator.check("x_shape[1]", x_shape[1], "w_shape[1]", w_shape[1], Rel.EQ, self.name)
        validator.check('kernel_size', self.kernel_size, 'w_shape[2:4]', tuple(w_shape[2:4]), Rel.EQ, self.name)

        kernel_size_n, _, kernel_size_h, kernel_size_w = w_shape
        _, _, stride_h, stride_w = self.stride
        _, _, dilation_h, dilation_w = self.dilation
        if kernel_size_n != 1:
            raise ValueError(f"The batch of input weight should be 1, but got {kernel_size_n}")
        if self.pad_mode == "valid":
            h_out = math.ceil((x_shape[2] - dilation_h * (kernel_size_h - 1)) / stride_h)
            w_out = math.ceil((x_shape[3] - dilation_w * (kernel_size_w - 1)) / stride_w)
            pad_top, pad_bottom, pad_left, pad_right = 0, 0, 0, 0
        elif self.pad_mode == "same":
            h_out = math.ceil(x_shape[2] / stride_h)
            w_out = math.ceil(x_shape[3] / stride_w)

            pad_needed_h = max(0, (h_out - 1) * stride_h + dilation_h * (kernel_size_h - 1) + 1 - x_shape[2])
            pad_top = math.floor(pad_needed_h / 2)
            pad_bottom = pad_needed_h - pad_top

            pad_needed_w = max(0, (w_out - 1) * stride_w + dilation_w * (kernel_size_w - 1) + 1 - x_shape[3])
            pad_left = math.floor(pad_needed_w / 2)
            pad_right = pad_needed_w - pad_left
        elif self.pad_mode == 'pad':
            pad_top, pad_bottom, pad_left, pad_right = self.pad, self.pad, self.pad, self.pad

            h_out = 1 + (x_shape[2] + 2 * self.pad - kernel_size_h - (kernel_size_h - 1) * (dilation_h - 1)) \
                / stride_h
            w_out = 1 + (x_shape[3] + 2 * self.pad - kernel_size_w - (kernel_size_w - 1) * (dilation_w - 1)) \
                / stride_w
            h_out = math.floor(h_out)
            w_out = math.floor(w_out)

        self.pad_list = (pad_top, pad_bottom, pad_left, pad_right)
        self.add_prim_attr('pads', self.pad_list)

        out_channel = self.channel_multiplier * x_shape[1]
        out_shape = [x_shape[0], out_channel, h_out, w_out]
        return out_shape

    def infer_dtype(self, x_dtype, w_dtype, b_dtype=None):
        args = {'x': x_dtype, 'w': w_dtype}
        validator.check_tensor_type_same(args, mstype.number_type, self.name)
        if x_dtype.element_type() == mstype.int8:
            return mstype.tensor_type(mstype.int32)
        return x_dtype


class _Pool(PrimitiveWithInfer):
    r"""
    Performs max/avg pooling operation.

    Args:
        ksize (Union[int, tuple[int]]): The size of the kernel, that should be a tuple
           of two `int` for height and width. Default: 1.
        strides (Union[int, tuple[int]]): The stride of the window, that should be
            a tuple of two `int` for height and width. Default: 1.
        padding (str): The optional value for pad mode, is "same" or "valid", not case sensitive.
            Default: "valid".
    """

    @prim_attr_register
    def __init__(self, ksize=1, strides=1, padding="valid"):
        self.init_prim_io_names(inputs=['x'], outputs=['output'])
        validator.check_value_type('ksize', ksize, [int, tuple], self.name)
        validator.check_value_type('strides', strides, [int, tuple], self.name)
        self.padding = validator.check_string('padding', padding.upper(), ['VALID', 'SAME'], self.name)
        self.add_prim_attr("padding", self.padding)
        self.is_maxpoolwithargmax = (self.name == "MaxPoolWithArgmax")
        if not self.is_maxpoolwithargmax:
            self.add_prim_attr('data_format', "NCHW")

        self.ksize = _check_positive_int_or_tuple("ksize", ksize, self.name, allow_four=False, ret_four=True)
        if self.is_maxpoolwithargmax:
            self.ksize = (1, self.ksize[-2], self.ksize[-1], 1)
        self.add_prim_attr("ksize", self.ksize)

        self.strides = _check_positive_int_or_tuple("strides", strides, self.name, allow_four=False, ret_four=True)
        if self.is_maxpoolwithargmax:
            self.strides = (1, self.strides[-2], self.strides[-1], 1)
        self.add_prim_attr("strides", self.strides)

    def infer_shape(self, x_shape):
        validator.check_integer("x rank", len(x_shape), 4, Rel.EQ, self.name)
        batch, channel, input_h, input_w = x_shape
        if self.is_maxpoolwithargmax:
            _, kernel_h, kernel_w, _ = self.ksize
            _, stride_h, stride_w, _ = self.strides
        else:
            _, _, kernel_h, kernel_w = self.ksize
            _, _, stride_h, stride_w = self.strides

        if self.padding == "VALID":
            out_h = math.ceil((input_h - (kernel_h - 1)) / stride_h)
            out_w = math.ceil((input_w - (kernel_w - 1)) / stride_w)
        elif self.padding == "SAME":
            out_h = math.ceil(input_h / stride_h)
            out_w = math.ceil(input_w / stride_w)
        out_shape = [batch, channel, out_h, out_w]

        for shape_value in out_shape:
            if shape_value <= 0:
                raise ValueError(f"For '{self.name}' The kernel size is not valid, "
                                 f"please check it if is larger than data's shape size.")
        return out_shape

    def infer_dtype(self, x_dtype):
        validator.check_subclass("input", x_dtype, mstype.tensor, self.name)
        return x_dtype


class MaxPool(_Pool):
    r"""
    Max pooling operation.

    Applies a 2D max pooling over an input Tensor which can be regarded as a composition of 2D planes.

    Typically the input is of shape :math:`(N_{in}, C_{in}, H_{in}, W_{in})`, MaxPool outputs
    regional maximum in the :math:`(H_{in}, W_{in})`-dimension. Given kernel size
    :math:`ks = (h_{ker}, w_{ker})` and stride :math:`s = (s_0, s_1)`, the operation is as follows.

    .. math::
        \text{output}(N_i, C_j, h, w) = \max_{m=0, \ldots, h_{ker}-1} \max_{n=0, \ldots, w_{ker}-1}
        \text{input}(N_i, C_j, s_0 \times h + m, s_1 \times w + n)

    Args:
        ksize (Union[int, tuple[int]]): The size of kernel used to take the maximum value,
            is an int number that represents height and width are both ksize, or a tuple
            of two int numbers that represent height and width respectively. Default: 1.
        strides (Union[int, tuple[int]]): The distance of kernel moving, an int number that represents
            the height and width of movement are both strides, or a tuple of two int numbers that
            represent height and width of movement respectively. Default: 1.
        padding (str): The optional value for pad mode, is "same" or "valid", not case sensitive.
            Default: "valid".

            - same: Adopts the way of completion. The height and width of the output will be the same as
              the input. The total number of padding will be calculated in horizontal and vertical
              directions and evenly distributed to top and bottom, left and right if possible.
              Otherwise, the last extra padding will be done from the bottom and the right side.

            - valid: Adopts the way of discarding. The possible largest height and width of output
              will be returned without padding. Extra pixels will be discarded.

    Inputs:
        - **input** (Tensor) - Tensor of shape :math:`(N, C_{in}, H_{in}, W_{in})`.

    Outputs:
        Tensor, with shape :math:`(N, C_{out}, H_{out}, W_{out})`.

    Examples:
        >>> input_tensor = Tensor(np.arange(1 * 3 * 3 * 4).reshape((1, 3, 3, 4)), mindspore.float32)
        >>> maxpool_op = P.MaxPool(padding="VALID", ksize=2, strides=1)
        >>> output_tensor = maxpool_op(input_tensor)
    """

    @prim_attr_register
    def __init__(self, ksize=1, strides=1, padding="valid"):
        super(MaxPool, self).__init__(ksize, strides, padding)


class MaxPoolWithArgmax(_Pool):
    r"""
    Performs max pooling on the input Tensor and return both max values and indices.

    Typically the input is of shape :math:`(N_{in}, C_{in}, H_{in}, W_{in})`, MaxPool outputs
    regional maximum in the :math:`(H_{in}, W_{in})`-dimension. Given kernel size
    :math:`ks = (h_{ker}, w_{ker})` and stride :math:`s = (s_0, s_1)`, the operation is as follows.

    .. math::
        \text{output}(N_i, C_j, h, w) = \max_{m=0, \ldots, h_{ker}-1} \max_{n=0, \ldots, w_{ker}-1}
        \text{input}(N_i, C_j, s_0 \times h + m, s_1 \times w + n)

    Args:
        ksize (Union[int, tuple[int]]): The size of kernel used to take the maximum value and arg value,
            is an int number that represents height and width are both ksize, or a tuple of
            two int numbers that represent height and width respectively. Default: 1.
        strides (Union[int, tuple[int]]): The distance of kernel moving, an int number that represents
            the height and width of movement are both strides, or a tuple of two int numbers that
            represent height and width of movement respectively. Default: 1.
        padding (str): The optional value for pad mode, is "same" or "valid", not case sensitive.
            Default: "valid".

            - same: Adopts the way of completion. The height and width of the output will be the same as
              the input. The total number of padding will be calculated in horizontal and vertical
              directions and evenly distributed to top and bottom, left and right if possible.
              Otherwise, the last extra padding will be done from the bottom and the right side.

            - valid: Adopts the way of discarding. The possible largest height and width of output
              will be returned without padding. Extra pixels will be discarded.


    Inputs:
        - **input** (Tensor) - Tensor of shape :math:`(N, C_{in}, H_{in}, W_{in})`.
          Data type should be float16 or float32.

    Outputs:
        Tuple of 2 Tensor, the maxpool result and where max values from.

        - **output** (Tensor) -  Maxpooling result, with shape :math:`(N, C_{out}, H_{out}, W_{out})`.
        - **mask** (Tensor) -  Max values' index represented by the mask.

    Examples:
        >>> input_tensor = Tensor(np.arange(1 * 3 * 3 * 4).reshape((1, 3, 3, 4)), mindspore.float32)
        >>> maxpool_arg_op = P.MaxPoolWithArgmax(padding="VALID", ksize=2, strides=1)
        >>> output_tensor, argmax = maxpool_arg_op(input_tensor)
    """

    def __init__(self, ksize=1, strides=1, padding="valid"):
        super(MaxPoolWithArgmax, self).__init__(ksize, strides, padding)
        self.is_tbe = context.get_context("device_target") == "Ascend"
        self.is_gpu = context.get_context("device_target") == "GPU"

    def infer_shape(self, x_shape):
        out_shape = _Pool.infer_shape(self, x_shape)
        _, _, out_h, out_w = out_shape
        _, kernel_h, kernel_w, _ = self.ksize

        argmax_shape = []
        if self.is_tbe:
            for i in range(4):
                if i == 2:
                    dim = kernel_h * kernel_w
                    argmax_shape.append(dim)
                elif i == 3:
                    dim = math.ceil(out_h * out_w / 16) + 1
                    argmax_shape.append(dim)
                else:
                    argmax_shape.append(x_shape[i])
        else:
            argmax_shape = out_shape

        return out_shape, argmax_shape

    def infer_dtype(self, x_dtype):
        out_dtype = x_dtype
        validator.check_tensor_type_same({"x": x_dtype}, (mstype.float16, mstype.float32), self.name)
        argmax_dtype = mstype.uint16
        if self.is_gpu:
            argmax_dtype = mstype.int32
        return out_dtype, argmax_dtype


class AvgPool(_Pool):
    r"""
    Average pooling operation.

    Applies a 2D average pooling over an input Tensor which can be regarded as a composition of 2D input planes.
    Typically the input is of shape :math:`(N_{in}, C_{in}, H_{in}, W_{in})`, AvgPool2d outputs
    regional average in the :math:`(H_{in}, W_{in})`-dimension. Given kernel size
    :math:`ks = (h_{ker}, w_{ker})` and stride :math:`s = (s_0, s_1)`, the operation is as follows.

    .. math::
        \text{output}(N_i, C_j, h, w) = \frac{1}{h_{ker} * w_{ker}} \sum_{m=0}^{h_{ker}-1} \sum_{n=0}^{w_{ker}-1}
        \text{input}(N_i, C_j, s_0 \times h + m, s_1 \times w + n)

    Args:
        ksize (Union[int, tuple[int]]): The size of kernel used to take the average value,
            is an int number that represents height and width are both ksize, or a tuple
            of two int numbers that represent height and width respectively. Default: 1.
        strides (Union[int, tuple[int]]): The distance of kernel moving, an int number that represents
            the height and width of movement are both strides, or a tuple of two int numbers that
            represent height and width of movement respectively. Default: 1.
        padding (str): The optional value for pad mode, is "same" or "valid", not case sensitive.
            Default: "valid".

            - same: Adopts the way of completion. The height and width of the output will be the same as
              the input. The total number of padding will be calculated in horizontal and vertical
              directions and evenly distributed to top and bottom, left and right if possible.
              Otherwise, the last extra padding will be done from the bottom and the right side.

            - valid: Adopts the way of discarding. The possible largest height and width of output
              will be returned without padding. Extra pixels will be discarded.

    Inputs:
        - **input** (Tensor) - Tensor of shape :math:`(N, C_{in}, H_{in}, W_{in})`.

    Outputs:
        Tensor, with shape :math:`(N, C_{out}, H_{out}, W_{out})`.

    Examples:
        >>> import mindspore
        >>> import mindspore.nn as nn
        >>> import numpy as np
        >>> from mindspore import Tensor
        >>> from mindspore.ops import operations as P
        >>> class Net(nn.Cell):
        >>>     def __init__(self):
        >>>         super(Net, self).__init__()
        >>>         self.avgpool_op = P.AvgPool(padding="VALID", ksize=2, strides=1)
        >>>
        >>>     def construct(self, x):
        >>>         result = self.avgpool_op(x)
        >>>         return result
        >>>
        >>> input_x = Tensor(np.arange(1 * 3 * 3 * 4).reshape(1, 3, 3, 4), mindspore.float32)
        >>> net = Net()
        >>> result = net(input_x)
        [[[[ 2.5   3.5   4.5]
           [ 6.5   7.5   8.5]]
          [[ 14.5  15.5  16.5]
           [ 18.5  19.5  20.5]]
          [[ 26.5  27.5  28.5]
           [ 30.5  31.5  32.5]]]]
    """

    @prim_attr_register
    def __init__(self, ksize=1, strides=1, padding="valid"):
        if context.get_context("device_target") == "GPU":
            self.target = "GPU"
        elif context.get_context("enable_ge"):
            self.target = "GE"
        else:
            self.target = "OTHER"
        super(AvgPool, self).__init__(ksize, strides, padding)


class Conv2DBackpropInput(PrimitiveWithInfer):
    """
    Computes the gradients of convolution with respect to the input.

    Args:
        out_channel (int): The dimensionality of the output space.
        kernel_size (Union[int, tuple[int]]): The size of the convolution window.
        pad_mode (str): "valid", "same", "pad" the mode to fill padding. Default: "valid".
        pad (Union[int, tuple[int]]): The pad value to fill. Default: 0. If `pad` is one integer, the padding of
                    top, bottom, left and right is same, equal to pad. If `pad` is tuple with four integer, the padding
                    of top, bottom, left and right equal to pad[0], pad[1], pad[2], pad[3] with corresponding.
        mode (int): 0 Math convolutiuon, 1 cross-correlation convolution ,
                       2 deconvolution, 3 depthwise convolution. Default: 1.
        stride (Union[int. tuple[int]]): The stride to apply conv filter. Default: 1.
        dilation (Union[int. tuple[int]]): Specifies the dilation rate to use for dilated convolution. Default: 1.
        group (int): Splits input into groups. Default: 1.

    Returns:
        Tensor, the gradients of convolution.

    Examples:
        >>> dout = Tensor(np.ones([10, 32, 30, 30]), mindspore.float32)
        >>> weight = Tensor(np.ones([32, 32, 3, 3]), mindspore.float32)
        >>> x = Tensor(np.ones([10, 32, 32, 32]))
        >>> conv2d_backprop_input = P.Conv2DBackpropInput(out_channel=32, kernel_size=3)
        >>> conv2d_backprop_input(dout, weight, F.shape(x))
    """

    @prim_attr_register
    def __init__(self,
                 out_channel,
                 kernel_size,
                 pad_mode="valid",
                 pad=0,
                 pad_list=None,
                 mode=1,
                 stride=1,
                 dilation=1,
                 group=1):
        """init Conv2DBackpropInput"""
        self.init_prim_io_names(inputs=['out_backprop', 'filter', 'input_sizes'], outputs=['output'])
        self.out_channel = validator.check_integer('out_channel', out_channel, 0, Rel.GT, self.name)
        self.kernel_size = _check_positive_int_or_tuple('kernel_size', kernel_size, self.name)
        self.stride = _check_positive_int_or_tuple('stride', stride, self.name, allow_four=True, ret_four=False)
        self.add_prim_attr('stride', self.stride)
        self.dilation = _check_positive_int_or_tuple('dilation', dilation, self.name, allow_four=True, ret_four=True)
        self.add_prim_attr('dilation', self.dilation)

        validator.check_value_type('pad', pad, (int, tuple), self.name)
        if isinstance(pad, int):
            pad = (pad,) * 4
        else:
            validator.check_integer('pad size', len(pad), 4, Rel.EQ, self.name)
        self.padding = pad
        self.pad_mode = validator.check_string('pad_mode', pad_mode, ['valid', 'same', 'pad'], self.name)
        if pad_mode != 'pad' and pad != (0, 0, 0, 0):
            raise ValueError(f"For '{self.name}', padding must be zero when pad_mode is '{pad_mode}'.")
        if self.pad_mode == 'pad':
            for item in pad:
                validator.check_integer('pad item', item, 0, Rel.GE, self.name)

        pad_mode = pad_mode.upper()
        self.add_prim_attr('pad_mode', pad_mode)
        self.mode = validator.check_integer('mode', mode, 1, Rel.EQ, self.name)
        self.group = validator.check_integer('group', group, 0, Rel.GT, self.name)
        self.add_prim_attr('data_format', "NCHW")
        if pad_list:
            for x in pad_list:
                validator.check_integer('element of pad_list', x, 0, Rel.GE, self.name)
            self.pad_list = pad_list

    def __infer__(self, doutput, w, x_size):
        x_size_v = x_size['value']
        validator.check_value_type('x_size', x_size_v, [tuple], self.name)
        for i, dim_len in enumerate(x_size_v):
            validator.check_value_type("x_size[%d]" % i, dim_len, [int], self.name)
        args = {'doutput': doutput['dtype'], 'w': w['dtype']}
        valid_types = [mstype.int8, mstype.int32, mstype.float16, mstype.float32]
        validator.check_tensor_type_same(args, valid_types, self.name)

        # infer shape
        dout_shape = doutput['shape']
        kernel_h = self.kernel_size[0]
        kernel_w = self.kernel_size[1]
        stride_h = self.stride[0]
        stride_w = self.stride[1]
        dilation_h = self.dilation[2]
        dilation_w = self.dilation[3]
        # default pad mode is valid
        pad_list = (0, 0, 0, 0)
        if self.pad_list:
            pad_list = tuple(self.pad_list)
        elif self.pad_mode == "SAME":
            pad_needed_h = max(0, (dout_shape[2] - 1) * stride_h + dilation_h * (kernel_h - 1) + 1 - x_size_v[2])
            pad_top = math.floor(pad_needed_h / 2)
            pad_bottom = pad_needed_h - pad_top

            pad_needed_w = max(0, (dout_shape[3] - 1) * stride_w + dilation_w * (kernel_w - 1) + 1 - x_size_v[3])
            pad_left = math.floor(pad_needed_w / 2)
            pad_right = pad_needed_w - pad_left
            pad_list = (pad_top, pad_bottom, pad_left, pad_right)
        elif self.pad_mode == 'PAD':
            pad_list = self.padding
        self.add_prim_attr('pad_list', pad_list)
        out = {
            'value': None,
            'shape': x_size_v,
            'dtype': doutput['dtype'],
        }
        return out


class BiasAdd(PrimitiveWithInfer):
    r"""
    Returns sum of input and bias tensor.

    Adds the 1-D bias tensor to the input tensor, and broadcasts the shape on all axis
    except for the channel axis.

    Inputs:
        - **input_x** (Tensor) - Input value. The input shape can be 2-4 dimensions.
        - **bias** (Tensor) - Bias value, with shape :math:`(C)`.
          The shape of `bias` must be the same as `input_x` in second dimension.

    Outputs:
        Tensor, with the same shape and type as `input_x`.

    Examples:
        >>> input_x = Tensor(np.arange(6).reshape((2, 3)), mindspore.float32)
        >>> bias = Tensor(np.random.random(3).reshape((3,)), mindspore.float32)
        >>> bias_add = P.BiasAdd()
        >>> bias_add(input_x, bias)
    """

    @prim_attr_register
    def __init__(self):
        self.init_prim_io_names(inputs=['x', 'b'], outputs=['output'])
        self.add_prim_attr('data_format', 'NCHW')

    def infer_shape(self, x_shape, b_shape):
        validator.check_integer("x rank", len(x_shape), 2, Rel.GE, self.name)
        validator.check_integer("bias rank", len(b_shape), 1, Rel.EQ, self.name)
        validator.check("b_shape[0]", b_shape[0], "x_shape[1]", x_shape[1], Rel.EQ, self.name)
        return x_shape

    def infer_dtype(self, x_type, b_type):
        args = {"input_x": x_type, "bias": b_type}
        validator.check_tensor_type_same(args, mstype.number_type, self.name)
        return x_type


class TopK(PrimitiveWithInfer):
    """
    Finds values and indices of the `k` largest entries along the last dimension.

    Args:
        sorted (bool): If true, the resulting elements will
            be sorted by the values in descending order. Default: False.

    Inputs:
        - **input_x** (Tensor) - Input to be computed, data type should be float16, float32 or int32.
        - **k** (int) - Number of top elements to be computed along the last dimension, constant input is needed.

    Outputs:
        Tuple of 2 Tensor, the values and the indices.

        - **values** (Tensor) - The `k` largest elements along each last dimensional slice.
        - **indices** (Tensor) - The indices of values within the last dimension of input.

    Examples:
        >>> topk = P.TopK(sorted=True)
        >>> input_x = Tensor([1, 2, 3, 4, 5], mindspore.float16)
        >>> k = 3
        >>> values, indices = topk(input_x, k)
        >>> assert values == Tensor(np.array([5, 4, 3]), mstype.float16)
        >>> assert indices == Tensor(np.array([4, 3, 2]), mstype.int32)
    """

    @prim_attr_register
    def __init__(self, sorted=False):
        validator.check_value_type("sorted", sorted, [bool], self.name)
        self.init_prim_io_names(inputs=['input', 'k'],
                                outputs=['values', 'indices'])

    def __infer__(self, input_x, k):
        x_dtype = input_x['dtype']
        valid_types = (mstype.int32, mstype.float16, mstype.float32)
        validator.check_tensor_type_same({'x': x_dtype}, valid_types, self.name)
        k_v = k['value']
        validator.check_value_type('k', k_v, (int,), self.name)
        x_shape = list(input_x['shape'])
        ndim = len(x_shape) - 1
        x_shape[ndim] = k_v
        return {'shape': (x_shape, x_shape),
                'dtype': (x_dtype, mstype.int32),
                'value': None}


class SoftmaxCrossEntropyWithLogits(PrimitiveWithInfer):
    r"""
    Gets the softmax cross-entropy value between logits and labels which shoule be one-hot encoding.

    Note:
        Sets input logits as `X`, input label as `Y`, output as `loss`. Then,

        .. math::
            p_{ij} = softmax(X_{ij}) = \frac{exp(x_i)}{\sum_{j = 0}^{N-1}\exp(x_j)}

        .. math::
            loss_{ij} = -\sum_j{Y_{ij} * ln(p_{ij})}

    Inputs:
        - **logits** (Tensor) - Input logits, with shape :math:`(N, C)`. Data type should be float16 or float32.
        - **labels** (Tensor) - Ground truth labels, with shape :math:`(N, C)`. Has the same data type with `logits`.

    Outputs:
        Tuple of 2 Tensor, the loss shape is `(N,)`, and the dlogits with the same shape as `logits`.

    Examples:
        >>> logits = Tensor([[2, 4, 1, 4, 5], [2, 1, 2, 4, 3]], mindspore.float32)
        >>> labels = Tensor([[0, 0, 0, 0, 1], [0, 0, 0, 1, 0]], mindspore.float32)
        >>> softmax_cross = P.SoftmaxCrossEntropyWithLogits()
        >>> loss, backprop = softmax_cross(logits, labels)
        ([0.5899297, 0.52374405], [[0.02760027, 0.20393994, 0.01015357, 0.20393994, -0.44563377],
        [0.08015892, 0.02948882, 0.08015892, -0.4077012, 0.21789455]])
    """

    @prim_attr_register
    def __init__(self):
        pass

    def infer_shape(self, logits_shape, labels_shape):
        validator.check("logits_shape", logits_shape, "labels_shape", labels_shape, Rel.EQ, self.name)
        loss_shape = [logits_shape[0]]
        dlogits_shape = logits_shape
        return (loss_shape, dlogits_shape)

    def infer_dtype(self, logits_type, labels_type):
        args = {"logits": logits_type, "labels": labels_type}
        validator.check_tensor_type_same(args, (mstype.float16, mstype.float32), self.name)
        return (logits_type, logits_type)


class SparseSoftmaxCrossEntropyWithLogits(PrimitiveWithInfer):
    r"""
    Computes the softmax cross-entropy value between logits and sparse encoding labels.

    Note:
        Sets input logits as `X`, input label as `Y`, output as `loss`. Then,

        .. math::
            p_{ij} = softmax(X_{ij}) = \frac{exp(x_i)}{\sum_{j = 0}^{N-1}\exp(x_j)}

        .. math::
            loss_{ij} = \begin{cases} -ln(p_{ij}), &j = y_i \cr -ln(1 - p_{ij}), & j \neq y_i \end{cases}

        .. math::
            loss = \sum_{ij} loss_{ij}

    Args:
        is_grad (bool): If it's true, this operation returns the computed gradient. Default: False.

    Inputs:
        - **logits** (Tensor) - Input logits, with shape :math:`(N, C)`. Data type should be float16 or float32.
        - **labels** (Tensor) - Ground truth labels, with shape :math:`(N)`.
          Data type should be int32 or int64.

    Outputs:
        Tensor, if `is_grad` is False, the output tensor is the value of loss which is a scalar tensor;
        if `is_grad` is True, the output tensor is the gradient of input with the same shape as `logits`.

    Examples:
        Please refer to the usage in nn.SoftmaxCrossEntropyWithLogits source code.
    """

    @prim_attr_register
    def __init__(self, is_grad=False):
        self.init_prim_io_names(inputs=['features', 'labels'], outputs=['output'])
        self.is_grad = is_grad
        self.add_prim_attr('sens', 1.0)

    def infer_shape(self, logits_shape, labels_shape):
        validator.check("logits_shape[0]", logits_shape[0], "labels_shape[0]", labels_shape[0], Rel.EQ, self.name)
        loss_shape = []
        if self.is_grad:
            return logits_shape
        return loss_shape

    def infer_dtype(self, logits_type, labels_type):
        validator.check_tensor_type_same({"logits": logits_type}, (mstype.float16, mstype.float32), self.name)
        validator.check_tensor_type_same({"labels": labels_type}, (mstype.int32, mstype.int64), self.name)
        return logits_type


class ApplyMomentum(PrimitiveWithInfer):
    """
    Optimizer that implements the Momentum algorithm.

    Refer to the paper `On the importance of initialization and momentum in deep
    learning <https://dl.acm.org/doi/10.5555/3042817.3043064>`_  for more details.

    Args:
        use_locking (bool): Enable a lock to protect the update of variable and accumlation tensors. Default: False.
        use_nesterov (bool): Enable Nesterov momentum. Default: False.
        gradient_scale (float): The scale of the gradient. Default: 1.0.

    Inputs:
        - **variable** (Parameter) - Weights to be updated. data type should be float.
        - **accumulation** (Parameter) - Accumulated gradient value by moment weight.
          Has the same data type with `variable`.
        - **learning_rate** (Union[Number, Tensor]) - The learning rate value, should be a float number or
          a scalar tensor with float data type.
        - **gradient** (Tensor) - Gradients, has the same data type as `variable`.
        - **momentum** (Union[Number, Tensor]) - Momentum, should be a float number or
          a scalar tensor with float data type.

    Outputs:
        Tensor, parameters to be updated.

    Examples:
        Please refer to the usage in nn.ApplyMomentum.
    """
    __mindspore_signature__ = (
        ('variable', sig_rw.RW_WRITE, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('accumulation', sig_rw.RW_WRITE, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE,
         sig_dtype.T),
        ('learning_rate', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE,
         sig_dtype.T1),
        ('gradient', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('momentum', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T2)
    )

    @prim_attr_register
    def __init__(self, use_nesterov=False, use_locking=False, gradient_scale=1.0):
        self.init_prim_io_names(inputs=['variable', 'accumulation', 'learning_rate', 'gradient', 'momentum'],
                                outputs=['output'])
        self.is_tbe = context.get_context("device_target") == "Ascend"
        self.is_ge = context.get_context("enable_ge")

    def infer_shape(self, v_shape, a_shape, l_shape, g_shape, m_shape):
        if not self.is_ge and self.is_tbe:
            return v_shape, v_shape
        return v_shape

    def infer_dtype(self, v_dtype, a_dtype, l_dtype, g_dtype, m_dtype):
        valid_types = [mstype.float16, mstype.float32, mstype.float64]
        if v_dtype != mstype.type_refkey and a_dtype != mstype.type_refkey:
            validator.check_tensor_type_same({"v": v_dtype}, valid_types, self.name)
            validator.check_tensor_type_same({"a": a_dtype}, valid_types, self.name)
        validator.check_scalar_or_tensor_type_same({"l_dtype": l_dtype}, valid_types, self.name)
        validator.check_scalar_or_tensor_type_same({"g_dtype": g_dtype}, valid_types, self.name)
        validator.check_scalar_or_tensor_type_same({"m_dtype": m_dtype}, valid_types, self.name)
        if not self.is_ge and self.is_tbe:
            return g_dtype, g_dtype
        return g_dtype


class SmoothL1Loss(PrimitiveWithInfer):
    r"""
    Computes smooth L1 loss, a robust L1 loss.

    SmoothL1Loss is a Loss similar to MSELoss but less sensitive to outliers as described in the
    `Fast R-CNN <https://arxiv.org/abs/1504.08083>`_ by Ross Girshick.

    Note:
        Sets input prediction as `X`, input target as `Y`, output as `loss`. Then,

        .. math::
            \text{SmoothL1Loss} = \begin{cases} \frac{0.5 x^{2}}{\text{beta}}, &if \left |x \right | < \text{beta} \cr
            \left |x \right|-0.5 \text{beta}, &\text{otherwise}\end{cases}

    Args:
        beta (float): A parameter used to control the point where the function will change from
            quadratic to linear. Default: 1.0.

    Inputs:
        - **prediction** (Tensor) - Predict data. Data type should be float16 or float32.
        - **target** (Tensor) - Ground truth data, with the same type and shape as `prediction`.

    Outputs:
        Tensor, with the same type and shape as `prediction`.

    Examples:
        >>> loss = P.SmoothL1Loss()
        >>> input_data = Tensor(np.array([1, 2, 3]), mindspore.float32)
        >>> target_data = Tensor(np.array([1, 2, 2]), mindspore.float32)
        >>> loss(input_data, target_data)
        [0, 0, 0.5]
    """

    @prim_attr_register
    def __init__(self, beta=1.0):
        validator.check_value_type('beta', beta, [float], self.name)
        validator.check('beta', beta, '', 0, Rel.GT, self.name)
        self.init_prim_io_names(inputs=['prediction', 'target'], outputs=['output'])

    def infer_shape(self, prediction, target):
        validator.check('prediction shape', prediction, 'target shape', target, Rel.EQ, self.name)
        return prediction

    def infer_dtype(self, prediction, target):
        args = {"prediction": prediction, "target": target}
        validator.check_tensor_type_same(args, (mstype.float16, mstype.float32), self.name)
        return prediction


class L2Loss(PrimitiveWithInfer):
    """
    Calculates half of the L2 norm of a tensor without using the `sqrt`.

    Set `input_x` as x and output as loss.

    .. math::
        loss = sum(x ** 2) / nelement(x)

    :math:`nelement(x)` represents the number of `input_x`.

    Inputs:
        - **input_x** (Tensor) - A input Tensor. Data type should be float16 or float32.

    Outputs:
        Tensor. Has the same dtype as `input_x`. The output tensor is the value of loss which is a scalar tensor.

    Examples
        >>> input_x = Tensor(np.array([1, 2, 3]), mindspore.float16)
        >>> l2_loss = P.L2Loss()
        >>> l2_loss(input_x)
        7.0
    """

    @prim_attr_register
    def __init__(self):
        """init L2Loss"""

    def infer_shape(self, input_x):
        loss_shape = []
        return loss_shape

    def infer_dtype(self, x_type):
        validator.check_subclass("x_type", x_type, mstype.tensor, self.name)
        valid_types = [mstype.float16, mstype.float32]
        validator.check_tensor_type_same({'x_type': x_type}, valid_types, self.name)
        return x_type


class DataFormatDimMap(PrimitiveWithInfer):
    """
    Returns the dimension index in the destination data format given the one in the source data format.

    Args:
        src_format (string): An optional value for source data format. Default: 'NHWC'.
        dst_format (string): An optional value for destination data format. Default: 'NCHW'.

    Inputs:
        - **input_x** (Tensor) - A Tensor with each element as a dimension index in source data format.
          Must be in the range [-4, 4). It's type is int32.

    Outputs:
        Tensor, has the same type as the `input_x`.

    Examples:
        >>> x = Tensor([0, 1, 2, 3], mindspore.int32)
        >>> dfdm = P.DataFormatDimMap()
        >>> dfdm(x)
        [0 3 1 2]
    """

    @prim_attr_register
    def __init__(self, src_format='NHWC', dst_format='NCHW'):
        valid_values = ['NHWC', 'NCHW']
        self.src_format = validator.check_string("src_format", src_format, valid_values, self.name)
        self.dst_format = validator.check_string("dst_format", dst_format, valid_values, self.name)
        self.init_prim_io_names(inputs=['input_x'], outputs=['output'])

    def infer_shape(self, x_shape):
        return x_shape

    def infer_dtype(self, x_type):
        validator.check_subclass("x", x_type, mstype.tensor, self.name)
        valid_types = [mstype.int32]
        validator.check_tensor_type_same({"x": x_type}, valid_types, self.name)
        return x_type


class RNNTLoss(PrimitiveWithInfer):
    """
    Computes the RNNTLoss and its gradient with respect to the softmax outputs.

    Args:
        blank_label (int): blank label. Default: 0.

    Inputs:
        - **acts** (Tensor) - Tensor of shape :math:`(B, T, U, V)`. Data type should be float16 or float32.
        - **labels** (Tensor[int32]) - Tensor of shape :math:`(B, U-1)`.
        - **input_lengths** (Tensor[int32]) - Tensor of shape :math:`(B,)`.
        - **label_lebgths** (Tensor[int32]) - Tensor of shape :math:`(B,)`.

    Outputs:
        - **costs** (Tensor[int32]) - Tensor of shape :math:`(B,)`.
        - **grads** (Tensor[int32]) - Has the same shape as `acts`.

    Examples:
        >>> B, T, U, V = 1, 2, 3, 5
        >>> acts = np.random.random((B, T, U, V)).astype(np.float32)
        >>> labels = np.array([[1, 2]]).astype(np.int32)
        >>> input_length = np.array([T] * B).astype(np.int32)
        >>> label_length = np.array([len(l) for l in labels]).astype(np.int32)
        >>> rnnt_loss = P.RNNTLoss(blank_label=blank)
        >>> costs, grads = rnnt_loss(Tensor(acts), Tensor(labels), Tensor(input_length), Tensor(label_length))
    """

    @prim_attr_register
    def __init__(self, blank_label=0):
        validator.check_value_type('blank_label', blank_label, [int], self.name)
        self.init_prim_io_names(inputs=['acts', 'labels', 'input_length', 'label_length'],
                                outputs=['costs', 'grads'])

    def infer_shape(self, acts_shape, labels_shape, input_length_shape, label_length_shape):
        validator.check_integer('acts_rank', len(acts_shape), 4, Rel.EQ, self.name)
        validator.check_integer('labels_rank', len(labels_shape), 2, Rel.EQ, self.name)
        validator.check_integer('input_length_rank', len(input_length_shape), 1, Rel.EQ, self.name)
        validator.check_integer('label_length_rank', len(label_length_shape), 1, Rel.EQ, self.name)
        validator.check('labels shape[0]', labels_shape[0], 'acts shape[0]', acts_shape[0], Rel.EQ, self.name)
        validator.check('labels shape[1]', labels_shape[1], 'acts shape[2]-1', acts_shape[2]-1, Rel.EQ, self.name)
        validator.check('input_length size', input_length_shape[0], 'acts shape[0]', acts_shape[0], Rel.EQ, self.name)
        validator.check('label_length size', label_length_shape[0], 'acts shape[0]', acts_shape[0], Rel.EQ, self.name)
        costs_shape = (acts_shape[0],)
        return (costs_shape, acts_shape)

    def infer_dtype(self, acts_type, labels_type, input_length_type, label_length_type):
        validator.check_subclass("acts_type", acts_type, mstype.tensor, self.name)
        validator.check_subclass("labels_type", labels_type, mstype.tensor, self.name)
        validator.check_subclass("input_length_type", input_length_type, mstype.tensor, self.name)
        validator.check_subclass("label_length_type", label_length_type, mstype.tensor, self.name)
        validator.check_tensor_type_same({"acts_type": acts_type}, [mstype.float32, mstype.float16], self.name)
        validator.check_tensor_type_same({"labels_type": labels_type}, [mstype.int32], self.name)
        validator.check_tensor_type_same({"input_length_type": input_length_type}, [mstype.int32], self.name)
        validator.check_tensor_type_same({"label_length_type": label_length_type}, [mstype.int32], self.name)
        return (acts_type, acts_type)


class SGD(PrimitiveWithInfer):
    """
    Computes stochastic gradient descent (optionally with momentum).

    Nesterov momentum is based on the formula from On the importance of
    initialization and momentum in deep learning.

    Note:
        For details, please refer to `nn.SGD` source code.

    Args:
        dampening (float): The dampening for momentum. Default: 0.0.
        weight_decay (float): Weight decay (L2 penalty). Default: 0.0.
        nesterov (bool): Enable Nesterov momentum. Default: False.

    Inputs:
        - **parameters** (Tensor) - Parameters to be updated. With float16 or float32 data type.
        - **gradient** (Tensor) - Gradients. With float16 or float32 data type.
        - **learning_rate** (Tensor) - Learning rate, a scalar tensor with float16 or float32 data type.
          e.g. Tensor(0.1, mindspore.float32)
        - **accum** (Tensor) - Accum(velocity) to be updated. With float16 or float32 data type.
        - **momentum** (Tensor) - Momentum, a scalar tensor with float16 or float32 data type.
          e.g. Tensor(0.1, mindspore.float32).
        - **stat** (Tensor) - States to be updated with the same shape as gradient. With float16 or float32 data type.

    Outputs:
        Tensor, parameters to be updated.

    Examples:
        >>> sgd = P.SGD()
        >>> parameters = Tensor(np.array([2, -0.5, 1.7, 4]), mindspore.float32)
        >>> gradient = Tensor(np.array([1, -1, 0.5, 2]), mindspore.float32)
        >>> learning_rate = Tensor(0.01, mindspore.float32)
        >>> accum = Tensor(np.array([0.1, 0.3, -0.2, -0.1]), mindspore.float32)
        >>> momentum = Tensor(0.1, mindspore.float32)
        >>> stat = Tensor(np.array([1.5, -0.3, 0.2, -0.7]), mindspore.float32)
        >>> result = sgd(parameters, gradient, learning_rate, accum, momentum, stat)
    """

    @prim_attr_register
    def __init__(self, dampening=0.0, weight_decay=0.0, nesterov=False):
        validator.check_value_type("nesterov", nesterov, [bool], self.name)
        if nesterov and dampening != 0:
            raise ValueError(f"Nesterov need zero dampening!")
        self.init_prim_io_names(inputs=['parameters', 'gradient', 'learning_rate', 'accum', 'momentum', 'stat'],
                                outputs=['output'])

    def infer_shape(self, parameters_shape, gradient_shape, learning_rate_shape,
                    accum_shape, momentum_shape, stat_shape):
        validator.check_integer(f'parameters rank', len(parameters_shape), 0, Rel.GT, self.name)
        validator.check_integer(f'gradient rank', len(gradient_shape), 0, Rel.GE, self.name)
        validator.check_integer(f'learning rate rank', len(learning_rate_shape), 0, Rel.GE, self.name)
        validator.check_integer(f'accumulation rank', len(accum_shape), 0, Rel.GT, self.name)
        validator.check_integer(f'momentum rank', len(momentum_shape), 0, Rel.GE, self.name)
        validator.check_integer(f'stat rank', len(stat_shape), 0, Rel.GE, self.name)
        validator.check("gradient shape", gradient_shape, "stat shape", stat_shape, Rel.EQ, self.name)
        return parameters_shape

    def infer_dtype(self, parameters_dtype, gradient_dtype, learning_rate_dtype,
                    accum_dtype, momentum_dtype, stat_dtype):
        valid_types = [mstype.float16, mstype.float32]
        validator.check_tensor_type_same({"parameters": parameters_dtype}, valid_types, self.name)
        validator.check_tensor_type_same({"gradient": gradient_dtype}, valid_types, self.name)
        validator.check_tensor_type_same({"learning_rate": learning_rate_dtype}, valid_types, self.name)
        validator.check_tensor_type_same({"accum": accum_dtype}, valid_types, self.name)
        validator.check_tensor_type_same({"momentum": momentum_dtype}, valid_types, self.name)
        validator.check_tensor_type_same({"stat": stat_dtype}, valid_types, self.name)
        return parameters_dtype


class ApplyRMSProp(PrimitiveWithInfer):
    """
    Optimizer that implements the Root Mean Square prop(RMSProp) algorithm.
    Please refer to the usage in source code of `nn.RMSProp`.

    Note:
        Update `var` according to the RMSProp algorithm.

        ..  math::
            s_{t} = \\rho s_{t-1} + (1 - \\rho)(\\nabla Q_{i}(w))^2

        ..  math::
            m_{t} = \\beta m_{t-1} + \\frac{\\eta} {\\sqrt{s_{t} + \\epsilon}} \\nabla Q_{i}(w)

        ..  math::
            w = w - m_{t}

        where, :math:`w` represents `var`, which will be updated.
        :math:`s_{t}` represents `mean_square`, :math:`s_{t-1}` is the last momentent of :math:`s_{t}`,
        :math:`m_{t}` represents `moment`, :math:`m_{t-1}` is the last momentent of :math:`m_{t}`.
        :math:`\\rho` represents `decay`. :math:`\\beta` is the momentum term, represents `momentum`.
        :math:`\\epsilon` is a smoothing term to avoid division by zero, represents `epsilon`.
        :math:`\\eta` represents `learning_rate`. :math:`\\nabla Q_{i}(w)` represents `grad`.

    Args:
        use_locking (bool): Enable a lock to protect the update of variable tensors. Default: False.

    Inputs:
        - **var** (Tensor) - Weights to be update.
        - **mean_square** (Tensor) - Mean square gradients, must have the same type as `var`.
        - **moment** (Tensor) - Delta of `var`, must have the same type as `var`.
        - **learning_rate** (Union[Number, Tensor]) - Learning rate. Should be a float number or
          a scalar tensor with float16 or float32 data type.
        - **grad** (Tensor) - Gradients, must have the same type as `var`.
        - **decay** (float) - Decay rate. Only constant value is allowed.
        - **momentum** (float) - Momentum. Only constant value is allowed.
        - **epsilon** (float) - Ridge term. Only constant value is allowed.

    Outputs:
        Tensor, parameters to be update.

    Examples:
        >>> apply_rms = P.ApplyRMSProp()
        >>> input_x = Tensor(1., mindspore.float32)
        >>> mean_square = Tensor(2., mindspore.float32)
        >>> moment = Tensor(1., mindspore.float32)
        >>> grad = Tensor(2., mindspore.float32 )
        >>> learning_rate = Tensor(0.9, mindspore.float32)
        >>> decay = 0.0
        >>> momentum = 1e-10
        >>> epsilon = 0.001
        >>> result = apply_rms(input_x, mean_square, moment, learning_rate, grad, decay, momentum, epsilon)
        (-2.9977674, 0.80999994, 1.9987665)
    """

    @prim_attr_register
    def __init__(self, use_locking=False):
        self.use_locking = validator.check_value_type("use_locking", use_locking, [bool], self.name)
        self.init_prim_io_names(inputs=['var', 'mean_square', 'moment', 'learning_rate', 'grad',
                                        'rho', 'momentum', 'epsilon'], outputs=['output'])
        self.is_ge = context.get_context("enable_ge")
        self.is_d = context.get_context("device_target") == "Ascend"

    def infer_shape(self, var_shape, mean_square_shape, moment_shape, learning_rate_shape, grad_shape, decay_shape,
                    momentum_shape, epsilon_shape):
        validator.check("var_shape", var_shape, "mean_square_shape", mean_square_shape, Rel.EQ, self.name)
        validator.check("var_shape", var_shape, "moment_shape", moment_shape, Rel.EQ, self.name)
        validator.check("var_shape", var_shape, "grad_shape", grad_shape, Rel.EQ, self.name)
        if not self.is_ge and self.is_d:
            return var_shape, var_shape, var_shape
        return var_shape

    def infer_dtype(self, var_dtype, mean_square_dtype, moment_dtype, learning_rate_dtype, grad_dtype, decay_dtype,
                    momentum_dtype, epsilon_dtype):
        args = {"var": var_dtype, "mean_square": mean_square_dtype, "moment": moment_dtype, "grad": grad_dtype}
        validator.check_tensor_type_same(args, mstype.number_type, self.name)

        valid_types = [mstype.float16, mstype.float32]
        args_decay = {"decay": decay_dtype, 'momentum': momentum_dtype, "epsilon": epsilon_dtype}
        validator.check_type_same(args_decay, valid_types, self.name)
        args_lr = {"learning_rate": learning_rate_dtype, "decay": decay_dtype}
        validator.check_scalar_or_tensor_type_same(args_lr, valid_types, self.name, allow_mix=True)
        if not self.is_ge and self.is_d:
            return var_dtype, var_dtype, var_dtype
        return var_dtype

    def infer_value(self, var, mean_square, moment, learning_rate, grad, decay, momentum, epsilon):
        if decay is None or momentum is None or epsilon is None:
            raise ValueError(f"For {self.name}, decay, momentum, epsilon must be const.")


class ApplyCenteredRMSProp(PrimitiveWithInfer):
    """
    Optimizer that implements the centered RMSProp algorithm.
    Please refer to the usage in source code of `nn.RMSProp`.

    Note:
        Update `var` according to the centered RMSProp algorithm.

        ..  math::
            g_{t} = \\rho g_{t-1} + (1 - \\rho)\\nabla Q_{i}(w)

        ..  math::
            s_{t} = \\rho s_{t-1} + (1 - \\rho)(\\nabla Q_{i}(w))^2

        ..  math::
            m_{t} = \\beta m_{t-1} + \\frac{\\eta} {\\sqrt{s_{t} - g_{t}^2 + \\epsilon}} \\nabla Q_{i}(w)

        ..  math::
            w = w - m_{t}

        where, :math:`w` represents `var`, which will be updated.
        :math:`g_{t}` represents `mean_gradient`, :math:`g_{t-1}` is the last momentent of :math:`g_{t}`.
        :math:`s_{t}` represents `mean_square`, :math:`s_{t-1}` is the last momentent of :math:`s_{t}`,
        :math:`m_{t}` represents `moment`, :math:`m_{t-1}` is the last momentent of :math:`m_{t}`.
        :math:`\\rho` represents `decay`. :math:`\\beta` is the momentum term, represents `momentum`.
        :math:`\\epsilon` is a smoothing term to avoid division by zero, represents `epsilon`.
        :math:`\\eta` represents `learning_rate`. :math:`\\nabla Q_{i}(w)` represents `grad`.

    Args:
        use_locking (bool): Enable a lock to protect the update of variable tensors. Default: False.

    Inputs:
        - **var** (Tensor) - Weights to be update.
        - **mean_gradient** (Tensor) - Mean gradients, must have the same type as `var`.
        - **mean_square** (Tensor) - Mean square gradients, must have the same type as `var`.
        - **moment** (Tensor) - Delta of `var`, must have the same type as `var`.
        - **grad** (Tensor) - Gradients, must have the same type as `var`.
        - **learning_rate** (Union[Number, Tensor]) - Learning rate. Should be a float number or
          a scalar tensor with float16 or float32 data type.
        - **decay** (float) - Decay rate.
        - **momentum** (float) - Momentum.
        - **epsilon** (float) - Ridge term.

    Outputs:
        Tensor, parameters to be update.

    Examples:
        >>> centered_rms_prop = P.ApplyCenteredRMSProp()
        >>> input_x = Tensor(np.arange(-6, 6).astype(np.float32).reshape(2, 3, 2), mindspore.float32)
        >>> mean_grad = Tensor(np.arange(12).astype(np.float32).reshape(2, 3, 2), mindspore.float32)
        >>> mean_square = Tensor(np.arange(-8, 4).astype(np.float32).reshape(2, 3, 2), mindspore.float32)
        >>> moment = Tensor(np.arange(12).astype(np.float32).reshape(2, 3, 2), mindspore.float32)
        >>> grad = Tensor(np.arange(12).astype(np.float32).reshape(2, 3, 2), mindspore.float32)
        >>> learning_rate = Tensor(0.9, mindspore.float32)
        >>> decay = 0.0
        >>> momentum = 1e-10
        >>> epsilon = 0.05
        >>> result = centered_rms_prop(input_x, mean_grad, mean_square, moment, grad,
        >>>                            learning_rate, decay, momentum, epsilon)
        [[[ -6.        -9.024922]
          [-12.049845 -15.074766]
          [-18.09969  -21.124613]]
         [[-24.149532 -27.174456]
          [-30.199379 -33.2243  ]
          [-36.249226 -39.274143]]]
    """

    @prim_attr_register
    def __init__(self, use_locking=False):
        self.use_locking = validator.check_value_type("use_locking", use_locking, [bool], self.name)
        self.is_ascend = context.get_context("device_target") == "Ascend"

    def infer_shape(self, var_shape, mean_gradient_shape, mean_square_shape, moment_shape, grad_shape,
                    learning_rate_shape, decay_shape, momentum_shape, epsilon_shape):
        validator.check("var_shape", var_shape, "mean_gradient_shape", mean_gradient_shape, Rel.EQ, self.name)
        validator.check("var_shape", var_shape, "mean_square_shape", mean_square_shape, Rel.EQ, self.name)
        validator.check("var_shape", var_shape, "moment_shape", moment_shape, Rel.EQ, self.name)
        validator.check("var_shape", var_shape, "grad_shape", grad_shape, Rel.EQ, self.name)
        if self.is_ascend:
            return var_shape, mean_gradient_shape, mean_square_shape, moment_shape
        return var_shape

    def infer_dtype(self, var_dtype, mean_gradient_dtype, mean_square_dtype, moment_dtype, grad_dtype,
                    learning_rate_dtype, rho_dtype, momentum_dtype, epsilon_dtype):
        args = {"var": var_dtype, "mean_gradient": mean_gradient_dtype,
                "mean_square": mean_square_dtype, "moment": moment_dtype, "grad": grad_dtype}
        validator.check_tensor_type_same(args, mstype.number_type, self.name)

        valid_types = [mstype.float16, mstype.float32]
        args_rho = {"rho": rho_dtype, 'momentum': momentum_dtype, "epsilon": epsilon_dtype}
        validator.check_type_same(args_rho, valid_types, self.name)
        args_lr = {"learning_rate": learning_rate_dtype, "rho": rho_dtype}
        validator.check_scalar_or_tensor_type_same(args_lr, valid_types, self.name, allow_mix=True)
        if self.is_ascend:
            return var_dtype, mean_gradient_dtype, mean_square_dtype, moment_dtype
        return var_dtype


class LayerNorm(Primitive):
    r"""
    Applies the Layer Normalization to the input tensor.

    This operator will normalize the input tensor on given axis. LayerNorm is described in the paper
    `Layer Normalization <https://arxiv.org/abs/1607.06450>`_.

    .. math::
        y = \frac{x - mean}{\sqrt{variance + \epsilon}} * \gamma + \beta

    where :math:`\gamma` is scale, :math:`\beta` is bias, :math:`\epsilon` is epsilon.

    Args:
        begin_norm_axis (int): The begin axis of the `input_x` to apply LayerNorm,
            the value should be in [-1, rank(input)). Default: 1.
        begin_params_axis (int): The begin axis of the parameter input (`gamma`, `beta`) to
            apply LayerNorm, the value should be in [-1, rank(input)). Default: 1.
        epsilon (float): A value added to the denominator for numerical stability. Default: 1e-7.

    Inputs:
        - **input_x** (Tensor) - Tensor of shape :math:`(N, \ldots)`.
          The input of LayerNorm.
        - **gamma** (Tensor) - Tensor of shape :math:`(P_0, \ldots, P_\text{begin_params_axis})`.
          The learnable parameter `gamma` as the scale on norm.
        - **beta** (Tensor) - Tensor of shape :math:`(P_0, \ldots, P_\text{begin_params_axis})`.
          The learnable parameter `beta` as the scale on norm.

    Outputs:
        tuple[Tensor], tuple of 3 tensors, the normalized input and the updated parameters.

        - **output_x** (Tensor) - The normalized input, has the same type and shape as the `input_x`.
          The shape is :math:`(N, C)`.
        - **mean** (Tensor) - Tensor of shape :math:`(C,)`.
        - **variance** (Tensor) - Tensor of shape :math:`(C,)`.

    Examples:
        >>> input_x = Tensor(np.array([[1, 2, 3], [1, 2, 3]]), mindspore.float32)
        >>> gamma = Tensor(np.ones([3]), mindspore.float32)
        >>> beta = Tensor(np.ones([3]), mindspore.float32)
        >>> layer_norm = P.LayerNorm()
        >>> output = layer_norm(input_x, gamma, beta)
        ([[-0.22474492, 1., 2.2247488], [-0.22474492, 1., 2.2247488]],
         [[2.], [2.]], [[0.6666667], [0.6666667]])
    """

    @prim_attr_register
    def __init__(self, begin_norm_axis=1, begin_params_axis=1, epsilon=1e-7):
        validator.check_value_type('begin_norm_axis', begin_norm_axis, [int], self.name)
        validator.check_value_type('begin_params_axis', begin_params_axis, [int], self.name)
        validator.check_value_type('epsilon', epsilon, [float], self.name)


class L2Normalize(PrimitiveWithInfer):
    r"""
    L2 normalization Operator.

    This operator will normalizes the input using the given axis. The function is shown as follows:

    .. math::
        \text{output} = \frac{x}{\sqrt{\text{max}(\text{sum} (\text{input_x}^2), \epsilon)}},

    where :math:`\epsilon` is epsilon.

    Args:
        axis (int): The begin axis for the input to apply L2 normalize. Default: 0.
        epsilon (float): A small value added for numerical stability. Default: 1e-4.

    Inputs:
        - **input_x** (Tensor) - Input to compute the normalization. Data type should be float16 or float32.

    Outputs:
        Tensor, with the same type and shape as the input.

    Examples:
        >>> l2_normalize = P.L2Normalize()
        >>> input_x = Tensor(np.random.randint(-256, 256, (2, 3, 4)), mindspore.float32)
        >>> result = l2_normalize(input_x)
        [[[-0.47247353   -0.30934513   -0.4991462   0.8185567 ]
          [-0.08070751   -0.9961299    -0.5741758   0.09262337]
          [-0.9916556    -0.3049123     0.5730487  -0.40579924]
         [[-0.88134485    0.9509498    -0.86651784  0.57442576]
          [ 0.99673784    0.08789381   -0.8187321   0.9957012 ]
          [ 0.12891524   -0.9523804    -0.81952125  0.91396334]]]
    """

    @prim_attr_register
    def __init__(self, axis=0, epsilon=1e-4):
        validator.check_value_type('axis', axis, [int], self.name)
        validator.check_value_type('epsilon', epsilon, [int, float], self.name)

    def infer_shape(self, input_x):
        dim = len(input_x)
        validator.check_int_range('axis value', self.axis, -dim, dim, Rel.INC_LEFT, self.name)
        return input_x

    def infer_dtype(self, input_x):
        validator.check_subclass("x", input_x, mstype.tensor, self.name)
        validator.check_tensor_type_same({"input_x": input_x}, [mstype.float16, mstype.float32], self.name)
        return input_x


class DropoutGenMask(Primitive):
    """
    Generates the mask value for the input shape.

    Args:
        Seed0 (int): Seed0 value for random generating. Default: 0.
        Seed1 (int): Seed1 value for random generating. Default: 0.

    Inputs:
        - **shape** (tuple[int]) - The shape of target mask.
        - **keep_prob** (Tensor) - The keep rate, between 0 and 1, e.g. keep_prob = 0.9,
          means dropping out 10% of input units.

    Outputs:
        Tensor, the value of generated mask for input shape.

    Examples:
        >>> dropout_gen_mask = P.DropoutGenMask()
        >>> shape = (20, 16, 50)
        >>> keep_prob = Tensor(0.5, mindspore.float32)
        >>> mask = dropout_gen_mask(shape, keep_prob)
    """

    @prim_attr_register
    def __init__(self, Seed0=0, Seed1=0):
        self.init_prim_io_names(inputs=['shape', 'keep_prob'], outputs=['output'])
        validator.check_value_type("Seed0", Seed0, [int], self.name)
        validator.check_value_type("Seed1", Seed1, [int], self.name)
        self.add_prim_attr("_random_effect", True)


class DropoutDoMask(PrimitiveWithInfer):
    """
    Applies dropout mask on the input tensor.

    Take the mask output of DropoutGenMask as input, and apply dropout on the input.

    Inputs:
        - **input_x** (Tensor) - The input tensor.
        - **mask** (Tensor) - The mask to be applied on `input_x`, which is the output of `DropoutGenMask`. And the
          shape of `input_x` must be same as the value of `DropoutGenMask`'s input `shape`. If input wrong `mask`,
          the output of `DropoutDoMask` are unpredictable.
        - **keep_prob** (Tensor) - The keep rate, between 0 and 1, e.g. keep_prob = 0.9,
          means dropping out 10% of input units. The value of `keep_prob` is the same as the input `keep_prob` of
          `DropoutGenMask`.

    Outputs:
        Tensor, the value that applied dropout on.

    Examples:
        >>> x = Tensor(np.ones([20, 16, 50]), mindspore.float32)
        >>> shape = (20, 16, 50)
        >>> keep_prob = Tensor(0.5, mindspore.float32)
        >>> dropout_gen_mask = P.DropoutGenMask()
        >>> dropout_do_mask = P.DropoutDoMask()
        >>> mask = dropout_gen_mask(shape, keep_prob)
        >>> output = dropout_do_mask(x, mask, keep_prob)
        >>> assert output.shape == (20, 16, 50)
    """

    @prim_attr_register
    def __init__(self):
        pass

    def __infer__(self, input_x, mask, keep_prob):
        input_x_shape = input_x['shape']
        mask_shape = mask['shape']
        keep_prob_shape = keep_prob['shape']
        validator.check("keep_prob's dim", len(keep_prob_shape), '0(scalar)', 0, Rel.EQ, self.name)
        size_x = reduce(lambda x, y: x * y, input_x_shape)
        if len(mask_shape) != 1:
            raise ValueError("DropoutDoMask mask shape should be 1-dimension.")
        size_y = mask_shape[0] * 8
        if size_x > size_y:
            raise ValueError(f"DropoutDoMask y mask do not math input input_x shape:"
                             "{input_x_shape}, mask shape: {mask_shape}.")

        validator.check_tensor_type_same({"input_x": input_x['dtype']}, [mstype.float32, mstype.float16, mstype.int32],
                                         self.name)
        validator.check_tensor_type_same({"input_mask": mask['dtype']}, [mstype.uint8], self.name)

        keep_prob_v = keep_prob['value']
        if keep_prob_v is not None:
            validator.check_number_range('keep_prob', keep_prob_v.asnumpy(), 0, 1, Rel.INC_BOTH, self.name)

        out = {'shape': input_x_shape,
               'dtype': input_x['dtype'],
               'value': None}
        return out


class ResizeBilinear(PrimitiveWithInfer):
    r"""
    Resizes the image to certain size using bilinear interpolation.

    The resizing only affects the lower two dimensions which represent the height and width. The input images
    can be represented by different data types, but the data types of output images are always float32.

    Args:
        size (tuple[int]): A tuple of 2 int elements `(new_height, new_width)`, the new size for the images.
        align_corners (bool): If it's true, rescale input by `(new_height - 1) / (height - 1)`,
                       which exactly aligns the 4 corners of images and resized images. If it's false,
                       rescale by `new_height / height`. Default: False.

    Inputs:
        - **input** (Tensor) - Image to be resized. Tensor of shape `(N_i, ..., N_n, height, width)`,
          with data type of float32 or float16.

    Outputs:
        Tensor, resized image. Tensor of shape `(N_i, ..., N_n, new_height, new_width)` in `float32`.

    Examples:
        >>> tensor = Tensor([[[[1, 2, 3, 4, 5], [1, 2, 3, 4, 5]]]], mindspore.float32)
        >>> resize_bilinear = P.ResizeBilinear((5, 5))
        >>> result = resize_bilinear(tensor)
        >>> assert result.shape == (1, 1, 5, 5)
    """

    @prim_attr_register
    def __init__(self, size, align_corners=False):
        pass

    def infer_shape(self, input_shape):
        input_shape = list(input_shape)
        batch, channel, _, _ = input_shape
        out_shape = [batch, channel]
        for i in self.size:
            out_shape.append(int(i))
        return out_shape

    def infer_dtype(self, input_dtype):
        validator.check_tensor_type_same({'input_dtype': input_dtype}, [mstype.float16, mstype.float32], self.name)
        return mstype.tensor_type(mstype.float32)


class OneHot(PrimitiveWithInfer):
    r"""
    Computes a one-hot tensor.

    Makes a new tensor, whose locations represented by indices in `indices` take value `on_value`, while all
    other locations take value `off_value`.

    Note:
        If the input indices is rank `N`, the output will have rank `N+1`. The new axis is created at dimension `axis`.

    Args:
        axis (int): Position to insert the value. e.g. If `indices` shape is [n, c], and `axis` is `-1` the output shape
            will be [n, c, depth], If `axis` is `0` the output shape will be [depth, n, c]. Default: -1.

    Inputs:
        - **indices** (Tensor) - A tensor of indices. Tensor of shape :math:`(X_0, \ldots, X_n)`.
          Data type must be int32.
        - **depth** (int) - A scalar defining the depth of the one hot dimension.
        - **on_value** (Tensor) - A value to fill in output when `indices[j] = i`. With data type of float16 or float32.
        - **off_value** (Tensor) - A value to fill in output when `indices[j] != i`.
          Has the same data type with as `on_value`.

    Outputs:
        Tensor, one_hot tensor. Tensor of shape :math:`(X_0, \ldots, X_{axis}, \text{depth} ,X_{axis+1}, \ldots, X_n)`.

    Examples:
        >>> indices = Tensor(np.array([0, 1, 2]), mindspore.int32)
        >>> depth, on_value, off_value = 3, Tensor(1.0, mindspore.float32), Tensor(0.0, mindspore.float32)
        >>> onehot = P.OneHot()
        >>> result = onehot(indices, depth, on_value, off_value)
        [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    """

    @prim_attr_register
    def __init__(self, axis=-1):
        self.init_prim_io_names(inputs=['indices', 'depth', 'on_value', 'off_value'], outputs=['output'])
        validator.check_value_type("axis", axis, [int], self.name)

    def __infer__(self, indices, depth, on_value, off_value):
        # check type
        validator.check_tensor_type_same({"indices": indices['dtype']}, (mstype.int32,), self.name)
        validator.check_type_name("depth", depth['dtype'], mstype.int_type, self.name)
        args = {"on_value": on_value['dtype'], "off_value": off_value['dtype']}
        validator.check_tensor_type_same(args, (mstype.float16, mstype.float32), self.name)

        # check shape
        indices_shp = indices['shape']
        validator.check_int_range("axis", self.axis, -1, len(indices_shp), Rel.INC_BOTH, self.name)
        depth_val = depth['value']
        validator.check_integer("depth", depth_val, 0, Rel.GE, self.name)
        # create new dimension at end if self.axis is -1
        _ = indices_shp.insert(self.axis, depth_val) if self.axis >= 0 else indices_shp.append(depth_val)

        return {'shape': indices_shp,
                'dtype': on_value['dtype'],
                'value': None}


class Gelu(PrimitiveWithInfer):
    r"""
    Gaussian Error Linear Units activation function.

    GeLU is described in the paper `Gaussian Error Linear Units (GELUs) <https://arxiv.org/abs/1606.08415>`_.
    And also please refer to `BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding.
    <https://arxiv.org/abs/1810.04805>`_.

    Defined as follows:

    .. math::
        \text{output} = 0.5 * x * (1 + erf(x / \sqrt{2})),

    where :math:`erf` is the "Gauss error function" .

    Inputs:
        - **input_x** (Tensor) - Input to compute the Gelu. With data type of float16 or float32.

    Outputs:
        Tensor, with the same type and shape as input.

    Examples:
        >>> tensor = Tensor(np.array([1.0, 2.0, 3.0]), mindspore.float32)
        >>> gelu = P.Gelu()
        >>> result = gelu(tensor)
    """

    @prim_attr_register
    def __init__(self):
        """init GeLU"""
        self.init_prim_io_names(inputs=['x'], outputs=['output'])

    def infer_shape(self, input_x):
        return input_x

    def infer_dtype(self, input_x):
        validator.check_tensor_type_same({"input_x": input_x}, (mstype.float16, mstype.float32), self.name)
        return input_x


class GetNext(PrimitiveWithInfer):
    """
    Returns the next element in the dataset queue.

    Note:
        GetNext op needs to be associated with network and also depends on the init_dataset interface,
        it can't be used directly as a single op.
        For details, please refer to `nn.DataWrapper` source code.

    Args:
        types (list[:class:`mindspore.dtype`]): The type of the outputs.
        shapes (list[tuple[int]]): The dimensionality of the outputs.
        output_num (int): The output number, length of `types` and `shapes`.
        shared_name (str): The queue name of `init_dataset` interface.

    Inputs:
        No inputs.

    Outputs:
        tuple[Tensor], the output of Dataset. The shape is described in `shapes`
        and the type is described is `types`.

    Examples:
        >>> get_next = P.GetNext([mindspore.float32, mindspore.int32], [[32, 1, 28, 28], [10]], 2, 'shared_name')
        >>> feature, label = get_next()
    """

    @prim_attr_register
    def __init__(self, types, shapes, output_num, shared_name):
        validator.check_value_type("types", types, [list, tuple], self.name)
        validator.check_value_type("shapes", shapes, [list, tuple], self.name)
        validator.check("types length", len(types), "shapes length", len(shapes), Rel.EQ, self.name)
        validator.check_value_type("output_num", output_num, [int], self.name)

    def infer_shape(self):
        return tuple(self.shapes)

    def infer_dtype(self):
        return tuple(self.types)


class PReLU(PrimitiveWithInfer):
    r"""
    Parametric Rectified Linear Unit activation function.

    PReLU is described in the paper `Delving Deep into Rectifiers: Surpassing Human-Level Performance on
    ImageNet Classification <https://arxiv.org/abs/1502.01852>`_. Defined as follows:

    .. math::
        prelu(x_i)= \max(0, x_i) + \min(0, w * x_i),

    where :math:`x_i` is an element of an channel of the input.

    Note:
        1-dimensional input_x is not supported.

    Inputs:
        - **input_x** (Tensor) - Float tensor, representing the output of the preview layer.
          With data type of float16 or float32.
        - **weight** (Tensor) -  Float Tensor, w > 0, there is only two shapes are legitimate,
          1 or the number of channels at input. With data type of float16 or float32.

    Outputs:
        Tensor, with the same type as `input_x`.

    Detailed information, please refer to `nn.PReLU`.

    Examples:
        >>> import mindspore
        >>> import mindspore.nn as nn
        >>> import numpy as np
        >>> from mindspore import Tensor
        >>> from mindspore.ops import operations as P
        >>> class Net(nn.Cell):
        >>>     def __init__(self):
        >>>         super(Net, self).__init__()
        >>>         self.prelu = P.PReLU()
        >>>     def construct(self, input_x, weight):
        >>>         result = self.prelu(input_x, weight)
        >>>         return result
        >>>
        >>> input_x = Tensor(np.random.randint(-3, 3, (2, 3, 2)), mindspore.float32)
        >>> weight = Tensor(np.array([0.1, 0.6, -0.3]), mindspore.float32)
        >>> net = Net()
        >>> result = net(input_x, weight)
        [[[-0.1      1.        ]
          [ 0.       2.        ]
          [0.        0.        ]]

         [[-0.2     -0.1      ]
          [2.       -1.8000001]
          [0.6       0.6       ]]]
    """

    @prim_attr_register
    def __init__(self):
        pass

    def infer_shape(self, input_x_shape, weight_shape):
        input_x_dim = len(input_x_shape)
        weight_dim = len(weight_shape)

        if input_x_dim == 1:
            raise ValueError(f'For \'{self.name}\' input_x rank 1 is not supported.')

        if weight_dim != 1:
            raise ValueError(f'For \'{self.name}\' weight_dim must be 1, while weight_dim is {weight_dim}.')

        if weight_shape[0] != input_x_shape[1] and weight_shape[0] != 1:
            raise ValueError(f'For \'{self.name}\' channel of input_x and weight must be matched,'
                             f' while channel of input_x is {input_x_shape[1]},'
                             f' weight_shape[0] is {weight_shape[0]}.')

        return input_x_shape

    def infer_dtype(self, input_x_dtype, weight_dtype):
        valid_types = (mstype.float16, mstype.float32)
        validator.check_tensor_type_same({"input_x": input_x_dtype}, valid_types, self.name)
        validator.check_tensor_type_same({"weight": weight_dtype}, valid_types, self.name)
        return input_x_dtype


class LSTM(PrimitiveWithInfer):
    """
    Performs the long short term memory(LSTM) on the input.

    Detailed information, please refer to `nn.LSTM`.
    """

    @prim_attr_register
    def __init__(self, input_size, hidden_size, num_layers, has_bias, bidirectional, dropout):
        self.input_size = validator.check_integer("input_size", input_size, 0, Rel.GT, self.name)
        self.hidden_size = validator.check_integer("hidden_size", hidden_size, 0, Rel.GT, self.name)
        self.num_layers = validator.check_integer("num_layers", num_layers, 0, Rel.GT, self.name)
        self.has_bias = validator.check_value_type("has_bias", has_bias, (bool,), self.name)
        self.bidirectional = validator.check_value_type("bidirectional", bidirectional, (bool,), self.name)
        self.dropout = validator.check_value_type("dropout", dropout, [float], self.name)
        self.dropout = validator.check_number_range('dropout', dropout, 0, 1, Rel.INC_BOTH, self.name)

        if bidirectional:
            self.num_directions = 2
        else:
            self.num_directions = 1

    def infer_shape(self, x_shape, h_shape, c_shape, w_shape):
        # (seq, batch_size, feature)
        validator.check_integer("x rank", len(x_shape), 3, Rel.EQ, self.name)
        validator.check_integer("x[2]", x_shape[2], self.input_size, Rel.EQ, self.name)

        # h and c should be same shape
        validator.check_integer("h rank", len(h_shape), 3, Rel.EQ, self.name)
        validator.check("h_shape", h_shape, "c_shape", c_shape, Rel.EQ, self.name)

        # (num_layers * num_directions, batch, hidden_size)
        validator.check_integer("h[0]", h_shape[0], self.num_layers * self.num_directions, Rel.EQ, self.name)
        validator.check_integer("h[1]", h_shape[1], x_shape[1], Rel.EQ, self.name)
        validator.check_integer("h[2]", h_shape[2], self.hidden_size, Rel.EQ, self.name)

        y_shape = (x_shape[0], x_shape[1], self.hidden_size * self.num_directions)

        # set arbitrary shape for reserved space
        type_size = 4
        gates_ws_ld = self.get_good_ld(self.hidden_size * 4, type_size)
        states_ws_ld = self.get_good_ld(max(self.hidden_size, self.input_size), type_size)
        self.ws_gates_size = self.num_layers * self.num_directions * x_shape[0] * x_shape[1] * gates_ws_ld * type_size
        self.ws_states_size = (self.num_layers + 1) * self.num_directions * (x_shape[0] + 1) * x_shape[
            1] * states_ws_ld * type_size
        self.ws_c_states_size = (self.num_layers + 1) * self.num_directions * (x_shape[0] + 1) * x_shape[
            1] * states_ws_ld * type_size
        self.ws_diff_states_size = (self.num_layers + 1) * self.num_directions * (x_shape[0] + 1) * (2 + 1) * x_shape[
            1] * states_ws_ld * type_size
        self.ws_grid_comp_size = 0
        self.page_size = 4096
        current_offset = 0
        current_offset += self.ws_gates_size
        current_offset = self.rnd_up(current_offset, self.page_size)
        current_offset += self.ws_states_size
        current_offset = self.rnd_up(current_offset, self.page_size)
        current_offset += self.ws_c_states_size
        current_offset = self.rnd_up(current_offset, self.page_size)
        current_offset += self.ws_diff_states_size
        current_offset = self.rnd_up(current_offset, self.page_size)
        current_offset += self.ws_grid_comp_size
        reserved_shape = (current_offset, 1)
        state_shape = (1, 1)
        return (y_shape, h_shape, c_shape, reserved_shape, state_shape)

    def infer_dtype(self, x_dtype, h_dtype, c_dtype, w_dtype):
        args = {'x': x_dtype, 'h': h_dtype, 'c': c_dtype, 'w': w_dtype}
        validator.check_tensor_type_same(args, (mstype.float32, mstype.float16), self.name)
        return (x_dtype, x_dtype, x_dtype, x_dtype, x_dtype)

    def rnd_up(self, current_offset, page_size):
        return ((current_offset + page_size - 1) // page_size) * page_size

    def get_good_ld(self, dim, type_size):
        ld = self.rnd_up(dim, 64 // type_size)
        if ld * 256 == 0:
            return ld + 64 // type_size
        return ld


class SigmoidCrossEntropyWithLogits(PrimitiveWithInfer):
    r"""
    Uses the given logits to compute sigmoid cross entropy.

    Note:
        Sets input logits as `X`, input label as `Y`, output as `loss`. Then,

        .. math::
            p_{ij} = sigmoid(X_{ij}) = \frac{1}{1 + e^{-X_{ij}}}

        .. math::
            loss_{ij} = -[Y_{ij} * ln(p_{ij}) + (1 - Y_{ij})ln(1 - p_{ij})]

    Inputs:
        - **logits** (Tensor) - Input logits.
        - **label** (Tensor) - Ground truth label.

    Outputs:
        Tensor, with the same shape and type as input `logits`.

    Examples:
        >>> logits = Tensor(np.random.randn(2, 3).astype(np.float16))
        >>> labels = Tensor(np.random.randn(2, 3).astype(np.float16))
        >>> sigmoid = P.SigmoidCrossEntropyWithLogits()
        >>> sigmoid(logits, labels)
    """

    @prim_attr_register
    def __init__(self):
        """Init SigmoidCrossEntropyWithLogits"""
        self.init_prim_io_names(inputs=['predict', 'target'], outputs=['loss'])

    def infer_shape(self, x_shape, y_shape):
        validator.check("x_shape", x_shape, "y_shape", y_shape, Rel.EQ, self.name)
        return x_shape

    def infer_dtype(self, x_dtype, y_dtype):
        args = {"x_dtype": x_dtype, "y_dtype": y_dtype}
        validator.check_tensor_type_same(args, mstype.number_type, self.name)
        return x_dtype


class Pad(PrimitiveWithInfer):
    """
    Pads input tensor according to the paddings.

    Args:
        paddings (tuple): The shape of parameter `paddings` is (N, 2). N is the rank of input data. All elements of
            paddings are int type. For the input in `D` th dimension, paddings[D, 0] indicates how many sizes to be
            extended ahead of the input tensor in the `D` th dimension, and paddings[D, 1] indicates how many sizes to
            be extended behind of the input tensor in the `D` th dimension.

    Inputs:
        - **input_x** (Tensor) - The input tensor.

    Outputs:
        Tensor, the tensor after padding.

    Examples:
        >>> input_tensor = Tensor(np.array([[-0.1, 0.3, 3.6], [0.4, 0.5, -3.2]]), mindspore.float32)
        >>> pad_op = P.Pad(((1, 2), (2, 1)))
        >>> output_tensor = pad_op(input_tensor)
        >>> assert output_tensor == Tensor(np.array([[ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
        >>>                                          [ 0. ,  0. , -0.1,  0.3,  3.6,  0. ],
        >>>                                          [ 0. ,  0. ,  0.4,  0.5, -3.2,  0. ],
        >>>                                          [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
        >>>                                          [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ]]), mindspore.float32)
    """

    @prim_attr_register
    def __init__(self, paddings):
        """Init Pad"""
        self.init_prim_io_names(inputs=['x'], outputs=['y'])
        if not isinstance(paddings, tuple):
            raise TypeError('Paddings must be tuple type.')
        for item in paddings:
            if len(item) != 2:
                raise ValueError('The shape of paddings must be (n, 2).')
        self.paddings = paddings

    def infer_shape(self, x):
        paddings = np.array(self.paddings)
        validator.check_integer('paddings.shape', paddings.size, len(x) * 2, Rel.EQ, self.name)
        if not np.all(paddings >= 0):
            raise ValueError('All elements of paddings must be >= 0.')
        y_shape = ()
        for i in range(int(paddings.size / 2)):
            y_shape += ((x[i] + paddings[i, 0] + paddings[i, 1]),)
        return y_shape

    def infer_dtype(self, x):
        validator.check_subclass("input_x", x, mstype.tensor, self.name)
        return x


class MirrorPad(PrimitiveWithInfer):
    """
    Pads the input tensor according to the paddings and mode.

    Args:
        mode (str): Specifies padding mode. The optional values are "REFLECT", "SYMMETRIC".
            Default: "REFLECT".

    Inputs:
        - **input_x** (Tensor) - The input tensor.
        - **paddings** (Tensor) - The paddings tensor. The value of `paddings` is a matrix(list),
          and its shape is (N, 2). N is the rank of input data. All elements of paddings
          are int type. For the input in `D` th dimension, paddings[D, 0] indicates how many sizes to be
          extended ahead of the input tensor in the `D` th dimension, and paddings[D, 1] indicates how many sizes to
          be extended behind of the input tensor in the `D` th dimension.

    Outputs:
        Tensor, the tensor after padding.

        - If `mode` is "REFLECT", it uses a way of symmetrical copying throught the axis of symmetry to fill in.
          If the `input_x` is [[1,2,3],[4,5,6],[7,8,9]] and `paddings` is [[1,1],[2,2]], then the
          Outputs is [[6,5,4,5,6,5,4],[3,2,1,2,3,2,1],[6,5,4,5,6,5,4],[9,8,7,8,9,8,7],[6,5,4,5,6,5,4]].
        - If `mode` is "SYMMETRIC", the filling method is similar to the "REFLECT". It is also copied
          according to the symmetry axis, except that it includes the symmetry axis. If the `input_x`
          is [[1,2,3],[4,5,6],[7,8,9]] and `paddings` is [[1,1],[2,2]], then the Outputs is
          [[2,1,1,2,3,3,2],[2,1,1,2,3,3,2],[5,4,4,5,6,6,5],[8,7,7,8,9,9,8],[8,7,7,8,9,9,8]].

    Examples:
        >>> from mindspore import Tensor
        >>> from mindspore.ops import operations as P
        >>> import mindspore.nn as nn
        >>> import numpy as np
        >>> class Net(nn.Cell):
        >>>     def __init__(self):
        >>>         super(Net, self).__init__()
        >>>         self.pad = P.MirrorPad(mode="REFLECT")
        >>>     def construct(self, x, paddings):
        >>>         return self.pad(x, paddings)
        >>> x = np.random.random(size=(2, 3)).astype(np.float32)
        >>> paddings = Tensor([[1,1],[2,2]])
        >>> pad = Net()
        >>> ms_output = pad(Tensor(x), paddings)
    """

    @prim_attr_register
    def __init__(self, mode='REFLECT'):
        """Init Pad"""
        validator.check_string('mode', mode, ['REFLECT', 'SYMMETRIC'], self.name)
        self.mode = mode

    def __infer__(self, input_x, paddings):
        validator.check_subclass("input_x", input_x['dtype'], mstype.tensor, self.name)
        validator.check_subclass("paddings", paddings['dtype'], mstype.tensor, self.name)
        x_shape = list(input_x['shape'])
        paddings_value = paddings['value'].asnumpy()
        paddings_size = paddings_value.size
        validator.check_integer('paddings.shape', paddings_size, len(x_shape) * 2, Rel.EQ, self.name)
        if not np.all(paddings_value >= 0):
            raise ValueError('All elements of paddings must be >= 0.')
        adjust = 0
        if self.mode == 'SYMMETRIC':
            adjust = 1
        for i in range(0, int(paddings_size / 2)):
            if (paddings_value[i, 0] >= x_shape[i] + adjust) or (paddings_value[i, 1] >= x_shape[i] + adjust):
                raise ValueError('At least one dim has too high a padding value for this input and mode')
        y_shape = ()
        for i in range(0, int(paddings_size / 2)):
            y_shape += ((x_shape[i] + paddings_value[i, 0] + paddings_value[i, 1]),)
        return {'shape': y_shape,
                'dtype': input_x['dtype'],
                'value': None}


class ROIAlign(PrimitiveWithInfer):
    """
    Computes Region of Interest (RoI) Align operator.

    The operator computes the value of each sampling point by bilinear interpolation from the nearby grid points on the
    feature map. No quantization is performed on any coordinates involved in the RoI, its bins, or the sampling
    points. The details of (RoI) Align operator are described in `Mask R-CNN <https://arxiv.org/abs/1703.06870>`_.

    Args:
        pooled_height (int): The output features' height.
        pooled_width (int): The output features' width.
        spatial_scale (float): A scaling factor that maps the raw image coordinates to the input
            feature map coordinates. Suppose the height of a RoI is `ori_h` in the raw image and `fea_h` in the
            input feature map, the `spatial_scale` should be `fea_h / ori_h`.
        sample_num (int): Number of sampling points. Default: 2.
        roi_end_mode (int): Number must be 0 or 1. Default: 1.

    Inputs:
        - **features** (Tensor) - The input features, whose shape should be `(N, C, H, W)`.
        - **rois** (Tensor) - The shape is `(rois_n, 5)`. With data type of float16 or float32.
          `rois_n` represents the number of RoI. The size of the second dimension should be `5` and the `5` colunms
          are `(image_index, top_left_x, top_left_y, bottom_right_x, bottom_right_y)`. `image_index` represents the
          index of image. `top_left_x` and `top_left_y` represent the `x, y` coordinates of the top left corner
          of corresponding RoI, respectively. `bottom_right_x` and `bottom_right_y` represent the `x, y`
          coordinates of the bottom right corner of corresponding RoI, respectively.

    Outputs:
        Tensor, the shape is `(rois_n, C, pooled_height, pooled_width)`.

    Examples:
        >>> input_tensor = Tensor(np.array([[[[1., 2.], [3., 4.]]]]), mindspore.float32)
        >>> rois = Tensor(np.array([[0, 0.2, 0.3, 0.2, 0.3]]), mindspore.float32)
        >>> roi_align = P.ROIAlign(2, 2, 0.5, 2)
        >>> output_tensor = roi_align(input_tensor, rois)
        >>> assert output_tensor == Tensor(np.array([[[[2.15]]]]), mindspore.float32)
    """

    @prim_attr_register
    def __init__(self, pooled_height, pooled_width, spatial_scale, sample_num=2, roi_end_mode=1):
        """init ROIAlign"""
        validator.check_value_type("pooled_height", pooled_height, [int], self.name)
        validator.check_value_type("pooled_width", pooled_width, [int], self.name)
        validator.check_value_type("spatial_scale", spatial_scale, [float], self.name)
        validator.check_value_type("sample_num", sample_num, [int], self.name)
        validator.check_value_type("roi_end_mode", roi_end_mode, [int], self.name)
        validator.check_int_range("roi_end_mode", roi_end_mode, 0, 1, Rel.INC_BOTH, self.name)
        self.pooled_height = pooled_height
        self.pooled_width = pooled_width
        self.spatial_scale = spatial_scale
        self.sample_num = sample_num
        self.roi_end_mode = roi_end_mode

    def infer_shape(self, inputs_shape, rois_shape):
        return [rois_shape[0], inputs_shape[1], self.pooled_height, self.pooled_width]

    def infer_dtype(self, inputs_type, rois_type):
        valid_types = (mstype.float16, mstype.float32)
        validator.check_tensor_type_same({"inputs_type": inputs_type}, valid_types, self.name)
        validator.check_tensor_type_same({"rois_type": rois_type}, valid_types, self.name)
        return inputs_type


class Adam(PrimitiveWithInfer):
    r"""
    Updates gradients by Adaptive Moment Estimation (Adam) algorithm.

    The Adam algorithm is proposed in `Adam: A Method for Stochastic Optimization <https://arxiv.org/abs/1412.6980>`_.

    The updating formulas are as follows,

    .. math::
        \begin{array}{ll} \\
            m = \beta_1 * m + (1 - \beta_1) * g \\
            v = \beta_2 * v + (1 - \beta_2) * g * g \\
            l = \alpha * \frac{\sqrt{1-\beta_2^t}}{1-\beta_1^t} \\
            w = w - l * \frac{m}{\sqrt{v} + \epsilon}
        \end{array}

    :math:`m` represents the 1st moment vector, :math:`v` represents the 2nd moment vector, :math:`g` represents
    `gradient`, :math:`l` represents scaling factor `lr`, :math:`\beta_1, \beta_2` represent `beta1` and `beta2`,
    :math:`t` represents updating step while :math:`beta_1^t` and :math:`beta_2^t` represent `beta1_power` and
    `beta2_power`, :math:`\alpha` represents `learning_rate`, :math:`w` represents `var`, :math:`\epsilon` represents
    `epsilon`.

    Args:
        use_locking (bool): Whether to enable a lock to protect updating variable tensors.
            If true, updates of the var, m, and v tensors will be protected by a lock.
            If false, the result is unpredictable. Default: False.
        use_nesterov (bool): Whether to use Nesterov Accelerated Gradient (NAG) algorithm to update the gradients.
            If true, update the gradients using NAG.
            If true, update the gradients without using NAG. Default: False.

    Inputs:
        - **var** (Tensor) - Weights to be updated.
        - **m** (Tensor) - The 1st moment vector in the updating formula. Has the same type as `var`.
        - **v** (Tensor) - the 2nd moment vector in the updating formula.
          Mean square gradients, has the same type as `var`.
        - **beta1_power** (float) - :math:`beta_1^t` in the updating formula.
        - **beta2_power** (float) - :math:`beta_2^t` in the updating formula.
        - **lr** (float) - :math:`l` in the updating formula.
        - **beta1** (float) - The exponential decay rate for the 1st moment estimations.
        - **beta2** (float) - The exponential decay rate for the 2nd moment estimations.
        - **epsilon** (float) - Term added to the denominator to improve numerical stability.
        - **gradient** (Tensor) - Gradients. Has the same type as `var`.

    Outputs:
        Tuple of 3 Tensor, the updated parameters.

        - **var** (Tensor) - The same shape and data type as `var`.
        - **m** (Tensor) - The same shape and data type as `m`.
        - **v** (Tensor) - The same shape and data type as `v`.

    Examples:
        >>> import numpy as np
        >>> import mindspore.nn as nn
        >>> from mindspore import Tensor, Parameter
        >>> from mindspore.ops import operations as P
        >>> class Net(nn.Cell):
        >>>     def __init__(self):
        >>>         super(Net, self).__init__()
        >>>         self.apply_adam = P.Adam()
        >>>         self.var = Parameter(Tensor(np.ones([3, 3, 3]).astype(np.float32)), name="var")
        >>>         self.m = Parameter(Tensor(np.ones([3, 3, 3]).astype(np.float32)), name="m")
        >>>         self.v = Parameter(Tensor(np.ones([3, 3, 3]).astype(np.float32)), name="v")
        >>>     def construct(self, beta1_power, beta2_power, lr, beta1, beta2, epsilon, grad):
        >>>         out = self.apply_adam(self.var, self.m, self.v, beta1_power, beta2_power, lr, beta1, beta2,
        >>>                               epsilon, grad)
        >>>         return out
        >>> net = Net()
        >>> gradient = Tensor(np.random.rand(3, 3, 3).astype(np.float32))
        >>> result = net(0.9, 0.999, 0.001, 0.9, 0.999, 1e-8, gradient)
    """
    @prim_attr_register
    def __init__(self, use_locking=False, use_nesterov=False):
        validator.check_value_type("use_locking", use_locking, [bool], self.name)
        validator.check_value_type("use_nesterov", use_nesterov, [bool], self.name)

    def infer_shape(self, var_shape, m_shape, v_shape, beta1_power_shape, beta2_power_shape, lr_shape,
                    beta1_shape, beta2_shape, epsilon_shape, grad_shape):
        validator.check("var_shape", var_shape, "m_shape", m_shape, Rel.EQ, self.name)
        validator.check("var_shape", var_shape, "v_shape", v_shape, Rel.EQ, self.name)
        validator.check("var_shape", var_shape, "grad_shape", grad_shape, Rel.EQ, self.name)
        return var_shape, m_shape, v_shape

    def infer_dtype(self, var_dtype, m_dtype, v_dtype, beta1_power_dtype, beta2_power_dtype, lr_dtype,
                    beta1_dtype, beta2_dtype, epsilon_dtype, grad_dtype):
        args = {"var": var_dtype, "m": m_dtype, "v": v_dtype, "grad": grad_dtype}
        validator.check_tensor_type_same(args, mstype.number_type, self.name)

        args = {"beta1_power": beta1_power_dtype, "beta2_power": beta2_power_dtype, 'lr': lr_dtype,
                "beta1": beta1_dtype, "beta2": beta2_dtype, "epsilon": epsilon_dtype}
        validator.check_scalar_or_tensor_type_same(args, [mstype.float16, mstype.float32], self.name, True)
        return var_dtype, m_dtype, v_dtype


class FusedSparseAdam(PrimitiveWithInfer):
    r"""
    Merge the duplicate value of the gradient and then updates parameters by Adaptive Moment Estimation (Adam)
    algorithm. This operator is used when the gradient is sparse.

    The Adam algorithm is proposed in `Adam: A Method for Stochastic Optimization <https://arxiv.org/abs/1412.6980>`_.

    The updating formulas are as follows,

    .. math::
        \begin{array}{ll} \\
            m = \beta_1 * m + (1 - \beta_1) * g \\
            v = \beta_2 * v + (1 - \beta_2) * g * g \\
            l = \alpha * \frac{\sqrt{1-\beta_2^t}}{1-\beta_1^t} \\
            w = w - l * \frac{m}{\sqrt{v} + \epsilon}
        \end{array}

    :math:`m` represents the 1st moment vector, :math:`v` represents the 2nd moment vector, :math:`g` represents
    `gradient`, :math:`l` represents scaling factor `lr`, :math:`\beta_1, \beta_2` represent `beta1` and `beta2`,
    :math:`t` represents updating step while :math:`beta_1^t` and :math:`beta_2^t` represent `beta1_power` and
    `beta2_power`, :math:`\alpha` represents `learning_rate`, :math:`w` represents `var`, :math:`\epsilon` represents
    `epsilon`.

    Args:
        use_locking (bool): Whether to enable a lock to protect updating variable tensors.
            If true, updates of the var, m, and v tensors will be protected by a lock.
            If false, the result is unpredictable. Default: False.
        use_nesterov (bool): Whether to use Nesterov Accelerated Gradient (NAG) algorithm to update the gradients.
            If true, update the gradients using NAG.
            If true, update the gradients without using NAG. Default: False.

    Inputs:
        - **var** (Parameter) - Parameters to be updated. With float32 data type.
        - **m** (Parameter) - The 1st moment vector in the updating formula. Has the same type as `var`. With
                              float32 data type.
        - **v** (Parameter) - The 2nd moment vector in the updating formula. Mean square gradients,
          has the same type as `var`. With float32 data type.
        - **beta1_power** (Tensor) - :math:`beta_1^t` in the updating formula. With float32 data type.
        - **beta2_power** (Tensor) - :math:`beta_2^t` in the updating formula. With float32 data type.
        - **lr** (Tensor) - :math:`l` in the updating formula. With float32 data type.
        - **beta1** (Tensor) - The exponential decay rate for the 1st moment estimations. With float32 data type.
        - **beta2** (Tensor) - The exponential decay rate for the 2nd moment estimations. With float32 data type.
        - **epsilon** (Tensor) - Term added to the denominator to improve numerical stability. With float32 data type.
        - **gradient** (Tensor) - Gradient value. With float32 data type.
        - **indices** (Tensor) - Gradient indices. With int32 data type.

    Outputs:
        Tuple of 3 Tensor, this operator will update the input parameters directly, the outputs are useless.

        - **var** (Tensor) - A Tensor with shape (1,).
        - **m** (Tensor) - A Tensor with shape (1,).
        - **v** (Tensor) - A Tensor with shape (1,).

    Examples:
        >>> import numpy as np
        >>> import mindspore.nn as nn
        >>> from mindspore import Tensor, Parameter
        >>> from mindspore.ops import operations as P
        >>> import mindspore.common.dtype as mstype
        >>> class Net(nn.Cell):
        >>>     def __init__(self):
        >>>         super(Net, self).__init__()
        >>>         self.sparse_apply_adam = P.FusedSparseAdam()
        >>>         self.var = Parameter(Tensor(np.ones([3, 1, 2]).astype(np.float32)), name="var")
        >>>         self.m = Parameter(Tensor(np.ones([3, 1, 2]).astype(np.float32)), name="m")
        >>>         self.v = Parameter(Tensor(np.ones([3, 1, 2]).astype(np.float32)), name="v")
        >>>     def construct(self, beta1_power, beta2_power, lr, beta1, beta2, epsilon, grad, indices):
        >>>         out = self.sparse_apply_adam(self.var, self.m, self.v, beta1_power, beta2_power, lr, beta1, beta2,
        >>>                                      epsilon, grad, indices)
        >>>         return out
        >>> net = Net()
        >>> beta1_power = Tensor(0.9, mstype.float32)
        >>> beta2_power = Tensor(0.999, mstype.float32)
        >>> lr = Tensor(0.001, mstype.float32)
        >>> beta1 = Tensor(0.9, mstype.float32)
        >>> beta2 = Tensor(0.999, mstype.float32)
        >>> epsilon = Tensor(1e-8, mstype.float32)
        >>> gradient = Tensor(np.random.rand(2, 1, 2), mstype.float32)
        >>> indices = Tensor([0, 1], mstype.int32)
        >>> result = net(beta1_power, beta2_power, lr, beta1, beta2, epsilon, gradient, indices)
    """
    __mindspore_signature__ = (
        ('var', sig_rw.RW_WRITE, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('m', sig_rw.RW_WRITE, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('v', sig_rw.RW_WRITE, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('beta1_power', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE,
         sig_dtype.T),
        ('beta2_power', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE,
         sig_dtype.T),
        ('lr', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE,
         sig_dtype.T),
        ('beta1', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE,
         sig_dtype.T),
        ('beta2', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE,
         sig_dtype.T),
        ('epsilon', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE,
         sig_dtype.T),
        ('grad', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('indices', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T1)
    )

    @prim_attr_register
    def __init__(self, use_locking=False, use_nesterov=False):
        validator.check_value_type("use_locking", use_locking, [bool], self.name)
        validator.check_value_type("use_nesterov", use_nesterov, [bool], self.name)
        self.init_prim_io_names(inputs=['var', 'm', 'v', 'beta1_power', 'beta2_power', 'lr', 'beta1', 'beta2',
                                        'epsilon', 'grad', 'indices'],
                                outputs=['var', 'm', 'v'])

    def infer_shape(self, var_shape, m_shape, v_shape, beta1_power_shape, beta2_power_shape, lr_shape,
                    beta1_shape, beta2_shape, epsilon_shape, grad_shape, indices_shape):
        validator.check("var_shape", var_shape, "m_shape", m_shape, Rel.EQ, self.name)
        validator.check("var_shape", var_shape, "v_shape", v_shape, Rel.EQ, self.name)
        validator.check_integer("indices rank", len(indices_shape), 1, Rel.EQ, self.name)
        validator.check('grad_shape[0]', grad_shape[0], 'indices_shape[0]', indices_shape[0], Rel.EQ, self.name)
        if len(var_shape) > 1 and grad_shape != indices_shape + var_shape[1:]:
            raise ValueError(f"For '{self.name}', the shape of updates should be [] or "
                             f"grad_shape = indices_shape + var_shape[1:], but got var_shape: {var_shape}, "
                             f"indices_shape: {indices_shape}, grad_shape: {grad_shape}.")
        return [1], [1], [1]

    def infer_dtype(self, var_dtype, m_dtype, v_dtype, beta1_power_dtype, beta2_power_dtype, lr_dtype,
                    beta1_dtype, beta2_dtype, epsilon_dtype, grad_dtype, indices_dtype):
        args = {"var": var_dtype, "m": m_dtype, "v": v_dtype, "grad": grad_dtype}
        validator.check_tensor_type_same(args, mstype.number_type, self.name)

        args = {"beta1_power": beta1_power_dtype, "beta2_power": beta2_power_dtype, 'lr': lr_dtype,
                "beta1": beta1_dtype, "beta2": beta2_dtype, "epsilon": epsilon_dtype}
        validator.check_scalar_or_tensor_type_same(args, [mstype.float16, mstype.float32], self.name, True)
        validator.check_tensor_type_same({"indices_dtype": indices_dtype}, [mstype.int32], self.name)
        return var_dtype, m_dtype, v_dtype


class FusedSparseLazyAdam(PrimitiveWithInfer):
    r"""
    Merge the duplicate value of the gradient and then updates parameters by Adaptive Moment Estimation (Adam)
    algorithm. This operator is used when the gradient is sparse. The behavior is not equivalent to the
    original Adam algorithm, as only the current indices parameters will be updated.

    The Adam algorithm is proposed in `Adam: A Method for Stochastic Optimization <https://arxiv.org/abs/1412.6980>`_.

    The updating formulas are as follows,

    .. math::
        \begin{array}{ll} \\
            m = \beta_1 * m + (1 - \beta_1) * g \\
            v = \beta_2 * v + (1 - \beta_2) * g * g \\
            l = \alpha * \frac{\sqrt{1-\beta_2^t}}{1-\beta_1^t} \\
            w = w - l * \frac{m}{\sqrt{v} + \epsilon}
        \end{array}

    :math:`m` represents the 1st moment vector, :math:`v` represents the 2nd moment vector, :math:`g` represents
    `gradient`, :math:`l` represents scaling factor `lr`, :math:`\beta_1, \beta_2` represent `beta1` and `beta2`,
    :math:`t` represents updating step while :math:`beta_1^t` and :math:`beta_2^t` represent `beta1_power` and
    `beta2_power`, :math:`\alpha` represents `learning_rate`, :math:`w` represents `var`, :math:`\epsilon` represents
    `epsilon`.

    Args:
        use_locking (bool): Whether to enable a lock to protect updating variable tensors.
            If true, updates of the var, m, and v tensors will be protected by a lock.
            If false, the result is unpredictable. Default: False.
        use_nesterov (bool): Whether to use Nesterov Accelerated Gradient (NAG) algorithm to update the gradients.
            If true, update the gradients using NAG.
            If true, update the gradients without using NAG. Default: False.

    Inputs:
        - **var** (Parameter) - Parameters to be updated. With float32 data type.
        - **m** (Parameter) - The 1st moment vector in the updating formula. Has the same type as `var`. With
                              float32 data type.
        - **v** (Parameter) - The 2nd moment vector in the updating formula. Mean square gradients,
          has the same type as `var`. With float32 data type.
        - **beta1_power** (Tensor) - :math:`beta_1^t` in the updating formula. With float32 data type.
        - **beta2_power** (Tensor) - :math:`beta_2^t` in the updating formula. With float32 data type.
        - **lr** (Tensor) - :math:`l` in the updating formula. With float32 data type.
        - **beta1** (Tensor) - The exponential decay rate for the 1st moment estimations. With float32 data type.
        - **beta2** (Tensor) - The exponential decay rate for the 2nd moment estimations. With float32 data type.
        - **epsilon** (Tensor) - Term added to the denominator to improve numerical stability. With float32 data type.
        - **gradient** (Tensor) - Gradient value. With float32 data type.
        - **indices** (Tensor) - Gradient indices. With int32 data type.

    Outputs:
        Tuple of 3 Tensor, this operator will update the input parameters directly, the outputs are useless.

        - **var** (Tensor) - A Tensor with shape (1,).
        - **m** (Tensor) - A Tensor with shape (1,).
        - **v** (Tensor) - A Tensor with shape (1,).

    Examples:
        >>> import numpy as np
        >>> import mindspore.nn as nn
        >>> from mindspore import Tensor, Parameter
        >>> from mindspore.ops import operations as P
        >>> import mindspore.common.dtype as mstype
        >>> class Net(nn.Cell):
        >>>     def __init__(self):
        >>>         super(Net, self).__init__()
        >>>         self.sparse_apply_lazyadam = P.FusedSparseLazyAdam()
        >>>         self.var = Parameter(Tensor(np.ones([3, 1, 2]).astype(np.float32)), name="var")
        >>>         self.m = Parameter(Tensor(np.ones([3, 1, 2]).astype(np.float32)), name="m")
        >>>         self.v = Parameter(Tensor(np.ones([3, 1, 2]).astype(np.float32)), name="v")
        >>>     def construct(self, beta1_power, beta2_power, lr, beta1, beta2, epsilon, grad, indices):
        >>>         out = self.sparse_apply_lazyadam(self.var, self.m, self.v, beta1_power, beta2_power, lr, beta1,
        >>>                                          beta2, epsilon, grad, indices)
        >>>         return out
        >>> net = Net()
        >>> beta1_power = Tensor(0.9, mstype.float32)
        >>> beta2_power = Tensor(0.999, mstype.float32)
        >>> lr = Tensor(0.001, mstype.float32)
        >>> beta1 = Tensor(0.9, mstype.float32)
        >>> beta2 = Tensor(0.999, mstype.float32)
        >>> epsilon = Tensor(1e-8, mstype.float32)
        >>> gradient = Tensor(np.random.rand(2, 1, 2), mstype.float32)
        >>> indices = Tensor([0, 1], mstype.int32)
        >>> result = net(beta1_power, beta2_power, lr, beta1, beta2, epsilon, gradient, indices)
    """
    __mindspore_signature__ = (
        ('var', sig_rw.RW_WRITE, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('m', sig_rw.RW_WRITE, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('v', sig_rw.RW_WRITE, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('beta1_power', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE,
         sig_dtype.T),
        ('beta2_power', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE,
         sig_dtype.T),
        ('lr', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE,
         sig_dtype.T),
        ('beta1', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE,
         sig_dtype.T),
        ('beta2', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE,
         sig_dtype.T),
        ('epsilon', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE,
         sig_dtype.T),
        ('grad', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('indices', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T1)
    )

    @prim_attr_register
    def __init__(self, use_locking=False, use_nesterov=False):
        validator.check_value_type("use_locking", use_locking, [bool], self.name)
        validator.check_value_type("use_nesterov", use_nesterov, [bool], self.name)
        self.init_prim_io_names(inputs=['var', 'm', 'v', 'beta1_power', 'beta2_power', 'lr', 'beta1', 'beta2',
                                        'epsilon', 'grad', 'indices'],
                                outputs=['var', 'm', 'v'])

    def infer_shape(self, var_shape, m_shape, v_shape, beta1_power_shape, beta2_power_shape, lr_shape,
                    beta1_shape, beta2_shape, epsilon_shape, grad_shape, indices_shape):
        validator.check("var_shape", var_shape, "m_shape", m_shape, Rel.EQ, self.name)
        validator.check("var_shape", var_shape, "v_shape", v_shape, Rel.EQ, self.name)
        validator.check_integer("indices rank", len(indices_shape), 1, Rel.EQ, self.name)
        validator.check('grad_shape[0]', grad_shape[0], 'indices_shape[0]', indices_shape[0], Rel.EQ, self.name)
        if len(var_shape) > 1 and grad_shape != indices_shape + var_shape[1:]:
            raise ValueError(f"For '{self.name}', the shape of updates should be [] or "
                             f"grad_shape = indices_shape + var_shape[1:], but got var_shape: {var_shape}, "
                             f"indices_shape: {indices_shape}, grad_shape: {grad_shape}.")
        return [1], [1], [1]

    def infer_dtype(self, var_dtype, m_dtype, v_dtype, beta1_power_dtype, beta2_power_dtype, lr_dtype,
                    beta1_dtype, beta2_dtype, epsilon_dtype, grad_dtype, indices_dtype):
        args = {"var": var_dtype, "m": m_dtype, "v": v_dtype, "grad": grad_dtype}
        validator.check_tensor_type_same(args, mstype.number_type, self.name)

        args = {"beta1_power": beta1_power_dtype, "beta2_power": beta2_power_dtype, 'lr': lr_dtype,
                "beta1": beta1_dtype, "beta2": beta2_dtype, "epsilon": epsilon_dtype}
        validator.check_scalar_or_tensor_type_same(args, [mstype.float16, mstype.float32], self.name, True)

        validator.check_tensor_type_same({"indices_dtype": indices_dtype}, [mstype.int32], self.name)
        return var_dtype, m_dtype, v_dtype


class FusedSparseFtrl(PrimitiveWithInfer):
    """
    Merge the duplicate value of the gradient and then update relevant entries according to the FTRL-proximal scheme.

    Args:
        lr (float): The learning rate value, must be positive.
        l1 (float): l1 regularization strength, must be greater than or equal to zero.
        l2 (float): l2 regularization strength, must be greater than or equal to zero.
        lr_power (float): Learning rate power controls how the learning rate decreases during training,
            must be less than or equal to zero. Use fixed learning rate if `lr_power` is zero.
        use_locking (bool): Use locks for updating operation if True . Default: False.

    Inputs:
        - **var** (Parameter) - The variable to be updated. The data type must be float32.
        - **accum** (Parameter) - The accum to be updated, must be same type and shape as `var`.
        - **linear** (Parameter) - The linear to be updated, must be same type and shape as `var`.
        - **grad** (Tensor) - A tensor of the same type as `var`, for the gradient.
        - **indices** (Tensor) - A vector of indices into the first dimension of `var` and `accum`. The shape
          of `indices` must be the same as `grad` in first dimension. The type must be int32.

    Outputs:
        Tuple of 3 Tensor, this operator will update the input parameters directly, the outputs are useless.

        - **var** (Tensor) - A Tensor with shape (1,).
        - **accum** (Tensor) - A Tensor with shape (1,).
        - **linear** (Tensor) - A Tensor with shape (1,).

    Examples:
        >>> import mindspore
        >>> import mindspore.nn as nn
        >>> import numpy as np
        >>> from mindspore import Parameter
        >>> from mindspore import Tensor
        >>> from mindspore.ops import operations as P
        >>> class SparseApplyFtrlNet(nn.Cell):
        >>>     def __init__(self):
        >>>         super(SparseApplyFtrlNet, self).__init__()
        >>>         self.sparse_apply_ftrl = P.FusedSparseFtrl(lr=0.01, l1=0.0, l2=0.0, lr_power=-0.5)
        >>>         self.var = Parameter(Tensor(np.random.rand(3, 1, 2).astype(np.float32)), name="var")
        >>>         self.accum = Parameter(Tensor(np.random.rand(3, 1, 2).astype(np.float32)), name="accum")
        >>>         self.linear = Parameter(Tensor(np.random.rand(3, 1, 2).astype(np.float32)), name="linear")
        >>>
        >>>     def construct(self, grad, indices):
        >>>         out = self.sparse_apply_ftrl(self.var, self.accum, self.linear, grad, indices)
        >>>         return out
        >>>
        >>> net = SparseApplyFtrlNet()
        >>> grad = Tensor(np.random.rand(2, 1, 2).astype(np.float32))
        >>> indices = Tensor(np.array([0, 1]).astype(np.int32))
        >>> output = net(grad, indices)
    """
    __mindspore_signature__ = (
        ('var', sig_rw.RW_WRITE, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('accum', sig_rw.RW_WRITE, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('linear', sig_rw.RW_WRITE, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('grad', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('indices', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T1)
    )

    @prim_attr_register
    def __init__(self, lr, l1, l2, lr_power, use_locking=False):
        self.init_prim_io_names(inputs=['var', 'accum', 'linear', 'grad', 'indices'],
                                outputs=['output'])
        validator.check_value_type("lr", lr, [float], self.name)
        validator.check_value_type("l1", l1, [float], self.name)
        validator.check_value_type("l2", l2, [float], self.name)
        validator.check_value_type("lr_power", lr_power, [float], self.name)
        self.lr = validator.check_number_range("lr", lr, 0.0, float("inf"), Rel.INC_NEITHER, self.name)
        self.l1 = validator.check_number_range("l1", l1, 0.0, float("inf"), Rel.INC_LEFT, self.name)
        self.l2 = validator.check_number_range("l2", l2, 0.0, float("inf"), Rel.INC_LEFT, self.name)
        self.lr_power = validator.check_number("lr_power", lr_power, 0, Rel.LE, self.name)
        self.use_locking = validator.check_value_type("use_locking", use_locking, [bool], self.name)

    def infer_shape(self, var_shape, accum_shape, linear_shape, grad_shape, indices_shape):
        validator.check('var shape', var_shape, 'accum shape', accum_shape, Rel.EQ, self.name)
        validator.check('var shape', var_shape, 'linear shape', linear_shape, Rel.EQ, self.name)
        if len(var_shape) > 1:
            validator.check('var_shape[1:]', var_shape[1:], 'grad_shape[1:]', grad_shape[1:], Rel.EQ, self.name)
        validator.check_integer("indices rank", len(indices_shape), 1, Rel.EQ, self.name)
        validator.check('grad_shape[0]', grad_shape[0], 'indices_shape[0]', indices_shape[0], Rel.EQ, self.name)
        return [1], [1], [1]

    def infer_dtype(self, var_dtype, accum_dtype, linear_dtype, grad_dtype, indices_dtype):
        args = {"var_dtype": var_dtype, "accum_dtype": accum_dtype,
                "linear_dtype": linear_dtype, "grad_dtype": grad_dtype}
        validator.check_tensor_type_same(args, [mstype.float32], self.name)
        validator.check_tensor_type_same({"indices_dtype": indices_dtype}, [mstype.int32], self.name)
        return var_dtype, accum_dtype, linear_dtype


class FusedSparseProximalAdagrad(PrimitiveWithInfer):
    r"""
    Merge the duplicate value of the gradient and then Updates relevant entries according to the proximal adagrad
    algorithm.

    .. math::
            accum += grad * grad
    .. math::
            \text{prox_v} = var - lr * grad * \frac{1}{\sqrt{accum}}
    .. math::
            var = \frac{sign(\text{prox_v})}{1 + lr * l2} * \max(\left| \text{prox_v} \right| - lr * l1, 0)

    Args:
        use_locking (bool): If true, updates of the var and accum tensors will be protected. Default: False.

    Inputs:
        - **var** (Parameter) - Variable tensor to be updated. The data type must be float32.
        - **accum** (Parameter) - Variable tensor to be updated. Has the same dtype as `var`.
        - **lr** (Tensor) - The learning rate value. The data type must be float32.
        - **l1** (Tensor) - l1 regularization strength. The data type must be float32.
        - **l2** (Tensor) - l2 regularization strength. The data type must be float32.
        - **grad** (Tensor) - A tensor of the same type as `var`, for the gradient. The data type must be float32.
        - **indices** (Tensor) - A vector of indices into the first dimension of `var` and `accum`. The data type
          must be int32.

    Outputs:
        Tuple of 2 Tensor, this operator will update the input parameters directly, the outputs are useless.

        - **var** (Tensor) - A Tensor with shape (1,).
        - **accum** (Tensor) - A Tensor with shape (1,).

    Examples:
        >>> import numpy as np
        >>> import mindspore.nn as nn
        >>> from mindspore import Tensor, Parameter
        >>> from mindspore.ops import operations as P
        >>> class Net(nn.Cell):
        >>>     def __init__(self):
        >>>         super(Net, self).__init__()
        >>>         self.sparse_apply_proximal_adagrad = P.FusedSparseProximalAdagrad()
        >>>         self.var = Parameter(Tensor(np.random.rand(3, 1, 2).astype(np.float32)), name="var")
        >>>         self.accum = Parameter(Tensor(np.random.rand(3, 1, 2).astype(np.float32)), name="accum")
        >>>         self.lr = Tensor(0.01, mstype.float32)
        >>>         self.l1 = Tensor(0.0, mstype.float32)
        >>>         self.l2 = Tensor(0.0, mstype.float32)
        >>>     def construct(self, grad, indices):
        >>>         out = self.sparse_apply_proximal_adagrad(self.var, self.accum, self.lr, self.l1,
        >>>                                                  self.l2, grad, indices)
        >>>         return out
        >>> net = Net()
        >>> grad = Tensor(np.random.rand(2, 1, 2).astype(np.float32))
        >>> indices = Tensor(np.array([0, 1]).astype(np.int32))
        >>> output = net(grad, indices)
    """
    __mindspore_signature__ = (
        ('var', sig_rw.RW_WRITE, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('accum', sig_rw.RW_WRITE, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('lr', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('l1', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('l2', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('grad', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('indices', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T1)
    )

    @prim_attr_register
    def __init__(self, use_locking=False):
        self.init_prim_io_names(inputs=['var', 'accum', 'lr', 'l1', 'l2', 'grad', 'indices'],
                                outputs=['output'])
        self.use_locking = validator.check_value_type("use_locking", use_locking, [bool], self.name)

    def infer_shape(self, var_shape, accum_shape, lr_shape, l1_shape, l2_shape, grad_shape, indices_shape):
        validator.check_integer("indices rank", len(indices_shape), 1, Rel.EQ, self.name)
        return [1], [1]

    def infer_dtype(self, var_dtype, accum_dtype, lr_dtype, l1_dtype, l2_dtype, grad_dtype, indices_dtype):
        args = {'var': var_dtype, 'accum': accum_dtype, 'grad': grad_dtype}
        validator.check_tensor_type_same(args, [mstype.float32], self.name)
        validator.check_scalar_or_tensor_type_same({"lr": lr_dtype}, [mstype.float32], self.name)
        validator.check_scalar_or_tensor_type_same({"l1": l1_dtype}, [mstype.float32], self.name)
        validator.check_scalar_or_tensor_type_same({"l2": l2_dtype}, [mstype.float32], self.name)
        valid_types = [mstype.int16, mstype.int32, mstype.int64,
                       mstype.uint16, mstype.uint32, mstype.uint64]
        validator.check_tensor_type_same({'indices': indices_dtype}, valid_types, self.name)
        return var_dtype, accum_dtype


class KLDivLoss(PrimitiveWithInfer):
    r"""
    Computes the Kullback-Leibler divergence between the target and the output.

    Note:
        Sets input as :math:`x`, input label as :math:`y`, output as :math:`\ell(x, y)`.
        Let,

        .. math::
            L = \{l_1,\dots,l_N\}^\top, \quad
            l_n = y_n \cdot (\log y_n - x_n)

        Then,

        .. math::
            \ell(x, y) = \begin{cases}
            L, & \text{if reduction} = \text{'none';}\\
            \operatorname{mean}(L), & \text{if reduction} = \text{'mean';}\\
            \operatorname{sum}(L),  & \text{if reduction} = \text{'sum'.}
            \end{cases}

    Args:
        reduction (str): Specifies the reduction to be applied to the output.
            Its value should be one of 'none', 'mean', 'sum'. Default: 'mean'.

    Inputs:
        - **input_x** (Tensor) - The input Tensor. The data type must be float32.
        - **input_y** (Tensor) - The label Tensor which has same shape as `input_x`. The data type must be float32.

    Outputs:
        Tensor or Scalar, if `reduction` is 'none', then output is a tensor and same shape as `input_x`.
        Otherwise it is a scalar.

    Examples:
        >>> import mindspore
        >>> import mindspore.nn as nn
        >>> import numpy as np
        >>> from mindspore import Tensor
        >>> from mindspore.ops import operations as P
        >>> class Net(nn.Cell):
        >>>     def __init__(self):
        >>>         super(Net, self).__init__()
        >>>         self.kldiv_loss = P.KLDivLoss()
        >>>     def construct(self, x, y):
        >>>         result = self.kldiv_loss(x, y)
        >>>         return result
        >>>
        >>> net = Net()
        >>> input_x = Tensor(np.array([0.2, 0.7, 0.1]), mindspore.float32)
        >>> input_y = Tensor(np.array([0., 1., 0.]), mindspore.float32)
        >>> result = net(input_x, input_y)
    """

    @prim_attr_register
    def __init__(self, reduction='mean'):
        self.reduction = validator.check_string('reduction', reduction, ['none', 'mean', 'sum'], self.name)

    def infer_shape(self, x_shape, y_shape):
        validator.check('x_shape', x_shape, 'y_shape', y_shape, Rel.EQ, self.name)
        if self.reduction in ('mean', 'sum'):
            shape = []
        else:
            shape = x_shape
        return shape

    def infer_dtype(self, x_type, y_type):
        args = {'x': x_type, 'y': y_type}
        valid_types = (mstype.float16, mstype.float32)
        validator.check_tensor_type_same(args, valid_types, self.name)
        return x_type


class BinaryCrossEntropy(PrimitiveWithInfer):
    r"""
    Computes the Binary Cross Entropy between the target and the output.

    Note:
        Sets input as :math:`x`, input label as :math:`y`, output as :math:`\ell(x, y)`.
        Let,

        .. math::
            L = \{l_1,\dots,l_N\}^\top, \quad
            l_n = - w_n \left[ y_n \cdot \log x_n + (1 - y_n) \cdot \log (1 - x_n) \right]

        Then,

        .. math::
            \ell(x, y) = \begin{cases}
            L, & \text{if reduction} = \text{'none';}\\
            \operatorname{mean}(L), & \text{if reduction} = \text{'mean';}\\
            \operatorname{sum}(L),  & \text{if reduction} = \text{'sum'.}
            \end{cases}

    Args:
        reduction (str): Specifies the reduction to be applied to the output.
            Its value should be one of 'none', 'mean', 'sum'. Default: 'mean'.

    Inputs:
        - **input_x** (Tensor) - The input Tensor. The data type should be float16 or float32.
        - **input_y** (Tensor) - The label Tensor which has same shape and data type as `input_x`.
        - **weight** (Tensor, optional) - A rescaling weight applied to the loss of each batch element.
          And it should have same shape and data type as `input_x`. Default: None.

    Outputs:
        Tensor or Scalar, if `reduction` is 'none', then output is a tensor and same shape as `input_x`.
        Otherwise it is a scalar.

    Examples:
        >>> import mindspore
        >>> import mindspore.nn as nn
        >>> import numpy as np
        >>> from mindspore import Tensor
        >>> from mindspore.ops import operations as P
        >>> class Net(nn.Cell):
        >>>     def __init__(self):
        >>>         super(Net, self).__init__()
        >>>         self.binary_cross_entropy = P.BinaryCrossEntropy()
        >>>     def construct(self, x, y, weight):
        >>>         result = self.binary_cross_entropy(x, y, weight)
        >>>         return result
        >>>
        >>> net = Net()
        >>> input_x = Tensor(np.array([0.2, 0.7, 0.1]), mindspore.float32)
        >>> input_y = Tensor(np.array([0., 1., 0.]), mindspore.float32)
        >>> weight = Tensor(np.array([1, 2, 2]), mindspore.float32)
        >>> result = net(input_x, input_y, weight)
        0.38240486
    """

    @prim_attr_register
    def __init__(self, reduction='mean'):
        self.reduction = validator.check_string('reduction', reduction, ['none', 'mean', 'sum'], self.name)

    def infer_shape(self, x_shape, y_shape, weight_shape):
        validator.check('x_shape', x_shape, 'y_shape', y_shape, Rel.EQ, self.name)
        if weight_shape:
            validator.check('y_shape', y_shape, 'weight_shape', weight_shape, Rel.EQ, self.name)
        if self.reduction in ('mean', 'sum'):
            shape = []
        else:
            shape = x_shape
        return shape

    def infer_dtype(self, x_type, y_type, weight_type):
        args = {'x': x_type, 'y': y_type}
        valid_types = (mstype.float16, mstype.float32)
        validator.check_tensor_type_same(args, valid_types, self.name)
        if weight_type:
            validator.check_tensor_type_same({'x': x_type, 'weight': weight_type}, valid_types, self.name)
        return x_type


class ApplyAdaMax(PrimitiveWithInfer):
    r"""
    Update relevant entries according to the adamax scheme.

    The updating formulas are as follows,

    .. math::
        \begin{array}{ll} \\
            m_{t} = \beta_1 * m_{t-1} + (1 - \beta_1) * g \\
            v_{t} = \max(\beta_2 * v_{t-1}, \left| g \right|) \\
            var = var - \frac{l}{1 - \beta_1^t} * \frac{m_{t}}{v_{t} + \epsilon}
        \end{array}

    :math:`t` represents updating step while, :math:`m` represents the 1st moment vector, :math:`m_{t-1}`
    is the last momentent of :math:`m_{t}`, :math:`v` represents the 2nd moment vector, :math:`v_{t-1}`
    is the last momentent of :math:`v_{t}`, :math:`l` represents scaling factor `lr`,
    :math:`g` represents `grad`, :math:`\beta_1, \beta_2` represent `beta1` and `beta2`,
    :math:`beta_1^t` represent `beta1_power`, :math:`var` represents Variable to be updated,
    :math:`\epsilon` represents `epsilon`.

    Inputs:
        - **var** (Parameter) - Variable to be updated. With float32 or float16 data type.
        - **m** (Parameter) - The 1st moment vector in the updating formula. Has the same shape and type as `var`.
          With float32 or float16 data type.
        - **v** (Parameter) - The 2nd moment vector in the updating formula. Mean square gradients,
          has the same shape and type as `var`. With float32 or float16 data type.
        - **beta1_power** (Union[Number, Tensor]) - :math:`beta_1^t` in the updating formula, should be scalar.
          With float32 or float16 data type.
        - **lr** (Union[Number, Tensor]) - Learning rate, :math:`l` in the updating formula, should be scalar.
          With float32 or float16 data type.
        - **beta1** (Union[Number, Tensor]) - The exponential decay rate for the 1st moment estimations,
          should be scalar. With float32 or float16 data type.
        - **beta2** (Union[Number, Tensor]) - The exponential decay rate for the 2nd moment estimations,
          should be scalar. With float32 or float16 data type.
        - **epsilon** (Union[Number, Tensor]) - A small value added for numerical stability, should be scalar.
          With float32 or float16 data type.
        - **grad** (Tensor) - A tensor for gradient. Has the same shape and type as `var`.
          With float32 or float16 data type.

    Outputs:
        Tuple of 3 Tensor, the updated parameters.

        - **var** (Tensor) - The same shape and data type as `var`.
        - **m** (Tensor) - The same shape and data type as `m`.
        - **v** (Tensor) - The same shape and data type as `v`.

    Examples:
        >>> import numpy as np
        >>> import mindspore.nn as nn
        >>> from mindspore import Tensor, Parameter
        >>> from mindspore.ops import operations as P
        >>> import mindspore.common.dtype as mstype
        >>> class Net(nn.Cell):
        >>>     def __init__(self):
        >>>         super(Net, self).__init__()
        >>>         self.apply_ada_max = P.ApplyAdaMax()
        >>>         self.var = Parameter(Tensor(np.random.rand(3, 3).astype(np.float32)), name="var")
        >>>         self.m = Parameter(Tensor(np.random.rand(3, 3).astype(np.float32)), name="m")
        >>>         self.v = Parameter(Tensor(np.random.rand(3, 3).astype(np.float32)), name="v")
        >>>     def construct(self, beta1_power, lr, beta1, beta2, epsilon, grad):
        >>>         out = self.apply_ada_max(self.var, self.m, self.v, beta1_power, lr, beta1, beta2, epsilon, grad)
        >>>         return out
        >>> net = Net()
        >>> beta1_power =Tensor(0.9, mstype.float32)
        >>> lr = Tensor(0.001, mstype.float32)
        >>> beta1 = Tensor(0.9, mstype.float32)
        >>> beta2 = Tensor(0.99, mstype.float32)
        >>> epsilon = Tensor(1e-10, mstype.float32)
        >>> grad = Tensor(np.random.rand(3, 3).astype(np.float32))
        >>> result = net(beta1_power, lr, beta1, beta2, epsilon, grad)
    """

    __mindspore_signature__ = (
        ('var', sig_rw.RW_WRITE, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('m', sig_rw.RW_WRITE, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('v', sig_rw.RW_WRITE, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('beta1_power', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE,
         sig_dtype.T1),
        ('lr', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T2),
        ('beta1', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T3),
        ('beta2', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T4),
        ('epsilon', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T5),
        ('grad', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T)
    )

    @prim_attr_register
    def __init__(self):
        """init ApplyAdaMax"""

    def infer_shape(self, var_shape, m_shape, v_shape, beta1_power_shape, lr_shape,
                    beta1_shape, beta2_shape, epsilon_shape, grad_shape):
        validator.check("m_shape", m_shape, "var_shape", var_shape, Rel.EQ, self.name)
        validator.check("v_shape", v_shape, "var_shape", var_shape, Rel.EQ, self.name)
        validator.check("grad_shape", grad_shape, "var_shape", var_shape, Rel.EQ, self.name)
        beta1_power_shp_len = len(beta1_power_shape)
        validator.check_integer("beta1 power's rank", beta1_power_shp_len, 1, Rel.LE, self.name)
        if beta1_power_shp_len == 1:
            validator.check_integer("beta1_power_shape[0]", beta1_power_shape[0], 1, Rel.EQ, self.name)
        lr_shp_len = len(lr_shape)
        validator.check_integer("lr's rank", lr_shp_len, 1, Rel.LE, self.name)
        if lr_shp_len == 1:
            validator.check_integer("lr_shape[0]", lr_shape[0], 1, Rel.EQ, self.name)
        beta1_shp_len = len(beta1_shape)
        validator.check_integer("beta1's rank", beta1_shp_len, 1, Rel.LE, self.name)
        if beta1_shp_len == 1:
            validator.check_integer("beta1_shape[0]", beta1_shape[0], 1, Rel.EQ, self.name)
        beta2_shp_len = len(beta2_shape)
        validator.check_integer("beta2's rank", beta2_shp_len, 1, Rel.LE, self.name)
        if beta2_shp_len == 1:
            validator.check_integer("beta2_shape[0]", beta2_shape[0], 1, Rel.EQ, self.name)
        epsilon_shp_len = len(epsilon_shape)
        validator.check_integer("epsilon's rank", epsilon_shp_len, 1, Rel.LE, self.name)
        if epsilon_shp_len == 1:
            validator.check_integer("epsilon_shape[0]", epsilon_shape[0], 1, Rel.EQ, self.name)
        return var_shape, m_shape, v_shape

    def infer_dtype(self, var_dtype, m_dtype, v_dtype, beta1_power_dtype, lr_dtype,
                    beta1_dtype, beta2_dtype, epsilon_dtype, grad_dtype):
        valid_types = [mstype.float16, mstype.float32]
        args = {"var": var_dtype, "m": m_dtype, "v": v_dtype, "grad": grad_dtype}
        validator.check_tensor_type_same(args, valid_types, self.name)
        validator.check_scalar_or_tensor_type_same({"beta1_power": beta1_power_dtype}, valid_types, self.name)
        validator.check_scalar_or_tensor_type_same({"lr": lr_dtype}, valid_types, self.name)
        validator.check_scalar_or_tensor_type_same({"beta1": beta1_dtype}, valid_types, self.name)
        validator.check_scalar_or_tensor_type_same({"beta2": beta2_dtype}, valid_types, self.name)
        validator.check_scalar_or_tensor_type_same({"epsilon": epsilon_dtype}, valid_types, self.name)
        return var_dtype, m_dtype, v_dtype


class ApplyAdadelta(PrimitiveWithInfer):
    r"""
    Update relevant entries according to the adadelta scheme.

    .. math::
            accum = \rho * accum + (1 - \rho) * grad^2
    .. math::
            \text{update} = \sqrt{\text{accum_update} + \epsilon} * \frac{grad}{\sqrt{accum + \epsilon}}
    .. math::
            \text{accum_update} = \rho * \text{accum_update} + (1 - \rho) * update^2
    .. math::
            var -= lr * update

    Inputs:
        - **var** (Parameter) - Weights to be updated. With float32 or float16 data type.
        - **accum** (Parameter) - Accum to be updated, has the same shape and type as `var`.
          With float32 or float16 data type.
        - **accum_update** (Parameter) - Accum_update to be updated, has the same shape and type as `var`.
          With float32 or float16 data type.
        - **lr** (Union[Number, Tensor]) - Learning rate, must be scalar. With float32 or float16 data type.
        - **rho** (Union[Number, Tensor]) - Decay rate, must be scalar. With float32 or float16 data type.
        - **epsilon** (Union[Number, Tensor]) - A small value added for numerical stability, must be scalar.
          With float32 or float16 data type.
        - **grad** (Tensor) - Gradients, has the same shape and type as `var`. With float32 or float16 data type.

    Outputs:
        Tuple of 3 Tensor, the updated parameters.

        - **var** (Tensor) - The same shape and data type as `var`.
        - **accum** (Tensor) - The same shape and data type as `accum`.
        - **accum_update** (Tensor) - The same shape and data type as `accum_update`.

    Examples:
        >>> import numpy as np
        >>> import mindspore.nn as nn
        >>> from mindspore import Tensor, Parameter
        >>> from mindspore.ops import operations as P
        >>> import mindspore.common.dtype as mstype
        >>> class Net(nn.Cell):
        >>>     def __init__(self):
        >>>         super(Net, self).__init__()
        >>>         self.apply_adadelta = P.ApplyAdadelta()
        >>>         self.var = Parameter(Tensor(np.random.rand(3, 3).astype(np.float32)), name="var")
        >>>         self.accum = Parameter(Tensor(np.random.rand(3, 3).astype(np.float32)), name="accum")
        >>>         self.accum_update = Parameter(Tensor(np.random.rand(3, 3).astype(np.float32)), name="accum_update")
        >>>     def construct(self, lr, rho, epsilon, grad):
        >>>         out = self.apply_adadelta(self.var, self.accum, self.accum_update, lr, rho, epsilon, grad)
        >>>         return out
        >>> net = Net()
        >>> lr = Tensor(0.001, mstype.float32)
        >>> rho = Tensor(0.0, mstype.float32)
        >>> epsilon = Tensor(1e-6, mstype.float32)
        >>> grad = Tensor(np.random.rand(3, 3).astype(np.float32))
        >>> result = net(lr, rho, epsilon, grad)
    """

    __mindspore_signature__ = (
        ('var', sig_rw.RW_WRITE, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('accum', sig_rw.RW_WRITE, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('accum_update', sig_rw.RW_WRITE, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE,
         sig_dtype.T),
        ('lr', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T1),
        ('rho', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T2),
        ('epsilon', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T3),
        ('grad', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T)
    )

    @prim_attr_register
    def __init__(self):
        """init ApplyAdadelta"""

    def infer_shape(self, var_shape, accum_shape, accum_update_shape, lr_shape, rho_shape,
                    epsilon_shape, grad_shape):
        validator.check("accum_shape", accum_shape, "var_shape", var_shape, Rel.EQ, self.name)
        validator.check("accum_update_shape", accum_update_shape, "var_shape", var_shape, Rel.EQ, self.name)
        validator.check("grad_shape", grad_shape, "var_shape", var_shape, Rel.EQ, self.name)
        lr_shp_len = len(lr_shape)
        validator.check_integer("lr's rank", lr_shp_len, 1, Rel.LE, self.name)
        if lr_shp_len == 1:
            validator.check_integer("lr_shape[0]", lr_shape[0], 1, Rel.EQ, self.name)
        rho_shp_len = len(rho_shape)
        validator.check_integer("rho's rank", rho_shp_len, 1, Rel.LE, self.name)
        if rho_shp_len == 1:
            validator.check_integer("rho_shape[0]", rho_shape[0], 1, Rel.EQ, self.name)
        epsilon_shp_len = len(epsilon_shape)
        validator.check_integer("lepsilon's rank", epsilon_shp_len, 1, Rel.LE, self.name)
        if epsilon_shp_len == 1:
            validator.check_integer("epsilon_shape[0]", epsilon_shape[0], 1, Rel.EQ, self.name)
        return var_shape, accum_shape, accum_update_shape

    def infer_dtype(self, var_dtype, accum_dtype, accum_update_dtype, lr_dtype, rho_dtype,
                    epsilon_dtype, grad_dtype):
        valid_types = [mstype.float16, mstype.float32]
        args = {"var": var_dtype, "accum": accum_dtype, "accum_update": accum_update_dtype, "grad": grad_dtype}
        validator.check_tensor_type_same(args, valid_types, self.name)
        validator.check_scalar_or_tensor_type_same({"lr": lr_dtype}, valid_types, self.name)
        validator.check_scalar_or_tensor_type_same({"rho": rho_dtype}, valid_types, self.name)
        validator.check_scalar_or_tensor_type_same({"epsilon": epsilon_dtype}, valid_types, self.name)
        return var_dtype, accum_dtype, accum_update_dtype


class ApplyAdagrad(PrimitiveWithInfer):
    r"""
    Update relevant entries according to the adagrad scheme.

    .. math::
            accum += grad * grad
    .. math::
            var -= lr * grad * \frac{1}{\sqrt{accum}}

    Args:
        update_slots (bool): If `True`, `accum` will be updated. Default: True.

    Inputs:
        - **var** (Parameter) - Variable to be updated. With float32 or float16 data type.
        - **accum** (Parameter) - Accum to be updated. The shape and dtype should be the same as `var`.
          With float32 or float16 data type.
        - **lr** (Union[Number, Tensor]) - The learning rate value, should be scalar. With float32 or float16 data type.
        - **grad** (Tensor) - A tensor for gradient. The shape and dtype should be the same as `var`.
          With float32 or float16 data type.

    Outputs:
        Tuple of 2 Tensor, the updated parameters.

        - **var** (Tensor) - The same shape and data type as `var`.
        - **accum** (Tensor) - The same shape and data type as `accum`.

    Examples:
        >>> import numpy as np
        >>> import mindspore.nn as nn
        >>> from mindspore import Tensor, Parameter
        >>> from mindspore.ops import operations as P
        >>> import mindspore.common.dtype as mstype
        >>> class Net(nn.Cell):
        >>>     def __init__(self):
        >>>         super(Net, self).__init__()
        >>>         self.apply_adagrad = P.ApplyAdagrad()
        >>>         self.var = Parameter(Tensor(np.random.rand(3, 3).astype(np.float32)), name="var")
        >>>         self.accum = Parameter(Tensor(np.random.rand(3, 3).astype(np.float32)), name="accum")
        >>>     def construct(self, lr, grad):
        >>>         out = self.apply_adagrad(self.var, self.accum, lr, grad)
        >>>         return out
        >>> net = Net()
        >>> lr = Tensor(0.001, mstype.float32)
        >>> grad = Tensor(np.random.rand(3, 3).astype(np.float32))
        >>> result = net(lr, grad)
    """

    __mindspore_signature__ = (
        ('var', sig_rw.RW_WRITE, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('accum', sig_rw.RW_WRITE, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('lr', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T1),
        ('grad', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T)
    )

    @prim_attr_register
    def __init__(self, update_slots=True):
        validator.check_value_type("update_slots", update_slots, [bool], self.name)

    def infer_shape(self, var_shape, accum_shape, lr_shape, grad_shape):
        validator.check('accum shape', accum_shape, 'var shape', var_shape, Rel.EQ, self.name)
        validator.check('grad shape', grad_shape, 'var shape', var_shape, Rel.EQ, self.name)
        lr_shp_len = len(lr_shape)
        validator.check_integer("lr's rank", lr_shp_len, 1, Rel.LE, self.name)
        if lr_shp_len == 1:
            validator.check_integer("lr_shape[0]", lr_shape[0], 1, Rel.EQ, self.name)
        return var_shape, accum_shape

    def infer_dtype(self, var_dtype, accum_dtype, lr_dtype, grad_dtype):
        args = {'var': var_dtype, 'accum': accum_dtype, 'grad': grad_dtype}
        valid_types = [mstype.float16, mstype.float32]
        validator.check_tensor_type_same(args, valid_types, self.name)
        validator.check_scalar_or_tensor_type_same({'lr': lr_dtype}, valid_types, self.name)
        return var_dtype, accum_dtype


class ApplyAdagradV2(PrimitiveWithInfer):
    r"""
    Update relevant entries according to the adagradv2 scheme.

    .. math::
            accum += grad * grad
    .. math::
            var -= lr * grad * \frac{1}{\sqrt{accum} + \epsilon}

    Args:
        epsilon (float): A small value added for numerical stability.
        update_slots (bool): If `True`, `accum` will be updated. Default: True.

    Inputs:
        - **var** (Parameter) - Variable to be updated. With float16 or float32 data type.
        - **accum** (Parameter) - Accum to be updated. The shape and dtype should be the same as `var`.
          With float16 or float32 data type.
        - **lr** (Union[Number, Tensor]) - The learning rate value, should be a float number or
          a scalar tensor with float16 or float32 data type.
        - **grad** (Tensor) - A tensor for gradient. The shape and dtype should be the same as `var`.
          With float16 or float32 data type.

    Outputs:
        Tuple of 2 Tensor, the updated parameters.

        - **var** (Tensor) - The same shape and data type as `var`.
        - **accum** (Tensor) - The same shape and data type as `m`.

    Examples:
        >>> import numpy as np
        >>> import mindspore.nn as nn
        >>> from mindspore import Tensor, Parameter
        >>> from mindspore.ops import operations as P
        >>> import mindspore.common.dtype as mstype
        >>> class Net(nn.Cell):
        >>>     def __init__(self):
        >>>         super(Net, self).__init__()
        >>>         self.apply_adagrad_v2 = P.ApplyAdagradV2(epsilon=1e-6)
        >>>         self.var = Parameter(Tensor(np.random.rand(3, 3).astype(np.float32)), name="var")
        >>>         self.accum = Parameter(Tensor(np.random.rand(3, 3).astype(np.float32)), name="accum")
        >>>     def construct(self, lr, grad):
        >>>         out = self.apply_adagrad_v2(self.var, self.accum, lr, grad)
        >>>         return out
        >>> net = Net()
        >>> lr = Tensor(0.001, mstype.float32)
        >>> grad = Tensor(np.random.rand(3, 3).astype(np.float32))
        >>> result = net(lr, grad)
    """

    __mindspore_signature__ = (
        ('var', sig_rw.RW_WRITE, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('accum', sig_rw.RW_WRITE, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('lr', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T1),
        ('grad', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T)
    )

    @prim_attr_register
    def __init__(self, epsilon, update_slots=True):
        validator.check_value_type("epsilon", epsilon, [float], self.name)
        validator.check_value_type("update_slots", update_slots, [bool], self.name)

    def infer_shape(self, var_shape, accum_shape, lr_shape, grad_shape):
        validator.check('var shape', var_shape, 'accum shape', accum_shape, Rel.EQ, self.name)
        validator.check('var shape', var_shape, 'grad shape', grad_shape, Rel.EQ, self.name)
        lr_shp_len = len(lr_shape)
        validator.check_integer("lr's rank", lr_shp_len, 1, Rel.LE, self.name)
        if lr_shp_len == 1:
            validator.check_integer("lr_shape[0]", lr_shape[0], 1, Rel.EQ, self.name)
        return var_shape, accum_shape

    def infer_dtype(self, var_dtype, accum_dtype, lr_dtype, grad_dtype):
        args = {'var': var_dtype, 'accum': accum_dtype, 'grad': grad_dtype}
        validator.check_tensor_type_same(args, [mstype.float16, mstype.float32], self.name)
        validator.check_scalar_or_tensor_type_same({'lr': lr_dtype}, [mstype.float16, mstype.float32], self.name)
        return var_dtype, accum_dtype


class SparseApplyAdagrad(PrimitiveWithInfer):
    r"""
    Update relevant entries according to the adagrad scheme.

    .. math::
            accum += grad * grad
    .. math::
            var -= lr * grad * (1 / sqrt(accum))

    Args:
        lr (float): Learning rate.
        update_slots (bool): If `True`, `accum` will be updated. Default: True.
        use_locking (bool): If true, updates of the var and accum tensors will be protected. Default: False.

    Inputs:
        - **var** (Parameter) - Variable to be updated. The data type must be float16 or float32.
        - **accum** (Parameter) - Accum to be updated. The shape and dtype should be the same as `var`.
        - **grad** (Tensor) - Gradient. The shape must be the same as `var`'s shape except first dimension.
          Has the same data type as `var`.
        - **indices** (Tensor) - A vector of indices into the first dimension of `var` and `accum`.
          The shape of `indices` must be the same as `grad` in first dimension, the type must be int32.

    Outputs:
        Tuple of 2 Tensor, the updated parameters.

        - **var** (Tensor) - The same shape and data type as `var`.
        - **accum** (Tensor) - The same shape and data type as `accum`.

    Examples:
        >>> import numpy as np
        >>> import mindspore.nn as nn
        >>> from mindspore import Tensor, Parameter
        >>> from mindspore.ops import operations as P
        >>> import mindspore.common.dtype as mstype
        >>> class Net(nn.Cell):
        >>>     def __init__(self):
        >>>         super(Net, self).__init__()
        >>>         self.sparse_apply_adagrad = P.SparseApplyAdagrad(lr=1e-8)
        >>>         self.var = Parameter(Tensor(np.ones([3, 3, 3]).astype(np.float32)), name="var")
        >>>         self.accum = Parameter(Tensor(np.ones([3, 3, 3]).astype(np.float32)), name="accum")
        >>>     def construct(self, grad, indices):
        >>>         out = self.sparse_apply_adagrad(self.var, self.accum, grad, indices)
        >>>         return out
        >>> net = Net()
        >>> grad = Tensor(np.random.rand(3, 3, 3).astype(np.float32))
        >>> indices = Tensor([0, 1, 2], mstype.int32)
        >>> result = net(grad, indices)
    """

    __mindspore_signature__ = (
        ('var', sig_rw.RW_WRITE, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('accum', sig_rw.RW_WRITE, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('grad', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('indices', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T1)
    )

    @prim_attr_register
    def __init__(self, lr, update_slots=True, use_locking=False):
        validator.check_value_type("lr", lr, [float], self.name)
        validator.check_number_range("lr", lr, float("-inf"), float("inf"), Rel.INC_NEITHER, self.name)
        validator.check_value_type("update_slots", update_slots, [bool], self.name)
        validator.check_value_type("use_locking", use_locking, [bool], self.name)

    def infer_shape(self, var_shape, accum_shape, grad_shape, indices_shape):
        validator.check('var shape', var_shape, 'accum shape', accum_shape, Rel.EQ, self.name)
        validator.check('len of var shape', len(var_shape), 'len of grad shape', len(grad_shape), Rel.EQ, self.name)
        if len(var_shape) > 1:
            validator.check('var_shape[1:]', var_shape[1:], 'grad_shape[1:]', grad_shape[1:], Rel.EQ, self.name)
        validator.check_integer("indices rank", len(indices_shape), 1, Rel.EQ, self.name)
        validator.check('grad_shape[0]', grad_shape[0], 'indices_shape[0]', indices_shape[0], Rel.EQ, self.name)
        return var_shape, accum_shape

    def infer_dtype(self, var_type, accum_type, grad_type, indices_type):
        args = {'var': var_type, 'accum': accum_type, 'grad': grad_type}
        validator.check_tensor_type_same(args, [mstype.float16, mstype.float32], self.name)
        validator.check_tensor_type_same({'indices': indices_type}, [mstype.int32], self.name)
        return var_type, accum_type


class SparseApplyAdagradV2(PrimitiveWithInfer):
    r"""
    Update relevant entries according to the adagrad scheme.

    .. math::
            accum += grad * grad
    .. math::
            var -= lr * grad * \frac{1}{\sqrt{accum} + \epsilon}

    Args:
        lr (float): Learning rate.
        epsilon (float): A small value added for numerical stability.
        use_locking (bool): If `True`, updating of the var and accum tensors will be protected. Default: False.
        update_slots (bool): If `True`, the computation logic will be different to `False`. Default: True.

    Inputs:
        - **var** (Parameter) - Variable to be updated. The data type must be float16 or float32.
        - **accum** (Parameter) - Accum to be updated. The shape and dtype should be the same as `var`.
        - **grad** (Tensor) - Gradient. The shape must be the same as `var`'s shape except first dimension.
          Has the same data type as `var`.
        - **indices** (Tensor) - A vector of indices into the first dimension of `var` and `accum`.
          The shape of `indices` must be the same as `grad` in first dimension, the type must be int32.

    Outputs:
        Tuple of 2 Tensor, the updated parameters.

        - **var** (Tensor) - The same shape and data type as `var`.
        - **accum** (Tensor) - The same shape and data type as `accum`.

    Examples:
        >>> import numpy as np
        >>> import mindspore.nn as nn
        >>> from mindspore import Tensor, Parameter
        >>> from mindspore.ops import operations as P
        >>> import mindspore.common.dtype as mstype
        >>> class Net(nn.Cell):
        >>>     def __init__(self):
        >>>         super(Net, self).__init__()
        >>>         self.sparse_apply_adagrad_v2 = P.SparseApplyAdagradV2(lr=1e-8, epsilon=1e-6)
        >>>         self.var = Parameter(Tensor(np.ones([3, 3, 3]).astype(np.float32)), name="var")
        >>>         self.accum = Parameter(Tensor(np.ones([3, 3, 3]).astype(np.float32)), name="accum")
        >>>
        >>>     def construct(self, grad, indices):
        >>>         out = self.sparse_apply_adagrad_v2(self.var, self.accum, grad, indices)
        >>>         return out
        >>> net = Net()
        >>> grad = Tensor(np.random.rand(3, 3, 3).astype(np.float32))
        >>> indices = Tensor([0, 1, 2], mstype.int32)
        >>> result = net(grad, indices)
    """

    __mindspore_signature__ = (
        ('var', sig_rw.RW_WRITE, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('accum', sig_rw.RW_WRITE, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('grad', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('indices', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T1)
    )

    @prim_attr_register
    def __init__(self, lr, epsilon, use_locking=False, update_slots=True):
        self.lr = validator.check_value_type("lr", lr, [float], self.name)
        self.epsilon = validator.check_value_type("epsilon", epsilon, [float], self.name)
        self.use_locking = validator.check_value_type("update_slots", update_slots, [bool], self.name)
        self.update_slots = validator.check_value_type("use_locking", use_locking, [bool], self.name)

    def infer_shape(self, var_shape, accum_shape, grad_shape, indices_shape):
        validator.check('var shape', var_shape, 'accum shape', accum_shape, Rel.EQ, self.name)
        validator.check('len of var shape', len(var_shape), 'len of grad shape', len(grad_shape), Rel.EQ, self.name)
        if len(var_shape) > 1:
            validator.check('var_shape[1:]', var_shape[1:], 'grad_shape[1:]', grad_shape[1:], Rel.EQ, self.name)
        validator.check_integer("indices rank", len(indices_shape), 1, Rel.EQ, self.name)
        validator.check('grad_shape[0]', grad_shape[0], 'indices_shape[0]', indices_shape[0], Rel.EQ, self.name)
        return var_shape, accum_shape

    def infer_dtype(self, var_type, accum_type, grad_type, indices_type):
        args = {'var': var_type, 'accum': accum_type, 'grad': grad_type}
        validator.check_tensor_type_same(args, [mstype.float16, mstype.float32], self.name)
        validator.check_tensor_type_same({'indices': indices_type}, [mstype.int32], self.name)
        return var_type, accum_type


class ApplyProximalAdagrad(PrimitiveWithInfer):
    r"""
    Update relevant entries according to the proximal adagrad algorithm.

    .. math::
            accum += grad * grad
    .. math::
            \text{prox_v} = var - lr * grad * \frac{1}{\sqrt{accum}}
    .. math::
            var = \frac{sign(\text{prox_v})}{1 + lr * l2} * \max(\left| \text{prox_v} \right| - lr * l1, 0)

    Args:
        use_locking (bool): If true, updates of the var and accum tensors will be protected. Default: False.

    Inputs:
        - **var** (Parameter) - Variable to be updated. The data type should be float16 or float32.
        - **accum** (Parameter) - Accum to be updated. Must has the same shape and dtype as `var`.
        - **lr** (Union[Number, Tensor]) - The learning rate value, should be scalar. The data type should be
          float16 or float32.
        - **l1** (Union[Number, Tensor]) - l1 regularization strength, should be scalar. The data type should be
          float16 or float32.
        - **l2** (Union[Number, Tensor]) - l2 regularization strength, should be scalar. The data type should be
          float16 or float32.
        - **grad** (Tensor) - Gradient. Must has the same shape and dtype as `var`.

    Outputs:
        Tuple of 2 Tensor, the updated parameters.

        - **var** (Tensor) - The same shape and data type as `var`.
        - **accum** (Tensor) - The same shape and data type as `accum`.

    Examples:
        >>> import numpy as np
        >>> import mindspore.nn as nn
        >>> from mindspore import Tensor, Parameter
        >>> from mindspore.ops import operations as P
        >>> class Net(nn.Cell):
        >>>     def __init__(self):
        >>>         super(Net, self).__init__()
        >>>         self.apply_proximal_adagrad = P.ApplyProximalAdagrad()
        >>>         self.var = Parameter(Tensor(np.random.rand(3, 3).astype(np.float32)), name="var")
        >>>         self.accum = Parameter(Tensor(np.random.rand(3, 3).astype(np.float32)), name="accum")
        >>>         self.lr = 0.01
        >>>         self.l1 = 0.0
        >>>         self.l2 = 0.0
        >>>     def construct(self, grad):
        >>>         out = self.apply_proximal_adagrad(self.var, self.accum, self.lr, self.l1, self.l2, grad)
        >>>         return out
        >>> net = Net()
        >>> grad = Tensor(np.random.rand(3, 3).astype(np.float32))
        >>> output = net(grad)
    """

    __mindspore_signature__ = (
        ('var', sig_rw.RW_WRITE, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('accum', sig_rw.RW_WRITE, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('lr', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T1),
        ('l1', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T2),
        ('l2', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T3),
        ('grad', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T)
    )

    @prim_attr_register
    def __init__(self, use_locking=False):
        self.init_prim_io_names(inputs=['var', 'accum', 'lr', 'l1', 'l2', 'grad'],
                                outputs=['var', 'accum'])
        self.use_locking = validator.check_value_type("use_locking", use_locking, [bool], self.name)

    def infer_shape(self, var_shape, accum_shape, lr_shape, l1_shape, l2_shape, grad_shape):
        validator.check('accum shape', accum_shape, 'var shape', var_shape, Rel.EQ, self.name)
        validator.check('grad shape', grad_shape, 'var shape', var_shape, Rel.EQ, self.name)
        lr_shp_len = len(lr_shape)
        validator.check_integer("lr's rank", lr_shp_len, 1, Rel.LE, self.name)
        if lr_shp_len == 1:
            validator.check_integer("lr_shape[0]", lr_shape[0], 1, Rel.EQ, self.name)
        l1_shp_len = len(l1_shape)
        validator.check_integer("l1's rank", l1_shp_len, 1, Rel.LE, self.name)
        if l1_shp_len == 1:
            validator.check_integer("l1_shape[0]", l1_shape[0], 1, Rel.EQ, self.name)
        l2_shp_len = len(l2_shape)
        validator.check_integer("l2's rank", l2_shp_len, 1, Rel.LE, self.name)
        if l2_shp_len == 1:
            validator.check_integer("l2_shape[0]", l2_shape[0], 1, Rel.EQ, self.name)
        return var_shape, accum_shape

    def infer_dtype(self, var_dtype, accum_dtype, lr_dtype, l1_dtype, l2_dtype, grad_dtype):
        valid_types = [mstype.float16, mstype.float32]
        args = {'var': var_dtype, 'accum': accum_dtype, 'grad': grad_dtype}
        validator.check_tensor_type_same(args, valid_types, self.name)
        validator.check_scalar_or_tensor_type_same({"lr": lr_dtype}, valid_types, self.name)
        validator.check_scalar_or_tensor_type_same({"l1": l1_dtype}, valid_types, self.name)
        validator.check_scalar_or_tensor_type_same({"l2": l2_dtype}, valid_types, self.name)
        return var_dtype, accum_dtype


class SparseApplyProximalAdagrad(PrimitiveWithInfer):
    r"""
    Update relevant entries according to the proximal adagrad algorithm. Compared with ApplyProximalAdagrad,
    an additional index tensor is input.

    .. math::
            accum += grad * grad
    .. math::
            \text{prox_v} = var - lr * grad * \frac{1}{\sqrt{accum}}
    .. math::
            var = \frac{sign(\text{prox_v})}{1 + lr * l2} * \max(\left| \text{prox_v} \right| - lr * l1, 0)

    Args:
        use_locking (bool): If true, updates of the var and accum tensors will be protected. Default: False.

    Inputs:
        - **var** (Parameter) - Variable tensor to be updated. The data type must be float16 or float32.
        - **accum** (Parameter) - Variable tensor to be updated. Has the same dtype as `var`.
        - **lr** (Union[Number, Tensor]) - The learning rate value. Tshould be a float number or
          a scalar tensor with float16 or float32 data type.
        - **l1** (Union[Number, Tensor]) - l1 regularization strength. should be a float number or
          a scalar tensor with float16 or float32 data type.
        - **l2** (Union[Number, Tensor]) - l2 regularization strength. should be a float number or
          a scalar tensor with float16 or float32 data type..
        - **grad** (Tensor) - A tensor of the same type as `var`, for the gradient.
          The data type must be float16 or float32.
        - **indices** (Tensor) - A vector of indices into the first dimension of `var` and `accum`.

    Outputs:
        Tuple of 2 Tensor, the updated parameters.

        - **var** (Tensor) - The same shape and data type as `var`.
        - **accum** (Tensor) - The same shape and data type as `accum`.

    Examples:
        >>> import numpy as np
        >>> import mindspore.nn as nn
        >>> from mindspore import Tensor, Parameter
        >>> from mindspore.ops import operations as P
        >>> class Net(nn.Cell):
        >>>     def __init__(self):
        >>>         super(Net, self).__init__()
        >>>         self.sparse_apply_proximal_adagrad = P.SparseApplyProximalAdagrad()
        >>>         self.var = Parameter(Tensor(np.random.rand(3, 3).astype(np.float32)), name="var")
        >>>         self.accum = Parameter(Tensor(np.random.rand(3, 3).astype(np.float32)), name="accum")
        >>>         self.lr = 0.01
        >>>         self.l1 = 0.0
        >>>         self.l2 = 0.0
        >>>     def construct(self, grad, indices):
        >>>         out = self.sparse_apply_proximal_adagrad(self.var, self.accum, self.lr, self.l1,
                                                             self.l2, grad, indices)
        >>>         return out
        >>> net = Net()
        >>> grad = Tensor(np.random.rand(3, 3).astype(np.float32))
        >>> indices = Tensor(np.ones((3,), np.int32))
        >>> output = net(grad, indices)
    """

    __mindspore_signature__ = (
        ('var', sig_rw.RW_WRITE, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('accum', sig_rw.RW_WRITE, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('lr', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T1),
        ('l1', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T2),
        ('l2', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T3),
        ('grad', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('indices', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T4)
    )

    @prim_attr_register
    def __init__(self, use_locking=False):
        self.init_prim_io_names(inputs=['var', 'accum', 'lr', 'l1', 'l2', 'grad', 'indices'],
                                outputs=['var', 'accum'])
        self.use_locking = validator.check_value_type("use_locking", use_locking, [bool], self.name)

    def infer_shape(self, var_shape, accum_shape, lr_shape, l1_shape, l2_shape, grad_shape, indices_shape):
        validator.check_integer("indices rank", len(indices_shape), 1, Rel.EQ, self.name)
        return var_shape, accum_shape

    def infer_dtype(self, var_dtype, accum_dtype, lr_dtype, l1_dtype, l2_dtype, grad_dtype, indices_dtype):
        args = {'var': var_dtype, 'accum': accum_dtype, 'grad': grad_dtype}
        validator.check_tensor_type_same(args, [mstype.float16, mstype.float32], self.name)
        validator.check_scalar_or_tensor_type_same({"lr": lr_dtype}, [mstype.float16, mstype.float32], self.name)
        validator.check_scalar_or_tensor_type_same({"l1": l1_dtype}, [mstype.float16, mstype.float32], self.name)
        validator.check_scalar_or_tensor_type_same({"l2": l2_dtype}, [mstype.float16, mstype.float32], self.name)
        valid_types = [mstype.int16, mstype.int32, mstype.int64,
                       mstype.uint16, mstype.uint32, mstype.uint64]
        validator.check_tensor_type_same({'indices': indices_dtype}, valid_types, self.name)
        return var_dtype, accum_dtype


class ApplyAddSign(PrimitiveWithInfer):
    r"""
    Update relevant entries according to the AddSign algorithm.

    .. math::
        \begin{array}{ll} \\
            m_{t} = \beta * m_{t-1} + (1 - \beta) * g \\
            \text{update} = (\alpha + \text{sign_decay} * sign(g) * sign(m)) * g \\
            var = var - lr_{t} * \text{update}
        \end{array}

    :math:`t` represents updating step while, :math:`m` represents the 1st moment vector, :math:`m_{t-1}`
    is the last momentent of :math:`m_{t}`, :math:`lr` represents scaling factor `lr`, :math:`g` represents `grad`.

    Inputs:
        - **var** (Parameter) - Variable tensor to be updated. With float32 or float16 data type.
        - **m** (Parameter) - Variable tensor to be updated. Has the same dtype as `var`.
        - **lr** (Union[Number, Tensor]) - The learning rate value, should be a scalar.
          With float32 or float16 data type.
        - **alpha** (Union[Number, Tensor]) - Should be a scalar. With float32 or float16 data type.
        - **sign_decay** (Union[Number, Tensor]) - Should be a scalar. With float32 or float16 data type.
        - **beta** (Union[Number, Tensor]) - The exponential decay rate, should be a scalar.
          With float32 or float16 data type.
        - **grad** (Tensor) - A tensor of the same type as `var`, for the gradient.

    Outputs:
        Tuple of 2 Tensor, the updated parameters.

        - **var** (Tensor) - The same shape and data type as `var`.
        - **m** (Tensor) - The same shape and data type as `m`.

    Examples:
        >>> import numpy as np
        >>> import mindspore.nn as nn
        >>> from mindspore import Tensor, Parameter
        >>> from mindspore.ops import operations as P
        >>> class Net(nn.Cell):
        >>>     def __init__(self):
        >>>         super(Net, self).__init__()
        >>>         self.apply_add_sign = P.ApplyAddSign()
        >>>         self.var = Parameter(Tensor(np.random.rand(3, 3).astype(np.float32)), name="var")
        >>>         self.m = Parameter(Tensor(np.random.rand(3, 3).astype(np.float32)), name="m")
        >>>         self.lr = 0.001
        >>>         self.alpha = 1.0
        >>>         self.sign_decay = 0.99
        >>>         self.beta = 0.9
        >>>     def construct(self, grad):
        >>>         out = self.apply_add_sign(self.var, self.m, self.lr, self.alpha, self.sign_decay, self.beta, grad)
        >>>         return out
        >>> net = Net()
        >>> grad = Tensor(np.random.rand(3, 3).astype(np.float32))
        >>> output = net(grad)
    """

    __mindspore_signature__ = (
        ('var', sig_rw.RW_WRITE, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('m', sig_rw.RW_WRITE, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('lr', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T1),
        ('alpha', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T2),
        ('sign_decay', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE,
         sig_dtype.T3),
        ('beta', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T4),
        ('grad', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T)
    )

    @prim_attr_register
    def __init__(self):
        "init ApplyAddSign"

    def infer_shape(self, var_shape, m_shape, lr_shape, alpha_shape, sign_decay_shape, beta_shape, grad_shape):
        validator.check('m_shape', m_shape, 'var_shape', var_shape, Rel.EQ, self.name)
        validator.check('grad_shape', grad_shape, 'var_shape', var_shape, Rel.EQ, self.name)
        lr_shape_len = len(lr_shape)
        validator.check_integer("lr's rank", lr_shape_len, 1, Rel.LE, self.name)
        if lr_shape_len == 1:
            validator.check_integer("lr_shape[0]", lr_shape[0], 1, Rel.EQ, self.name)
        alpha_shape_len = len(alpha_shape)
        validator.check_integer("alpha's rank", alpha_shape_len, 1, Rel.LE, self.name)
        if alpha_shape_len == 1:
            validator.check_integer("alpha_shape[0]", alpha_shape[0], 1, Rel.EQ, self.name)
        sign_decay_shape_len = len(sign_decay_shape)
        validator.check_integer("sign_decay's rank", sign_decay_shape_len, 1, Rel.LE, self.name)
        if sign_decay_shape_len == 1:
            validator.check_integer("sign_decay_shape[0]", sign_decay_shape[0], 1, Rel.EQ, self.name)
        beta_shape_len = len(beta_shape)
        validator.check_integer("beta's rank", beta_shape_len, 1, Rel.LE, self.name)
        if beta_shape_len == 1:
            validator.check_integer("beta_shape[0]", beta_shape[0], 1, Rel.EQ, self.name)
        return var_shape, m_shape

    def infer_dtype(self, var_dtype, m_dtype, lr_dtype, alpha_dtype, sign_decay_dtype, beta_dtype, grad_dtype):
        valid_types = [mstype.float16, mstype.float32]
        args = {'var': var_dtype, 'm': m_dtype, 'grad': grad_dtype}
        validator.check_tensor_type_same(args, valid_types, self.name)
        validator.check_scalar_or_tensor_type_same({"lr": lr_dtype}, valid_types, self.name)
        validator.check_scalar_or_tensor_type_same({"alpha": alpha_dtype}, valid_types, self.name)
        validator.check_scalar_or_tensor_type_same({"sign_decay": sign_decay_dtype}, valid_types, self.name)
        validator.check_scalar_or_tensor_type_same({"beta": beta_dtype}, valid_types, self.name)
        return var_dtype, m_dtype


class ApplyPowerSign(PrimitiveWithInfer):
    r"""
    Update relevant entries according to the AddSign algorithm.

    .. math::
        \begin{array}{ll} \\
            m_{t} = \beta * m_{t-1} + (1 - \beta) * g \\
            \text{update} = \exp(\text{logbase} * \text{sign_decay} * sign(g) * sign(m)) * g \\
            var = var - lr_{t} * \text{update}
        \end{array}

    :math:`t` represents updating step while, :math:`m` represents the 1st moment vector, :math:`m_{t-1}`
    is the last momentent of :math:`m_{t}`, :math:`lr` represents scaling factor `lr`, :math:`g` represents `grad`.

    Inputs:
        - **var** (Parameter) - Variable tensor to be updated. With float32 or float16 data type.
          If data type of `var` is float16, all inputs must have the same data type as `var`.
        - **m** (Parameter) - Variable tensor to be updated. Has the same dtype as `var`.
        - **lr** (Union[Number, Tensor]) - The learning rate value, should be a scalar.
          With float32 or float16 data type.
        - **logbase** (Union[Number, Tensor]) - Should be a scalar. With float32 or float16 data type.
        - **sign_decay** (Union[Number, Tensor]) - Should be a scalar. With float32 or float16 data type.
        - **beta** (Union[Number, Tensor]) - The exponential decay rate, should be a scalar.
          With float32 or float16 data type.
        - **grad** (Tensor) - A tensor of the same type as `var`, for the gradient.

    Outputs:
        Tuple of 2 Tensor, the updated parameters.

        - **var** (Tensor) - The same shape and data type as `var`.
        - **m** (Tensor) - The same shape and data type as `m`.

    Examples:
        >>> import numpy as np
        >>> import mindspore.nn as nn
        >>> from mindspore import Tensor, Parameter
        >>> from mindspore.ops import operations as P
        >>> class Net(nn.Cell):
        >>>     def __init__(self):
        >>>         super(Net, self).__init__()
        >>>         self.apply_power_sign = P.ApplyPowerSign()
        >>>         self.var = Parameter(Tensor(np.random.rand(3, 3).astype(np.float32)), name="var")
        >>>         self.m = Parameter(Tensor(np.random.rand(3, 3).astype(np.float32)), name="m")
        >>>         self.lr = 0.001
        >>>         self.logbase = np.e
        >>>         self.sign_decay = 0.99
        >>>         self.beta = 0.9
        >>>     def construct(self, grad):
        >>>         out = self.apply_power_sign(self.var, self.m, self.lr, self.logbase,
                                                self.sign_decay, self.beta, grad)
        >>>         return out
        >>> net = Net()
        >>> grad = Tensor(np.random.rand(3, 3).astype(np.float32))
        >>> output = net(grad)
    """

    __mindspore_signature__ = (
        ('var', sig_rw.RW_WRITE, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('m', sig_rw.RW_WRITE, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('lr', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('logbase', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('sign_decay', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE,
         sig_dtype.T),
        ('beta', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('grad', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T)
    )

    @prim_attr_register
    def __init__(self):
        "init ApplyPowerSign"

    def infer_shape(self, var_shape, m_shape, lr_shape, logbase_shape, sign_decay_shape, beta_shape, grad_shape):
        validator.check('m_shape', m_shape, 'var_shape', var_shape, Rel.EQ, self.name)
        validator.check('grad_shape', grad_shape, 'var_shape', var_shape, Rel.EQ, self.name)
        lr_shape_len = len(lr_shape)
        validator.check_integer("lr's rank", lr_shape_len, 1, Rel.LE, self.name)
        if lr_shape_len == 1:
            validator.check_integer("lr_shape[0]", lr_shape[0], 1, Rel.EQ, self.name)
        logbase_shape_len = len(logbase_shape)
        validator.check_integer("logbase's rank", logbase_shape_len, 1, Rel.LE, self.name)
        if logbase_shape_len == 1:
            validator.check_integer("logbase_shape[0]", logbase_shape[0], 1, Rel.EQ, self.name)
        sign_decay_shape_len = len(sign_decay_shape)
        validator.check_integer("sign_decay's rank", sign_decay_shape_len, 1, Rel.LE, self.name)
        if sign_decay_shape_len == 1:
            validator.check_integer("sign_decay_shape[0]", sign_decay_shape[0], 1, Rel.EQ, self.name)
        beta_shape_len = len(beta_shape)
        validator.check_integer("beta's rank", beta_shape_len, 1, Rel.LE, self.name)
        if beta_shape_len == 1:
            validator.check_integer("beta_shape[0]", beta_shape[0], 1, Rel.EQ, self.name)
        return var_shape, m_shape

    def infer_dtype(self, var_dtype, m_dtype, lr_dtype, logbase_dtype, sign_decay_dtype, beta_dtype, grad_dtype):
        valid_types = [mstype.float16, mstype.float32]
        args = {'var': var_dtype, 'm': m_dtype, 'grad': grad_dtype}
        validator.check_tensor_type_same(args, valid_types, self.name)
        validator.check_scalar_or_tensor_type_same({"lr": lr_dtype}, valid_types, self.name)
        validator.check_scalar_or_tensor_type_same({"logbase": logbase_dtype}, valid_types, self.name)
        validator.check_scalar_or_tensor_type_same({"sign_decay": sign_decay_dtype}, valid_types, self.name)
        validator.check_scalar_or_tensor_type_same({"beta": beta_dtype}, valid_types, self.name)
        return var_dtype, m_dtype


class ApplyGradientDescent(PrimitiveWithInfer):
    r"""
    Update relevant entries according to the following formula.

    .. math::
        var = var - \alpha * \delta

    Inputs:
        - **var** (Parameter) - Variable tensor to be updated. With float32 or float16 data type.
        - **alpha** (Union[Number, Tensor]) - Scaling factor, should be a scalar. With float32 or float16 data type.
        - **delta** (Tensor) - A tensor for the change. Has the same type as `var`.

    Outputs:
        Tensor, representing the updated var.

    Examples:
        >>> import numpy as np
        >>> import mindspore.nn as nn
        >>> from mindspore import Tensor, Parameter
        >>> from mindspore.ops import operations as P
        >>> class Net(nn.Cell):
        >>>     def __init__(self):
        >>>         super(Net, self).__init__()
        >>>         self.apply_gradient_descent = P.ApplyGradientDescent()
        >>>         self.var = Parameter(Tensor(np.random.rand(3, 3).astype(np.float32)), name="var")
        >>>         self.alpha = 0.001
        >>>     def construct(self, delta):
        >>>         out = self.apply_gradient_descent(self.var, self.alpha, delta)
        >>>         return out
        >>> net = Net()
        >>> delta = Tensor(np.random.rand(3, 3).astype(np.float32))
        >>> output = net(delta)
    """

    __mindspore_signature__ = (
        ('var', sig_rw.RW_WRITE, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('alpha', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T1),
        ('delta', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T)
    )

    @prim_attr_register
    def __init__(self):
        "init ApplyGradientDescent"

    def infer_shape(self, var_shape, alpha_shape, delta_shape):
        validator.check('delta shape', delta_shape, 'var shape', var_shape, Rel.EQ, self.name)
        alpha_shape_len = len(alpha_shape)
        validator.check_integer("alpha's rank", alpha_shape_len, 1, Rel.LE, self.name)
        if alpha_shape_len == 1:
            validator.check_integer("alpha_shape[0]", alpha_shape[0], 1, Rel.EQ, self.name)
        return var_shape

    def infer_dtype(self, var_dtype, alpha_dtype, delta_dtype):
        valid_types = [mstype.float16, mstype.float32]
        args = {'var': var_dtype, 'delta': delta_dtype}
        validator.check_tensor_type_same(args, valid_types, self.name)
        validator.check_scalar_or_tensor_type_same({"alpha": alpha_dtype}, valid_types, self.name)
        return var_dtype


class ApplyProximalGradientDescent(PrimitiveWithInfer):
    r"""
    Update relevant entries according to the FOBOS(Forward Backward Splitting) algorithm.

    .. math::
        \text{prox_v} = var - \alpha * \delta
    .. math::
        var = \frac{sign(\text{prox_v})}{1 + \alpha * l2} * \max(\left| \text{prox_v} \right| - alpha * l1, 0)

    Inputs:
        - **var** (Parameter) - Variable tensor to be updated. With float32 or float16 data type.
        - **alpha** (Union[Number, Tensor]) - Saling factor, should be a scalar. With float32 or float16 data type.
        - **l1** (Union[Number, Tensor]) - l1 regularization strength, should be scalar.
          With float32 or float16 data type.
        - **l2** (Union[Number, Tensor]) - l2 regularization strength, should be scalar.
          With float32 or float16 data type.
        - **delta** (Tensor) - A tensor for the change. Has the same type as `var`.

    Outputs:
        Tensor, representing the updated var.

    Examples:
        >>> import numpy as np
        >>> import mindspore.nn as nn
        >>> from mindspore import Tensor, Parameter
        >>> from mindspore.ops import operations as P
        >>> class Net(nn.Cell):
        >>>     def __init__(self):
        >>>         super(Net, self).__init__()
        >>>         self.apply_proximal_gradient_descent = P.ApplyProximalGradientDescent()
        >>>         self.var = Parameter(Tensor(np.random.rand(3, 3).astype(np.float32)), name="var")
        >>>         self.alpha = 0.001
        >>>         self.l1 = 0.0
        >>>         self.l2 = 0.0
        >>>     def construct(self, delta):
        >>>         out = self.apply_proximal_gradient_descent(self.var, self.alpha, self.l1, self.l2, delta)
        >>>         return out
        >>> net = Net()
        >>> delta = Tensor(np.random.rand(3, 3).astype(np.float32))
        >>> output = net(delta)
    """

    __mindspore_signature__ = (
        ('var', sig_rw.RW_WRITE, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('alpha', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T1),
        ('l1', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T2),
        ('l2', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T3),
        ('delta', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T)
    )

    @prim_attr_register
    def __init__(self):
        "init ApplyGradientDescent"

    def infer_shape(self, var_shape, alpha_shape, l1_shape, l2_shape, delta_shape):
        validator.check('delta shape', delta_shape, 'var shape', var_shape, Rel.EQ, self.name)
        alpha_shape_len = len(alpha_shape)
        validator.check_integer("alpha's rank", alpha_shape_len, 1, Rel.LE, self.name)
        if alpha_shape_len == 1:
            validator.check_integer("alpha_shape[0]", alpha_shape[0], 1, Rel.EQ, self.name)
        l1_shape_len = len(l1_shape)
        validator.check_integer("l1's rank", l1_shape_len, 1, Rel.LE, self.name)
        if l1_shape_len == 1:
            validator.check_integer("l1_shape[0]", l1_shape[0], 1, Rel.EQ, self.name)
        l2_shape_len = len(l2_shape)
        validator.check_integer("l2's rank", l2_shape_len, 1, Rel.LE, self.name)
        if l2_shape_len == 1:
            validator.check_integer("l2_shape[0]", l2_shape[0], 1, Rel.EQ, self.name)
        return var_shape

    def infer_dtype(self, var_dtype, alpha_dtype, l1_dtype, l2_dtype, delta_dtype):
        valid_types = [mstype.float16, mstype.float32]
        args = {'var': var_dtype, 'delta': delta_dtype}
        validator.check_tensor_type_same(args, valid_types, self.name)
        validator.check_scalar_or_tensor_type_same({"alpha": alpha_dtype}, valid_types, self.name)
        validator.check_scalar_or_tensor_type_same({"l1": l1_dtype}, valid_types, self.name)
        validator.check_scalar_or_tensor_type_same({"l2": l2_dtype}, valid_types, self.name)
        return var_dtype


class LARSUpdate(PrimitiveWithInfer):
    """
    Conduct lars (layer-wise adaptive rate scaling) update on the square sum of gradient.

    Args:
        epsilon (float): Term added to the denominator to improve numerical stability. Default: 1e-05.
        hyperpara (float): Trust coefficient for calculating the local learning rate. Default: 0.001.
        use_clip (bool): Whether to use clip operation for calculating the local learning rate. Default: False.

    Inputs:
        - **weight** (Tensor) - The weight to be updated.
        - **gradient** (Tensor) - The gradient of weight, which has the same shape and dtype with weight.
        - **norm_weight** (Tensor) - A scalar tensor, representing the square sum of weight.
        - **norm_gradient** (Tensor) - A scalar tensor, representing the square sum of gradient.
        - **weight_decay** (Union[Number, Tensor]) - Weight decay. It should be a scalar tensor or number.
        - **learning_rate** (Union[Number, Tensor]) - Learning rate. It should be a scalar tensor or number.

    Outputs:
        Tensor, representing the new gradient.

    Examples:
        >>> from mindspore import Tensor
        >>> from mindspore.ops import operations as P
        >>> from mindspore.ops import functional as F
        >>> import mindspore.nn as nn
        >>> import numpy as np
        >>> class Net(nn.Cell):
        >>>     def __init__(self):
        >>>         super(Net, self).__init__()
        >>>         self.lars = P.LARSUpdate()
        >>>         self.reduce = P.ReduceSum()
        >>>     def construct(self, weight, gradient):
        >>>         w_square_sum = self.reduce(F.square(weight))
        >>>         grad_square_sum = self.reduce(F.square(gradient))
        >>>         grad_t = self.lars(weight, gradient, w_square_sum, grad_square_sum, 0.0, 1.0)
        >>>         return grad_t
        >>> weight = np.random.random(size=(2, 3)).astype(np.float32)
        >>> gradient = np.random.random(size=(2, 3)).astype(np.float32)
        >>> net = Net()
        >>> ms_output = net(Tensor(weight), Tensor(gradient))
    """

    @prim_attr_register
    def __init__(self, epsilon=1e-05, hyperpara=0.001, use_clip=False):
        """init"""
        validator.check_value_type("epsilon", epsilon, [float], self.name)
        validator.check_value_type("hyperpara", hyperpara, [float], self.name)
        validator.check_value_type("use_clip", use_clip, [bool], self.name)

    def infer_shape(self, weight_shape, gradient_shape, norm_weight_shape, norm_gradient_shape, weight_decay_shape,
                    learning_rate_shape):
        validator.check("weight shape", weight_shape, "gradient shape", gradient_shape, Rel.EQ, self.name)
        validator.check("norm weight shape", norm_weight_shape, "norm gradient shape", norm_gradient_shape, Rel.EQ,
                        self.name)
        shp_len = len(weight_decay_shape)
        validator.check_integer("weight decay's rank", shp_len, 1, Rel.LE, self.name)
        if shp_len == 1:
            validator.check_integer("weight_decay_shape[0]", weight_decay_shape[0], 1, Rel.EQ, self.name)
        shp_len = len(learning_rate_shape)
        validator.check_integer("learning rate's rank", shp_len, 1, Rel.LE, self.name)
        if shp_len == 1:
            validator.check_integer("learning_rate_shape[0]", learning_rate_shape[0], 1, Rel.EQ, self.name)
        return weight_shape

    def infer_dtype(self, weight_dtype, gradient_dtype, norm_weight_dtype, norm_gradient_dtype,
                    weight_decay_dtype, learning_rate_dtype):
        args = {"Weight dtype": weight_dtype, "gradient dtype": gradient_dtype, "norm weight dtype": norm_weight_dtype,
                "norm gradient dtype": norm_gradient_dtype}
        validator.check_tensor_type_same(args, [mstype.float16, mstype.float32, mstype.int16, mstype.int32], self.name)
        validator.check_scalar_or_tensor_type_same({"weight_decay": weight_decay_dtype},
                                                   [mstype.float16, mstype.float32, mstype.float64], self.name)
        validator.check_scalar_or_tensor_type_same({"learning_rate": learning_rate_dtype},
                                                   [mstype.float16, mstype.float32, mstype.float64], self.name)
        return weight_dtype


class ApplyFtrl(PrimitiveWithInfer):
    """
    Update relevant entries according to the FTRL scheme.

    Args:
        use_locking (bool): Use locks for updating operation if True . Default: False.

    Inputs:
        - **var** (Parameter) - The variable to be updated. The data type should be float16 or float32.
        - **accum** (Parameter) - The accum to be updated, must be same type and shape as `var`.
        - **linear** (Parameter) - The linear to be updated, must be same type and shape as `var`.
        - **grad** (Tensor) - Gradient. The data type should be float16 or float32.
        - **lr** (Union[Number, Tensor]) - The learning rate value, must be positive. Default: 0.001.
          It should be a float number or a scalar tensor with float16 or float32 data type.
        - **l1** (Union[Number, Tensor]) - l1 regularization strength, must be greater than or equal to zero.
          Default: 0.0. It should be a float number or a scalar tensor with float16 or float32 data type.
        - **l2** (Union[Number, Tensor]) - l2 regularization strength, must be greater than or equal to zero.
          Default: 0.0. It should be a float number or a scalar tensor with float16 or float32 data type.
        - **lr_power** (Union[Number, Tensor]) - Learning rate power controls how the learning rate decreases
          during training, must be less than or equal to zero. Use fixed learning rate if lr_power is zero.
          Default: -0.5. It should be a float number or a scalar tensor with float16 or float32 data type.

    Outputs:
        Tensor, representing the updated var.

    Examples:
        >>> import mindspore
        >>> import mindspore.nn as nn
        >>> import numpy as np
        >>> from mindspore import Parameter
        >>> from mindspore import Tensor
        >>> from mindspore.ops import operations as P
        >>> class ApplyFtrlNet(nn.Cell):
        >>>     def __init__(self):
        >>>         super(ApplyFtrlNet, self).__init__()
        >>>         self.apply_ftrl = P.ApplyFtrl()
        >>>         self.lr = 0.001
        >>>         self.l1 = 0.0
        >>>         self.l2 = 0.0
        >>>         self.lr_power = -0.5
        >>>         self.var = Parameter(Tensor(np.random.rand(3, 3).astype(np.float32)), name="var")
        >>>         self.accum = Parameter(Tensor(np.random.rand(3, 3).astype(np.float32)), name="accum")
        >>>         self.linear = Parameter(Tensor(np.random.rand(3, 3).astype(np.float32)), name="linear")
        >>>
        >>>     def construct(self, grad):
        >>>         out = self.apply_ftrl(self.var, self.accum, self.linear, grad, self.lr, self.l1, self.l2,
        >>>                               self.lr_power)
        >>>         return out
        >>>
        >>> net = ApplyFtrlNet()
        >>> input_x = Tensor(np.random.randint(-4, 4, (3, 3)), mindspore.float32)
        >>> result = net(input_x)
        [[0.67455846   0.14630564   0.160499  ]
         [0.16329421   0.00415689   0.05202988]
         [0.18672481   0.17418946   0.36420345]]
    """

    @prim_attr_register
    def __init__(self, use_locking=False):
        self.init_prim_io_names(inputs=['var', 'accum', 'linear', 'grad', 'lr', 'l1', 'l2', 'lr_power'],
                                outputs=['output'])
        self.use_locking = validator.check_value_type("use_locking", use_locking, [bool], self.name)
        self.is_tbe = context.get_context("device_target") == "Ascend"

    def infer_shape(self, var_shape, accum_shape, linear_shape, grad_shape, lr_shape, l1_shape, l2_shape,
                    lr_power_shape):
        validator.check('var shape', var_shape, 'accum shape', accum_shape, Rel.EQ, self.name)
        validator.check('var shape', var_shape, 'linear shape', linear_shape, Rel.EQ, self.name)
        if self.is_tbe:
            return var_shape, var_shape, var_shape
        return var_shape

    def infer_dtype(self, var_type, accum_type, linear_type, grad_type, lr_type, l1_type, l2_type, lr_power_type):
        valid_types = [mstype.float16, mstype.float32]
        args = {'var': var_type, 'accum': accum_type, 'linear': linear_type, 'grad': grad_type}
        validator.check_tensor_type_same(args, valid_types, self.name)

        validator.check_scalar_or_tensor_type_same({"lr": lr_type}, valid_types, self.name)
        validator.check_scalar_or_tensor_type_same({"l1": l1_type}, valid_types, self.name)
        validator.check_scalar_or_tensor_type_same({"l2": l2_type}, valid_types, self.name)
        validator.check_scalar_or_tensor_type_same({"lr_power": lr_power_type}, valid_types, self.name)
        if self.is_tbe:
            return var_type, var_type, var_type
        return var_type


class SparseApplyFtrl(PrimitiveWithInfer):
    """
    Update relevant entries according to the FTRL-proximal scheme.

    Args:
        lr (float): The learning rate value, must be positive.
        l1 (float): l1 regularization strength, must be greater than or equal to zero.
        l2 (float): l2 regularization strength, must be greater than or equal to zero.
        lr_power (float): Learning rate power controls how the learning rate decreases during training,
            must be less than or equal to zero. Use fixed learning rate if `lr_power` is zero.
        use_locking (bool): Use locks for updating operation if True . Default: False.

    Inputs:
        - **var** (Parameter) - The variable to be updated. The data type must be float16 or float32.
        - **accum** (Parameter) - The accum to be updated, must be same type and shape as `var`.
        - **linear** (Parameter) - The linear to be updated, must be same type and shape as `var`.
        - **grad** (Tensor) - A tensor of the same type as `var`, for the gradient.
        - **indices** (Tensor) - A vector of indices into the first dimension of `var` and `accum`.
          The shape of `indices` must be the same as `grad` in first dimension. The type must be int32.

    Outputs:
        - **var** (Tensor) - Tensor, has the same shape and type as `var`.
        - **accum** (Tensor) - Tensor, has the same shape and type as `accum`.
        - **linear** (Tensor) - Tensor, has the same shape and type as `linear`.

    Examples:
        >>> import mindspore
        >>> import mindspore.nn as nn
        >>> import numpy as np
        >>> from mindspore import Parameter
        >>> from mindspore import Tensor
        >>> from mindspore.ops import operations as P
        >>> class SparseApplyFtrlNet(nn.Cell):
        >>>     def __init__(self):
        >>>         super(SparseApplyFtrlNet, self).__init__()
        >>>         self.sparse_apply_ftrl = P.SparseApplyFtrl(lr=0.01, l1=0.0, l2=0.0, lr_power=-0.5)
        >>>         self.var = Parameter(Tensor(np.random.rand(3, 3).astype(np.float32)), name="var")
        >>>         self.accum = Parameter(Tensor(np.random.rand(3, 3).astype(np.float32)), name="accum")
        >>>         self.linear = Parameter(Tensor(np.random.rand(3, 3).astype(np.float32)), name="linear")
        >>>
        >>>     def construct(self, grad, indices):
        >>>         out = self.sparse_apply_ftrl(self.var, self.accum, self.linear, grad, indices)
        >>>         return out
        >>>
        >>> net = SparseApplyFtrlNet()
        >>> grad = Tensor(np.random.rand(3, 3).astype(np.float32))
        >>> indices = Tensor(np.ones([3]), mindspore.int32)
        >>> output = net(grad, indices)
    """

    __mindspore_signature__ = (
        ('var', sig_rw.RW_WRITE, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('accum', sig_rw.RW_WRITE, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('linear', sig_rw.RW_WRITE, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('grad', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('indices', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T1)
    )

    @prim_attr_register
    def __init__(self, lr, l1, l2, lr_power, use_locking=False):
        validator.check_value_type("lr", lr, [float], self.name)
        validator.check_value_type("l1", l1, [float], self.name)
        validator.check_value_type("l2", l2, [float], self.name)
        validator.check_value_type("lr_power", lr_power, [float], self.name)
        self.lr = validator.check_number_range("lr", lr, 0.0, float("inf"), Rel.INC_NEITHER, self.name)
        self.l1 = validator.check_number_range("l1", l1, 0.0, float("inf"), Rel.INC_LEFT, self.name)
        self.l2 = validator.check_number_range("l2", l2, 0.0, float("inf"), Rel.INC_LEFT, self.name)
        self.lr_power = validator.check_number("lr_power", lr_power, 0, Rel.LE, self.name)
        self.use_locking = validator.check_value_type("use_locking", use_locking, [bool], self.name)

    def infer_shape(self, var_shape, accum_shape, linear_shape, grad_shape, indices_shape):
        validator.check('var shape', var_shape, 'accum shape', accum_shape, Rel.EQ, self.name)
        validator.check('var shape', var_shape, 'linear shape', linear_shape, Rel.EQ, self.name)
        if len(var_shape) > 1:
            validator.check('var_shape[1:]', var_shape[1:], 'grad_shape[1:]', grad_shape[1:], Rel.EQ, self.name)
        validator.check_integer("indices rank", len(indices_shape), 1, Rel.EQ, self.name)
        validator.check('grad_shape[0]', grad_shape[0], 'indices_shape[0]', indices_shape[0], Rel.EQ, self.name)
        return var_shape, accum_shape, linear_shape

    def infer_dtype(self, var_dtype, accum_dtype, linear_dtype, grad_dtype, indices_dtype):
        args = {"var_dtype": var_dtype, "accum_dtype": accum_dtype,
                "linear_dtype": linear_dtype, "grad_dtype": grad_dtype}
        validator.check_tensor_type_same(args, [mstype.float16, mstype.float32], self.name)
        validator.check_tensor_type_same({"indices_dtype": indices_dtype}, [mstype.int32], self.name)
        return var_dtype, accum_dtype, linear_dtype


class SparseApplyFtrlV2(PrimitiveWithInfer):
    """
    Update relevant entries according to the FTRL-proximal scheme.

    Args:
        lr (float): The learning rate value, must be positive.
        l1 (float): l1 regularization strength, must be greater than or equal to zero.
        l2 (float): l2 regularization strength, must be greater than or equal to zero.
        l2_shrinkage (float): L2 shrinkage regularization.
        lr_power (float): Learning rate power controls how the learning rate decreases during training,
            must be less than or equal to zero. Use fixed learning rate if `lr_power` is zero.
        use_locking (bool): If `True`, updating of the var and accum tensors will be protected. Default: False.

    Inputs:
        - **var** (Parameter) - The variable to be updated. The data type must be float16 or float32.
        - **accum** (Parameter) - The accum to be updated, must be same type and shape as `var`.
        - **linear** (Parameter) - The linear to be updated, must be same type and shape as `var`.
        - **grad** (Tensor) - A tensor of the same type as `var`, for the gradient.
        - **indices** (Tensor) - A vector of indices into the first dimension of `var` and `accum`.
          The shape of `indices` must be the same as `grad` in first dimension. The type must be int32.

    Outputs:
        Tuple of 3 Tensor, the updated parameters.

        - **var** (Tensor) - Tensor, has the same shape and type as `var`.
        - **accum** (Tensor) - Tensor, has the same shape and type as `accum`.
        - **linear** (Tensor) - Tensor, has the same shape and type as `linear`.

    Examples:
        >>> import mindspore
        >>> import mindspore.nn as nn
        >>> import numpy as np
        >>> from mindspore import Parameter
        >>> from mindspore import Tensor
        >>> from mindspore.ops import operations as P
        >>> class SparseApplyFtrlV2Net(nn.Cell):
        >>>     def __init__(self):
        >>>         super(SparseApplyFtrlV2Net, self).__init__()
        >>>         self.sparse_apply_ftrl_v2 = P.SparseApplyFtrlV2(lr=0.01, l1=0.0, l2=0.0,
                                                                    l2_shrinkage=0.0, lr_power=-0.5)
        >>>         self.var = Parameter(Tensor(np.random.rand(3, 3).astype(np.float32)), name="var")
        >>>         self.accum = Parameter(Tensor(np.random.rand(3, 3).astype(np.float32)), name="accum")
        >>>         self.linear = Parameter(Tensor(np.random.rand(3, 3).astype(np.float32)), name="linear")
        >>>
        >>>     def construct(self, grad, indices):
        >>>         out = self.sparse_apply_ftrl_v2(self.var, self.accum, self.linear, grad, indices)
        >>>         return out
        >>>
        >>> net = SparseApplyFtrlV2Net()
        >>> grad = Tensor(np.random.rand(3, 3).astype(np.float32))
        >>> indices = Tensor(np.ones([3]), mindspore.int32)
        >>> output = net(grad, indices)
    """

    __mindspore_signature__ = (
        ('var', sig_rw.RW_WRITE, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('accum', sig_rw.RW_WRITE, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('linear', sig_rw.RW_WRITE, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('grad', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T),
        ('indices', sig_rw.RW_READ, sig_kind.KIND_POSITIONAL_KEYWORD, sig_kind.KIND_EMPTY_DEFAULT_VALUE, sig_dtype.T1)
    )

    @prim_attr_register
    def __init__(self, lr, l1, l2, l2_shrinkage, lr_power, use_locking=False):
        validator.check_value_type("lr", lr, [float], self.name)
        validator.check_value_type("l1", l1, [float], self.name)
        validator.check_value_type("l2", l2, [float], self.name)
        validator.check_value_type("lr_power", lr_power, [float], self.name)
        self.lr = validator.check_number_range("lr", lr, 0.0, float("inf"), Rel.INC_NEITHER, self.name)
        self.l1 = validator.check_number_range("l1", l1, 0.0, float("inf"), Rel.INC_LEFT, self.name)
        self.l2 = validator.check_number_range("l2", l2, 0.0, float("inf"), Rel.INC_LEFT, self.name)
        self.lr_power = validator.check_number("lr_power", lr_power, 0, Rel.LE, self.name)
        self.l2_shrinkage = validator.check_value_type("l2_shrinkage", l2_shrinkage, [float], self.name)
        self.use_locking = validator.check_value_type("use_locking", use_locking, [bool], self.name)

    def infer_shape(self, var_shape, accum_shape, linear_shape, grad_shape, indices_shape):
        validator.check('var shape', var_shape, 'accum shape', accum_shape, Rel.EQ, self.name)
        validator.check('var shape', var_shape, 'linear shape', linear_shape, Rel.EQ, self.name)
        if len(var_shape) > 1:
            validator.check('var_shape[1:]', var_shape[1:], 'grad_shape[1:]', grad_shape[1:], Rel.EQ, self.name)
        validator.check_integer("indices rank", len(indices_shape), 1, Rel.EQ, self.name)
        validator.check('grad_shape[0]', grad_shape[0], 'indices_shape[0]', indices_shape[0], Rel.EQ, self.name)
        return var_shape, accum_shape, linear_shape

    def infer_dtype(self, var_dtype, accum_dtype, linear_dtype, grad_dtype, indices_dtype):
        args = {"var_dtype": var_dtype, "accum_dtype": accum_dtype,
                "linear_dtype": linear_dtype, "grad_dtype": grad_dtype}
        validator.check_tensor_type_same(args, [mstype.float16, mstype.float32], self.name)
        validator.check_tensor_type_same({"indices_dtype": indices_dtype}, [mstype.int32], self.name)
        return var_dtype, accum_dtype, linear_dtype


class ConfusionMulGrad(PrimitiveWithInfer):
    """
    `output0` is the result of which input0 dot multily input1.

    `output1` is the result of which input0 dot multily input1, then reducesum it.

    Args:
        axis (Union[int, tuple[int], list[int]]): The dimensions to reduce.
            Default:(), reduce all dimensions. Only constant value is allowed.
        keep_dims (bool):
            - If true, keep these reduced dimensions and the length is 1.
            - If false, don't keep these dimensions. Default:False.

    Inputs:
        - **input_0** (Tensor) - The input Tensor.
        - **input_1** (Tensor) - The input Tensor.
        - **input_2** (Tensor) - The input Tensor.

    outputs:
        - **output_0** (Tensor) - The same shape with `input0`.
        - **output_1** (Tensor)

            - If axis is (), and keep_dims is false, the output is a 0-D array representing
              the sum of all elements in the input array.
            - If axis is int, set as 2, and keep_dims is false,
              the shape of output is :math:`(x_1,x_3,...,x_R)`.
            - If axis is tuple(int), set as (2,3), and keep_dims is false,
              the shape of output is :math:`(x_1,x_4,...x_R)`.

    Examples:
        >>> confusion_mul_grad = P.ConfusionMulGrad()
        >>> input_0 = Tensor(np.random.randint(-2, 2, (2, 3)), mindspore.float32)
        >>> input_1 = Tensor(np.random.randint(0, 4, (2, 3)), mindspore.float32)
        >>> input_2 = Tensor(np.random.randint(-4, 0, (2, 3)), mindspore.float32)
        >>> output_0, output_1 = confusion_mul_grad(input_0, input_1, input_2)
        output_0:
            [[ 3.   1.   0.]
             [-6.   2.  -2.]]
        output_1:
            -3.0
    """

    @prim_attr_register
    def __init__(self, axis=(), keep_dims=False):
        self.init_prim_io_names(inputs=["input0", "input1", "input2"], outputs=["output0", "output1"])
        self.axis_ = validator.check_value_type("axis", axis, [int, tuple, list], self.name)
        self.keep_dims_ = validator.check_value_type("keep_dims", keep_dims, [bool], self.name)

    def infer_shape(self, input0_shape, input1_shape, input2_shape):
        outshape0 = input0_shape
        outshape1 = _infer_shape_reduce(input1_shape, self.axis_, self.keep_dims_, self.name)
        return outshape0, outshape1

    def infer_dtype(self, input0_dtype, input1_dtype, input2_dtype):
        validator.check_subclass("input0_dtype", input0_dtype, mstype.tensor, self.name)
        validator.check_subclass("input1_dtype", input1_dtype, mstype.tensor, self.name)
        validator.check_subclass("input2_dtype", input2_dtype, mstype.tensor, self.name)
        return input0_dtype, input1_dtype


class Dropout(PrimitiveWithInfer):
    """
    During training, randomly zeroes some of the elements of the input tensor with probability.

    Args:
        keep_prob (float): The keep rate, between 0 and 1, e.g. keep_prob = 0.9,
          means dropping out 10% of input units.

    Inputs:
        - **shape** (tuple[int]) - The shape of target mask.

    Outputs:
        Tensor, the value of generated mask for input shape.

    Examples:
        >>> dropout = P.Dropout(keep_prob=0.5)
        >>> in = Tensor((20, 16, 50, 50))
        >>> out = dropout(in)
    """

    @prim_attr_register
    def __init__(self, keep_prob=0.5):
        self.keep_prob = validator.check_number_range("keep_prob", keep_prob, 0, 1, Rel.INC_RIGHT, self.name)

    def infer_shape(self, x_shape):
        validator.check_integer("x_shape", len(x_shape), 1, Rel.GE, self.name)
        mask_shape = x_shape
        return x_shape, mask_shape

    def infer_dtype(self, x_dtype):
        valid_types = (mstype.float16, mstype.float32)
        validator.check_subclass("x", x_dtype, mstype.tensor, self.name)
        validator.check_tensor_type_same({"x_dtype": x_dtype}, valid_types, self.name)
        return x_dtype, x_dtype


class DropoutGrad(PrimitiveWithInfer):
    """
    The gradient of Dropout. During training, randomly zeroes some of the elements
    of the input tensor with probability.

    Args:
        keep_prob (float): The keep rate, between 0 and 1, e.g. keep_prob = 0.9,
          means dropping out 10% of input units.

    Inputs:
        - **shape** (tuple[int]) - The shape of target mask.

    Outputs:
        Tensor, the value of generated mask for input shape.

    Examples:
        >>> dropout_grad = P.DropoutGrad(keep_prob=0.5)
        >>> in = Tensor((20, 16, 50, 50))
        >>> out = dropout_grad(in)
    """

    @prim_attr_register
    def __init__(self, keep_prob=0.5):
        self.keep_prob = validator.check_number_range("keep_prob", keep_prob, 0, 1, Rel.INC_RIGHT, self.name)

    def infer_shape(self, dy_shape, mask_shape):
        return dy_shape

    def infer_dtype(self, dy_dtype, mask_dtype):
        valid_types = (mstype.float16, mstype.float32)
        validator.check_subclass("dy", dy_dtype, mstype.tensor, self.name)
        validator.check_subclass("mask", mask_dtype, mstype.tensor, self.name)
        validator.check_tensor_type_same({"dy_dtype": dy_dtype}, valid_types, self.name)
        return dy_dtype


class CTCLoss(PrimitiveWithInfer):
    """
    Calculates the CTC(Connectionist Temporal Classification) loss. Also calculates the gradient.

    Args:
        preprocess_collapse_repeated (bool): If true, repeated labels are collapsed prior to the CTC calculation.
                                             Default: False.
        ctc_merge_repeated (bool): If false, during CTC calculation, repeated non-blank labels will not be merged
                                   and are interpreted as individual labels. This is a simplfied version of CTC.
                                   Default: True.
        ignore_longer_outputs_than_inputs (bool): If True, sequences with longer outputs than inputs will be ignored.
                                                  Default: False.

    Inputs:
        - **inputs** (Tensor) - The input Tensor should be a `3-D` tensor whose shape is
          :math:`(max_time, batch_size, num_classes)`. `num_classes` should be `num_labels + 1` classes, `num_labels`
          indicates the number of actual labels. Blank labels are reserved. Default blank label is `num_classes - 1`.
          Data type must be float32 or float64.
        - **labels_indices** (Tensor) - The indices of labels. `labels_indices[i, :] == [b, t]` means `labels_values[i]`
          stores the id for `(batch b, time t)`. The type must be int64 and rank must be 2.
        - **labels_values** (Tensor) - A `1-D` input tensor. The values associated with the given batch and time. The
          type must be int32. `labels_values[i]` must in the range of `[0, num_classes)`.
        - **sequence_length** (Tensor) - A tensor containing sequence lengths with the shape of :math:`(batch_size)`.
          The type must be int32. Each value in the tensor should not greater than `max_time`.

    Outputs:
        - **loss** (Tensor) - A tensor containing log-probabilities, the shape is :math:`(batch_size)`. Has the same
          type with `inputs`.
        - **gradient** (Tensor) - The gradient of `loss`. Has the same type and shape with `inputs`.

    Examples:
        >>> inputs = Tensor(np.random.random((2, 2, 3)), mindspore.float32)
        >>> labels_indices = Tensor(np.array([[0, 0], [1, 0]]), mindspore.int64)
        >>> labels_values = Tensor(np.array([2, 2]), mindspore.int32)
        >>> sequence_length = Tensor(np.array([2, 2]), mindspore.int32)
        >>> ctc_loss = P.CTCLoss()
        >>> output = ctc_loss(inputs, labels_indices, labels_values, sequence_length)
    """

    @prim_attr_register
    def __init__(self, preprocess_collapse_repeated=False, ctc_merge_repeated=True,
                 ignore_longer_outputs_than_inputs=False):
        self.init_prim_io_names(inputs=["inputs", "labels_indices", "labels_values", "sequence_length"],
                                outputs=["loss", "gradient"])
        validator.check_value_type("preprocess_collapse_repeated", preprocess_collapse_repeated, [bool], self.name)
        self.preprocess_collapse_repeated_ = preprocess_collapse_repeated
        self.ctc_merge_repeated_ = validator.check_value_type("ctc_merge_repeated", ctc_merge_repeated,
                                                              [bool], self.name)
        validator.check_value_type("ignore_longer_outputs_than_inputs",
                                   ignore_longer_outputs_than_inputs, [bool], self.name)
        self.ignore_longer_outputs_than_inputs_ = ignore_longer_outputs_than_inputs

    def infer_shape(self, inputs, labels_indices, labels_values, sequence_length):
        validator.check_integer("inputs rank", len(inputs), 3, Rel.EQ, self.name)
        validator.check_integer("labels_indices rank", len(labels_indices), 2, Rel.EQ, self.name)
        validator.check_integer("labels_indices dim one", labels_indices[1], 2, Rel.EQ, self.name)
        validator.check_integer("labels_values rank", len(labels_values), 1, Rel.EQ, self.name)
        validator.check_integer("sequence_length rank", len(sequence_length), 1, Rel.EQ, self.name)
        validator.check('labels_indices size', labels_indices[0], 'labels_values size',
                        labels_values[0], Rel.EQ, self.name)
        validator.check('inputs batch_size', inputs[1], 'sequence_length batch_size',
                        sequence_length[0], Rel.EQ, self.name)
        batch_size = []
        batch_size.append(inputs[1])
        return batch_size, inputs

    def infer_dtype(self, inputs, labels_indices, labels_values, sequence_length):
        validator.check_tensor_type_same({"inputs_dtype": inputs}, [mstype.float32, mstype.double], self.name)
        validator.check_tensor_type_same({"labels_indices_dtype": labels_indices}, [mstype.int64], self.name)
        validator.check_tensor_type_same({"labels_values_dtype": labels_values}, [mstype.int32], self.name)
        validator.check_tensor_type_same({"sequence_length_dtype": sequence_length}, [mstype.int32], self.name)
        return inputs, inputs


class CTCGreedyDecoder(PrimitiveWithInfer):
    """
    Performs greedy decoding on the logits given in inputs.

    Args:
        merge_repeated (bool): If True, merge repeated classes in output. Default: True.

    Inputs:
        - **inputs** (Tensor) - The input Tensor should be a `3-D` tensor whose shape is
          :math:`(max_time, batch_size, num_classes)`. `num_classes` should be `num_labels + 1` classes, `num_labels`
          indicates the number of actual labels. Blank labels are reserved. Default blank label is `num_classes - 1`.
          Data type must be float32 or float64.
        - **sequence_length** (Tensor) - A tensor containing sequence lengths with the shape of :math:`(batch_size)`.
          The type must be int32. Each value in the tensor should not greater than `max_time`.

    Outputs:
        - **decoded_indices** (Tensor) - A tensor with shape of :math:`(total_decoded_outputs, 2)`.
          Data type is int64.
        - **decoded_values** (Tensor) - A tensor with shape of :math:`(total_decoded_outputs)`,
          it stores the decoded classes. Data type is int64.
        - **decoded_shape** (Tensor) - The value of tensor is :math:`[batch_size, max_decoded_legth]`.
          Data type is int64.
        - **log_probability** (Tensor) - A tensor with shape of :math:`(batch_size, 1)`,
          containing sequence log-probability. Has the same type as `inputs`.

    Examples:
        >>>    class CTCGreedyDecoderNet(nn.Cell):
        >>>        def __init__(self):
        >>>            super(CTCGreedyDecoderNet, self).__init__()
        >>>            self.ctc_greedy_decoder = P.CTCGreedyDecoder()
        >>>            self.assert_op = P.Assert(300)
        >>>
        >>>        def construct(self, inputs, sequence_length):
        >>>            out = self.ctc_greedy_decoder(inputs,sequence_length)
        >>>            self.assert_op(True, (out[0], out[1], out[2], out[3]))
        >>>            return out[2]
        >>>
        >>> inputs = Tensor(np.random.random((2, 2, 3)), mindspore.float32)
        >>> sequence_length = Tensor(np.array([2, 2]), mindspore.int32)
        >>> net = CTCGreedyDecoderNet()
        >>> output = net(inputs, sequence_length)
    """

    @prim_attr_register
    def __init__(self, merge_repeated=True):
        self.merge_repeated = validator.check_value_type("merge_repeated", merge_repeated, [bool], self.name)

    def infer_shape(self, inputs_shape, sequence_length_shape):
        validator.check_integer("inputs rank", len(inputs_shape), 3, Rel.EQ, self.name)
        validator.check_integer("sequence_length rank", len(sequence_length_shape), 1, Rel.EQ, self.name)
        validator.check('inputs batch_size', inputs_shape[1], 'sequence_length batch_size',
                        sequence_length_shape[0], Rel.EQ, self.name)
        total_decoded_outputs = -1
        decoded_indices_shape = [total_decoded_outputs, 2]
        decoded_values = [total_decoded_outputs]
        decoded_shape = [2]
        log_probability_shape = [inputs_shape[1], 1]
        return decoded_indices_shape, decoded_values, decoded_shape, log_probability_shape

    def infer_dtype(self, inputs_dtype, sequence_length_dtype):
        validator.check_tensor_type_same({"inputs_dtype": inputs_dtype}, [mstype.float32, mstype.double], self.name)
        validator.check_tensor_type_same({"sequence_length_dtype": sequence_length_dtype}, [mstype.int32], self.name)
        decoded_type = mstype.tensor_type(mstype.int64)
        return decoded_type, decoded_type, decoded_type, inputs_dtype


class BasicLSTMCell(PrimitiveWithInfer):
    r"""
    Performs the long short term memory(LSTM) on the input.

    .. math::
        \begin{array}{ll} \\
            i_t = \sigma(W_{ix} x_t + b_{ix} + W_{ih} h_{(t-1)} + b_{ih}) \\
            f_t = \sigma(W_{fx} x_t + b_{fx} + W_{fh} h_{(t-1)} + b_{fh}) \\
            \tilde{c}_t = \tanh(W_{cx} x_t + b_{cx} + W_{ch} h_{(t-1)} + b_{ch}) \\
            o_t = \sigma(W_{ox} x_t + b_{ox} + W_{oh} h_{(t-1)} + b_{oh}) \\
            c_t = f_t * c_{(t-1)} + i_t * \tilde{c}_t \\
            h_t = o_t * \tanh(c_t) \\
        \end{array}

    Here :math:`\sigma` is the sigmoid function, and :math:`*` is the Hadamard product. :math:`W, b`
    are learnable weights between the output and the input in the formula. For instance,
    :math:`W_{ix}, b_{ix}` are the weight and bias used to transform from input :math:`x` to :math:`i`.
    Details can be found in paper `LONG SHORT-TERM MEMORY
    <https://www.bioinf.jku.at/publications/older/2604.pdf>`_ and
    `Long Short-Term Memory Recurrent Neural Network Architectures for Large Scale Acoustic Modeling
    <https://static.googleusercontent.com/media/research.google.com/zh-CN//pubs/archive/43905.pdf>`_.

    Args:
        keep_prob (float): If not 1.0, append `Dropout` layer on the outputs of each
            LSTM layer except the last layer. Default 1.0. The range of dropout is [0.0, 1.0].
        forget_bias (float): Add forget bias to forget gate biases in order to decrease former scale. Default to 1.0.
        state_is_tuple (bool): If true, state is tensor tuple, containing h and c; If false, one tensor,
          need split first. Default to True.
        activation (str): Activation. Default to "tanh".

    Inputs:
        - **x** (Tensor) - Current words. Tensor of shape (`batch_size`, `input_size`).
        - **h** (Tensor) - Hidden state last moment. Tensor of shape (`batch_size`, `hidden_size`).
        - **c** (Tensor) - Cell state last moment. Tensor of shape (`batch_size`, `hidden_size`).
        - **w** (Tensor) - Weight. Tensor of shape (`4 x hidden_size`, `input_size + hidden_size`, 1, 1).
        - **b** (Tensor) - Bias. Tensor of shape (`4 x hidden_size`, 1, 1, 1).

    Outputs:
        - **ct** (Tensor) - Forward :math:`c_t` cache at moment `t`. Tensor of shape (`batch_size`, `hidden_size`).
        - **ht** (Tensor) - Cell output. Tensor of shape (`batch_size`, `hidden_size`).
        - **it** (Tensor) - Forward :math:`i_t` cache at moment `t`. Tensor of shape (`batch_size`, `hidden_size`).
        - **jt** (Tensor) - Forward :math:`j_t` cache at moment `t`. Tensor of shape (`batch_size`, `hidden_size`).
        - **ft** (Tensor) - Forward :math:`f_t` cache at moment `t`. Tensor of shape (`batch_size`, `hidden_size`).
        - **ot** (Tensor) - Forward :math:`o_t` cache at moment `t`. Tensor of shape (`batch_size`, `hidden_size`).
        - **tanhct** (Tensor) - Forward :math:`tanh c_t` cache at moment `t`.
          Tensor of shape (`batch_size`, `hidden_size`).

    Examples:
         'block': P.BasicLSTMCell(keep_prob=1.0, forget_bias=1.0, state_is_tuple=True, activation='tanh'),
        'desc_inputs': [[128, 128], [128, 128], [128, 128], [512, 256, 1, 1],[512, 1, 1, 1]],
        'desc_bprop': [[128, 128], [128, 128], [128, 128], [128, 128], [128, 128], [128, 128], [128, 128]],

        >>> x = Tensor(np.random.rand(128, 128).astype(np.float16))
        >>> h = Tensor(np.random.rand(128, 128).astype(np.float16))
        >>> c = Tensor(np.random.rand(128, 128).astype(np.float16))
        >>> w = Tensor(np.random.rand(512, 256, 1, 1).astype(np.float16))
        >>> b = Tensor(np.random.rand(512, 1, 1, 1).astype(np.float16))
        >>> lstm = P.BasicLSTMCell(keep_prob=1.0, forget_bias=1.0, state_is_tuple=True, activation='tanh')
        >>> lstm(x, h, c, w, b)
    """

    @prim_attr_register
    def __init__(self, keep_prob=1.0, forget_bias=1.0, state_is_tuple=True, activation='tanh'):
        self.keep_prob = validator.check_value_type("keep_prob", keep_prob, [float], self.name)
        self.keep_prob = validator.check_number_range("keep_prob", keep_prob, 0.0, 1.0, Rel.INC_BOTH, self.name)
        self.forget_bias = validator.check_value_type("forget_bias", forget_bias, [float], self.name)
        self.state_is_tuple = validator.check_value_type("state_is_tuple", state_is_tuple, [bool], self.name)
        self.activation = validator.check_string("activation", activation, ['tanh'], self.name)

    def infer_shape(self, x_shape, h_shape, c_shape, w_shape, b_shape):
        # (batch_size, input_size)
        validator.check_integer("x_shape", len(x_shape), 2, Rel.EQ, self.name)

        # h and c should be same shape
        validator.check_integer("h_shape", len(h_shape), 2, Rel.EQ, self.name)
        validator.check("h rank", len(h_shape), "c rank", len(c_shape), Rel.EQ, self.name)
        validator.check("h shape", h_shape, "c shape", c_shape, Rel.EQ, self.name)
        validator.check_integer("w rank", len(w_shape), 4, Rel.EQ, self.name)
        validator.check_integer("b rank", len(b_shape), 4, Rel.EQ, self.name)
        validator.check("w_shape[0]", w_shape[0], "4*h_shape[1]", 4 * h_shape[1], Rel.EQ, self.name)
        validator.check("w_shape[1]", w_shape[1], "x_shape[1]+h_shape[1]", x_shape[1] + h_shape[1], Rel.EQ, self.name)
        validator.check("b_shape[0]", b_shape[0], "4*h_shape[1]", 4 * h_shape[1], Rel.EQ, self.name)
        ct_shape = c_shape
        ht_shape = h_shape
        it_shape = h_shape
        jt_shape = h_shape
        ft_shape = h_shape
        ot_shape = h_shape
        tanhct_shape = h_shape

        return (ct_shape, ht_shape, it_shape, jt_shape, ft_shape, ot_shape, tanhct_shape)

    def infer_dtype(self, x_dtype, h_dtype, c_dtype, w_dtype, b_dtype):
        validator.check_subclass("x", x_dtype, [mstype.tensor], self.name)
        validator.check_subclass("h", h_dtype, [mstype.tensor], self.name)
        validator.check_subclass("c", c_dtype, [mstype.tensor], self.name)
        validator.check_subclass("w", w_dtype, [mstype.tensor], self.name)
        validator.check_subclass("b", b_dtype, [mstype.tensor], self.name)
        validator.check_type_name("x", x_dtype, [mstype.float16, mstype.float32], self.name)
        validator.check_type_name("h", h_dtype, [mstype.float16, mstype.float32], self.name)
        validator.check_type_name("c", c_dtype, [mstype.float16, mstype.float32], self.name)
        validator.check_type_name("w", w_dtype, [mstype.float16, mstype.float32], self.name)
        validator.check_type_name("b", b_dtype, [mstype.float16, mstype.float32], self.name)
        return (x_dtype, x_dtype, x_dtype, x_dtype, x_dtype, x_dtype, x_dtype)


class InTopK(PrimitiveWithInfer):
    r"""
    Says whether the targets are in the top `k` predictions.

    Args:
        k (int): Special the number of top elements to look at for computing precision.

    Inputs:
        - **x1** (Tensor) - A 2D Tensor define the predictions of a batch of samples with float16 or float32 data type.
        - **x2** (Tensor) - A 1D Tensor define the labels of a batch of samples with int32 data type.

    Outputs:
        Tensor, which is 1 dimension of type bool and has same shape with `x2`. for label of sample `i` in `x2`,
        if label in first `k` predictions for sample `i` in `x1`, then the value is True else False.

    Examples:
        >>> x1 = Tensor(np.array([[1, 8, 5, 2, 7], [4, 9, 1, 3, 5]]), mindspore.float32)
        >>> x2 = Tensor(np.array([1, 3]), mindspore.int32)
        >>> in_top_k = P.InTopK(3)
        >>> result = in_top_k(x1, x2)
        [True  False]
    """

    @prim_attr_register
    def __init__(self, k):
        """Init InTopK"""
        self.init_prim_io_names(inputs=['x1', 'x2', 'k'], outputs=['y'])
        validator.check_value_type("k", k, [int], self.name)

    def infer_dtype(self, x1_dtype, x2_dtype):
        validator.check_tensor_type_same({"x1": x1_dtype}, (mstype.float16, mstype.float32,), self.name)
        validator.check_tensor_type_same({"x2": x2_dtype}, (mstype.int32,), self.name)

        return mstype.tensor_type(mstype.bool_)

    def infer_shape(self, x1_shape, x2_shape):
        validator.check("x1", len(x1_shape), "", 2, Rel.EQ, self.name)
        validator.check("x2", len(x2_shape), "", 1, Rel.EQ, self.name)
        validator.check("size of x2", x2_shape[0], "x1's first dimension", x1_shape[0], Rel.EQ, self.name)
        return x2_shape


class LRN(PrimitiveWithInfer):
    r"""
    Local Response Normalization

    Args:
        depth_radius (int): Half-width of the 1-D normalization window. Shape of 0-D.
        bias (float): An offset (usually positive to avoid dividing by 0).
        alpha (float): A scale factor, usually positive.
        beta (float): An exponent.
        norm_region (str): Specify normalization region. Options: "ACROSS_CHANNELS". Default: "ACROSS_CHANNELS".

    Inputs:
        - **x** (Tensor) - A 4D Tensor with float16 or float32 data type.

    Outputs:
        Tensor, With shape and data type same as the input tensor.

    Examples:
        >>> x = Tensor(np.random.rand(1, 10, 4, 4)), mindspore.float32)
        >>> lrn = P.LRN()
        >>> lrn(x)
    """
    @prim_attr_register
    def __init__(self, depth_radius=5, bias=1.0, alpha=1.0, beta=0.5, norm_region="ACROSS_CHANNELS"):
        """Init LRN"""
        self.init_prim_io_names(inputs=['x'], outputs=['y'])
        validator.check_value_type("depth_radius", depth_radius, [int], self.name)
        validator.check_value_type("bias", bias, [float], self.name)
        validator.check_value_type("alpha", alpha, [float], self.name)
        validator.check_value_type("beta", beta, [float], self.name)
        validator.check_value_type("norm_region", norm_region, [str], self.name)
        validator.check_string('norm_region', norm_region, ['ACROSS_CHANNELS'], self.name)
        validator.check_integer("depth_radius", depth_radius, 0, Rel.GE, self.name)

    def infer_dtype(self, x_dtype):
        validator.check_tensor_type_same({"x": x_dtype}, (mstype.float16, mstype.float32,), self.name)
        return x_dtype

    def infer_shape(self, x_shape):
        validator.check_integer("x_shape", len(x_shape), 4, Rel.EQ, self.name)
        return x_shape


class CTCLossV2(PrimitiveWithInfer):
    r"""
    Calculates the CTC(Connectionist Temporal Classification) loss. Also calculates the gradient.
    Note:
        - Cudnn Uses label value of for the `blank`

    Inputs:
        - **inputs** (Tensor) - The input Tensor should be a `3-D` tensor whose shape is
          :math:`(max_time, batch_size, num_class)`. `num_class` should be `num_labels + 1` classes, `num_labels`
          indicates the number of actual labels. Blank labels are reserved.
        - **labels** (Tensor) - The labels Tensor should be a `1-D` tensor whose shape is
          :math:`(\sigma{label_lengths})`
          or `2-D` tensor whose shape is
          :math:`(max_time, max{label_lengths})`
          The type must be int32.
        - **input_lengths** (Tensor) - A `1-D` input tensor whose shape is
          :math:`(batch_size,)`. The values should be batch. The type must be int32.
        - **label_lengths** (Tensor) - A tensor containing sequence lengths with the shape of :math:`(batch_size)`.
          The type must be int32. Each value in the tensor should not greater than `max_time`.

    Outputs:
        - **loss** (Tensor) - A tensor containing log-probabilities, the shape is :math:`(batch_size)`. Has the same
          type with `inputs`.
        - **gradient** (Tensor) - The gradient of `loss`. Has the same type and shape with `inputs`.

    Examples:
        >>> inputs = Tensor(np.random.random((2, 2, 3)), mindspore.float32)
        >>> labels = Tensor(np.array([[0, 0], [1, 0]]), mindspore.int32)
        >>> input_lengths = Tensor(np.array([3, 3, 3]), mindspore.int32)
        >>> label_lengths = Tensor(np.array([3, 3, 3]), mindspore.int32)
        >>> ctc_loss = P.CTCLossV2()
        >>> output = ctc_loss(inputs, labels, input_lengths, label_lengths)
    """
    @prim_attr_register
    def __init__(self):
        pass

    def infer_dtype(self, input_dtype, labels_dtype, input_lengths_dtype, label_lengths_dtype):
        validator.check_tensor_type_same({"input": input_dtype}, (mstype.float32,), self.name)
        validator.check_tensor_type_same({"labels": labels_dtype}, (mstype.int32,), self.name)
        validator.check_tensor_type_same({"input_lengths": input_lengths_dtype}, (mstype.int32,), self.name)
        validator.check_tensor_type_same({"target_lengths": label_lengths_dtype}, (mstype.int32,), self.name)
        return mstype.float32, mstype.float32

    def infer_shape(self, input_shape, labels_shape, input_lengths_shape, label_lengths_shape):
        validator.check_integer("input shape", len(input_shape), 3, Rel.EQ, self.name)
        validator.check_number_range("labels shape", len(labels_shape), 1, 2, Rel.INC_BOTH, self.name)
        validator.check_integer("input lengths shape", len(input_lengths_shape), 1, Rel.EQ, self.name)
        validator.check_integer("label lengths shape", len(label_lengths_shape), 1, Rel.EQ, self.name)
        validator.check_integer("input[1]", input_shape[1], input_lengths_shape[0], Rel.EQ, self.name)
        validator.check_integer("input[1]", input_shape[1], label_lengths_shape[0], Rel.EQ, self.name)
        return (input_shape[1],), input_shape
