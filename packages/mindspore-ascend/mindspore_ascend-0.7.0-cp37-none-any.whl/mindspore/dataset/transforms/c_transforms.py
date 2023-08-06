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
"""
This module c_transforms provides common operations, including OneHotOp and TypeCast.
"""
from enum import IntEnum
import numpy as np

import mindspore.common.dtype as mstype
import mindspore._c_dataengine as cde

from .validators import check_num_classes, check_de_type, check_fill_value, check_slice_op, check_mask_op, \
    check_pad_end, check_concat_type, check_random_transform_ops
from ..core.datatypes import mstype_to_detype


class OneHot(cde.OneHotOp):
    """
    Tensor operation to apply one hot encoding.

    Args:
        num_classes (int): Number of classes of the label
            it should be bigger than largest label number in dataset.

    Raises:
        RuntimeError: feature size is bigger than num_classes.
    """

    @check_num_classes
    def __init__(self, num_classes):
        self.num_classes = num_classes
        super().__init__(num_classes)


class Fill(cde.FillOp):
    """
    Tensor operation to create a tensor filled with passed scalar value.
    The output tensor will have the same shape and type as the input tensor.

    Args:
        fill_value (Union[str, bytes, int, float, bool])) : scalar value
            to fill created tensor with.
    """

    @check_fill_value
    def __init__(self, fill_value):
        super().__init__(cde.Tensor(np.array(fill_value)))


class TypeCast(cde.TypeCastOp):
    """
    Tensor operation to cast to a given MindSpore data type.

    Args:
        data_type (mindspore.dtype): mindspore.dtype to be casted to.
    """

    @check_de_type
    def __init__(self, data_type):
        data_type = mstype_to_detype(data_type)
        self.data_type = str(data_type)
        super().__init__(data_type)


class Slice(cde.SliceOp):
    """
    Slice operation to extract a tensor out using the given n slices.

    The functionality of Slice is similar to NumPy indexing feature.
    (Currently only rank-1 tensors are supported).

    Args:
        slices(Union[int, list(int), slice, None, Ellipses]):
            Maximum `n` number of arguments to slice a tensor of rank `n`.
            One object in slices can be one of:
            1.  :py:obj:`int`: Slice this index only. Negative index is supported.
            2.  :py:obj:`list(int)`: Slice these indices ion the list only. Negative indices are supported.
            3.  :py:obj:`slice`: Slice the generated indices from the slice object. Similar to `start:stop:step`.
            4.  :py:obj:`None`: Slice the whole dimension. Similar to `:` in python indexing.
            5.  :py:obj:`Ellipses`: Slice all dimensions between the two slices. Similar to `...` in python indexing.

    Examples:
     >>> # Data before
     >>> # |   col   |
     >>> # +---------+
     >>> # | [1,2,3] |
     >>> # +---------|
     >>> data = data.map(operations=Slice(slice(1,3))) # slice indices 1 and 2 only
     >>> # Data after
     >>> # |   col   |
     >>> # +---------+
     >>> # |  [2,3]  |
     >>> # +---------|
    """

    @check_slice_op
    def __init__(self, *slices):
        dim0 = slices[0]
        if isinstance(dim0, int):
            dim0 = [dim0]
        elif dim0 is None:
            dim0 = True
        elif isinstance(dim0, slice):
            dim0 = (dim0.start, dim0.stop, dim0.step)
        elif dim0 is Ellipsis:
            dim0 = True
        super().__init__(dim0)


class Relational(IntEnum):
    EQ = 0
    NE = 1
    GT = 2
    GE = 3
    LT = 4
    LE = 5


DE_C_RELATIONAL = {Relational.EQ: cde.RelationalOp.EQ,
                   Relational.NE: cde.RelationalOp.NE,
                   Relational.GT: cde.RelationalOp.GT,
                   Relational.GE: cde.RelationalOp.GE,
                   Relational.LT: cde.RelationalOp.LT,
                   Relational.LE: cde.RelationalOp.LE}


