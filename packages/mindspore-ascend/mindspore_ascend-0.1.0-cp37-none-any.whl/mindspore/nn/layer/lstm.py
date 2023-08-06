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
"""lstm"""
from mindspore.ops import operations as P
from mindspore.nn.cell import Cell
from mindspore.common.parameter import Parameter
from mindspore.common.initializer import initializer
from mindspore._checkparam import ParamValidator as validator


class LSTM(Cell):
    r"""
    LSTM (Long Short-Term Memory) layer.

    Applies a LSTM to the input.

    There are two pipelines connecting two consecutive cells in a LSTM model; one is cell state pipeline
    and another is hidden state pipeline. Denote two consecutive time nodes as :math:`t-1` and :math:`t`.
    Given an input :math:`x_t` at time :math:`t`, an hidden state :math:`h_{t-1}` and an cell
    state :math:`c_{t-1}` of the layer at time :math:`{t-1}`, the cell state and hidden state at
    time :math:`t` is computed using an gating mechanism. Input gate :math:`i_t` is designed to protect the cell
    from perturbation by irrelevant inputs. Forget gate :math:`f_t` affords protection of the cell by forgetting
    some information in the past, which is stored in :math:`h_{t-1}`. Output gate :math:`o_t` protects other
    units from perturbation by currently irrelevant memory contents. Candidate cell state :math:`\tilde{c}_t` is
    calculated with the current input, on which the input gate will be applied. Finally, current cell state
    :math:`c_{t}` and hidden state :math:`h_{t}` are computed with the calculated gates and cell states. The complete
    formulation is as follows.

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
        input_size (int): Number of features of input.
        hidden_size (int):  Number of features of hidden layer.
        num_layers (int): Number of layers of stacked LSTM . Default: 1.
        has_bias (bool): Specifies whether has bias `b_ih` and `b_hh`. Default: True.
        batch_first (bool): Specifies whether the first dimension of input is batch_size. Default: False.
        dropout (float): If not 0, append `Dropout` layer on the outputs of each
            LSTM layer except the last layer. Default 0. The range of dropout is [0.0, 1.0].
        bidirectional (bool): Specifies whether this is a bidirectional LSTM. If set True,
            number of directions will be 2 otherwise number of directions is 1. Default: False.

    Inputs:
        - **input** (Tensor) - Tensor of shape (seq_len, batch_size, `input_size`).
        - **hx** (tuple) - A tuple of two Tensors (h_0, c_0) both of data type mindspore.float32 or
          mindspore.float16 and shape (num_directions * `num_layers`, batch_size, `hidden_size`).
          Data type of `hx` should be the same of `input`.

    Outputs:
        Tuple, a tuple constains (`output`, (`h_n`, `c_n`)).

        - **output** (Tensor) - Tensor of shape (seq_len, batch_size, num_directions * `hidden_size`).
        - **hx_n** (tuple) - A tuple of two Tensor (h_n, c_n) both of shape
          (num_directions * `num_layers`, batch_size, `hidden_size`).

    Examples:
        >>> class LstmNet(nn.Cell):
        >>>     def __init__(self, input_size, hidden_size, num_layers, has_bias, batch_first, bidirectional):
        >>>         super(LstmNet, self).__init__()
        >>>         self.lstm = nn.LSTM(input_size=input_size,
        >>>                             hidden_size=hidden_size,
        >>>                             num_layers=num_layers,
        >>>                             has_bias=has_bias,
        >>>                             batch_first=batch_first,
        >>>                             bidirectional=bidirectional,
        >>>                             dropout=0.0)
        >>>
        >>>     def construct(self, inp, h0, c0):
        >>>         return self.lstm(inp, (h0, c0))
        >>>
        >>> net = LstmNet(10, 12, 2, has_bias=True, batch_first=True, bidirectional=False)
        >>> input = Tensor(np.ones([3, 5, 10]).astype(np.float32))
        >>> h0 = Tensor(np.ones([1 * 2, 3, 12]).astype(np.float32))
        >>> c0 = Tensor(np.ones([1 * 2, 3, 12]).astype(np.float32))
        >>> output, (hn, cn) = net(input, h0, c0)
    """
    def __init__(self,
                 input_size,
                 hidden_size,
                 num_layers=1,
                 has_bias=True,
                 batch_first=False,
                 dropout=0,
                 bidirectional=False):
        super(LSTM, self).__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.has_bias = has_bias
        self.batch_first = validator.check_type("batch_first", batch_first, [bool])
        self.dropout = float(dropout)
        self.bidirectional = bidirectional

        if self.batch_first:
            self.transpose1 = P.Transpose()
            self.transpose2 = P.Transpose()
        self.lstm = P.LSTM(input_size=self.input_size,
                           hidden_size=self.hidden_size,
                           num_layers=self.num_layers,
                           has_bias=self.has_bias,
                           bidirectional=self.bidirectional,
                           dropout=self.dropout)

        num_directions = 2 if self.bidirectional else 1

        weight_size = 0
        gate_size = 4 * self.hidden_size
        for layer in range(self.num_layers):
            input_layer_size = self.input_size if layer == 0 else self.hidden_size * num_directions
            increment_size = gate_size * input_layer_size
            increment_size += gate_size * self.hidden_size
            if self.has_bias:
                increment_size += 2 * gate_size
            weight_size += increment_size * num_directions

        self.weight = Parameter(initializer(0.0, [weight_size, 1, 1]), name='weight')

        self.fill = P.Fill()
        self.shape = P.Shape()

    def construct(self, x, hx):
        if self.batch_first:
            x = self.transpose1(x, (1, 0, 2))
        h0, c0 = hx
        output, hn, cn, _ = self.lstm(x, h0, c0, self.weight)
        if self.batch_first:
            output = self.transpose2(output, (1, 0, 2))
        return (output, (hn, cn))