class Mask(cde.MaskOp):
    """
    Mask content of the input tensor with the given predicate.
    Any element of the tensor that matches the predicate will be evaluated to True, otherwise False.

    Args:
        operator (Relational): One of the relational operator EQ, NE LT, GT, LE or GE
        constant (Union[str, int, float, bool]): constant to be compared to.
            Constant will be casted to the type of the input tensor
        dtype (mindspore.dtype, optional): type of the generated mask. Default to bool

    Examples:
        >>> # Data before
        >>> # |  col1   |
        >>> # +---------+
        >>> # | [1,2,3] |
        >>> # +---------+
        >>> data = data.map(operations=Mask(Relational.EQ, 2))
        >>> # Data after
        >>> # |       col1         |
        >>> # +--------------------+
        >>> # | [False,True,False] |
        >>> # +--------------------+
    """

    @check_mask_op
    def __init__(self, operator, constant, dtype=mstype.bool_):
        dtype = mstype_to_detype(dtype)
        constant = cde.Tensor(np.array(constant))
        super().__init__(DE_C_RELATIONAL[operator], constant, dtype)


class PadEnd(cde.PadEndOp):
    """
    Pad input tensor according to `pad_shape`, need to have same rank.

    Args:
        pad_shape (list(int)): list on integers representing the shape needed. Dimensions that set to `None` will
            not be padded (i.e., original dim will be used). Shorter dimensions will truncate the values.
        pad_value (Union[str, bytes, int, float, bool]), optional): value used to pad. Default to 0 or empty
            string in case of Tensors of strings.

    Examples:
        >>> # Data before
        >>> # |   col   |
        >>> # +---------+
        >>> # | [1,2,3] |
        >>> # +---------|
        >>> data = data.map(operations=PadEnd(pad_shape=[4], pad_value=10))
        >>> # Data after
        >>> # |    col     |
        >>> # +------------+
        >>> # | [1,2,3,10] |
        >>> # +------------|
    """

    @check_pad_end
    def __init__(self, pad_shape, pad_value=None):
        if pad_value is not None:
            pad_value = cde.Tensor(np.array(pad_value))
        super().__init__(cde.TensorShape(pad_shape), pad_value)


class Concatenate(cde.ConcatenateOp):
    """
    Tensor operation that concatenates all columns into a single tensor.

    Args:
        axis (int, optional): concatenate the tensors along given axis (Default=0).
        prepend (numpy.array, optional): numpy array to be prepended to the already concatenated tensors (Default=None).
        append (numpy.array, optional): numpy array to be appended to the already concatenated tensors (Default=None).
    """

    @check_concat_type
    def __init__(self, axis=0, prepend=None, append=None):
        if prepend is not None:
            prepend = cde.Tensor(np.array(prepend))
        if append is not None:
            append = cde.Tensor(np.array(append))
        super().__init__(axis, prepend, append)


class Duplicate(cde.DuplicateOp):
    """
    Duplicate the input tensor to a new output tensor. The input tensor is carried over to the output list.

    Examples:
        >>> # Data before
        >>> # |  x      |
        >>> # +---------+
        >>> # | [1,2,3] |
        >>> # +---------+
        >>> data = data.map(input_columns=["x"], operations=Duplicate(),
        >>>         output_columns=["x", "y"], columns_order=["x", "y"])
        >>> # Data after
        >>> # |  x      |  y      |
        >>> # +---------+---------+
        >>> # | [1,2,3] | [1,2,3] |
        >>> # +---------+---------+
    """


class Compose(cde.ComposeOp):
    """
    Compose a list of transforms into a single transform.

    Args:
        transforms (list): List of transformations to be applied.

    Examples:
        >>> compose = Compose([vision.Decode(), vision.RandomCrop()])
        >>> dataset = ds.map(operations=compose)
    """

    @check_random_transform_ops
    def __init__(self, transforms):
        super().__init__(transforms)


class RandomApply(cde.RandomApplyOp):
    """
    Randomly performs a series of transforms with a given probability.

    Args:
        transforms (list): List of transformations to be applied.
        prob (float, optional): The probability to apply the transformation list (default=0.5)

    Examples:
        >>> rand_apply = RandomApply([vision.RandomCrop()])
        >>> dataset = ds.map(operations=rand_apply)
    """

    @check_random_transform_ops
    def __init__(self, transforms, prob=0.5):
        super().__init__(prob, transforms)


class RandomChoice(cde.RandomChoiceOp):
    """
    Randomly selects one transform from a list of transforms to perform operation.

    Args:
        transforms (list): List of transformations to be chosen from to apply.

    Examples:
        >>> rand_choice = RandomChoice([vision.CenterCrop(), vision.RandomCrop()])
        >>> dataset = ds.map(operations=rand_choice)
    """

    @check_random_transform_ops
    def __init__(self, transforms):
        super().__init__(transforms)
