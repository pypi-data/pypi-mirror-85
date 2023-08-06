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

"""tbe ops"""
from .adam_apply_one_with_decay import _adam_apply_one_with_decay_tbe
from .add import _add_tbe
from .add_n import _add_n_tbe
from .apply_momentum import _apply_momentum_tbe
from .apply_adam import _apply_adam_tbe
from .assign import _assign_tbe
from .assign_add import _assign_add_tbe
from .assign_sub import _assign_sub_tbe
from .batch_matmul import _batch_matmul_tbe
from .batchnorm import _batch_norm_tbe
from .batchnorm_grad import _batch_norm_grad_tbe
from .bias_add import _bias_add_tbe
from .bias_add_grad import _bias_add_grad_tbe
from .cast import _cast_tbe
from .conv2d import _conv2d_tbe
from .conv2d_backprop_filter import _conv2d_backprop_filter_tbe
from .conv2d_backprop_input import _conv2d_backprop_input_tbe
from .dropout_do_mask import _dropout_do_mask_tbe
from .gelu import _gelu_tbe
from .gelu_grad import _gelu_grad_tbe
from .max_pool import _max_pool_tbe
from .max_pool_grad import _max_pool_grad_tbe
from .max_pool_grad_with_argmax import _max_pool_grad_with_argmax_tbe
from .max_pool_with_argmax import _max_pool_with_argmax_tbe
from .mul import _mul_tbe
from .real_div import _real_div_tbe
from .relu import _relu_tbe
from .relu_grad import _relu_grad_tbe
from .softmax_cross_entropy_with_logits import _softmax_cross_entropy_with_logits_tbe
from .sigmoid_cross_entropy_with_logits import _sigmoid_cross_entropy_with_logits_tbe
from .sigmoid_cross_entropy_with_logits_grad import _sigmoid_cross_entropy_with_logits_grad_tbe
from .tensor_add import _tensor_add_tbe
from .trans_data import _trans_data_tbe
from .topkv2 import _topk_v2_tbe
from .matmul import _matmul_tbe
from .sub import _sub_tbe
from .reduce_mean_d import _reduce_mean_d_tbe
from .scatter_nd import _scatter_nd_tbe
from .scatter_nd_d import _scatter_nd_d_tbe
from .reduce_mean import _reduce_mean_tbe
from .reshape import _reshape_tbe
from .expand_dims import _expand_dims_tbe
from .squeeze import _squeeze_tbe
from .tile import _tile_tbe
from .atomic_addr_clean import _atomic_addr_clean_tbe
from .gather_v2 import _gather_v2_tbe
from .bn_training_reduce import _bn_training_reduce_tbe
from .bn_training_reduce_grad import _bn_training_reduce_grad_tbe
from .bn_training_update import _bn_training_update_tbe
from .bn_training_update_grad import _bn_training_update_grad_tbe
from .reciprocal import _reciprocal_tbe
from .strideslice_d import _strided_slice_d_tbe
from .strideslicegrad_d import _strided_slice_grad_d_tbe
from .split_d import _split_d_tbe
from .exp import _exp_tbe
from .div import _div_tbe
from .log import _log_tbe
from .floor_div import _floor_div_tbe
from .zeros_like import _zeros_like_tbe
from .neg import _neg_tbe
from .npu_clear_float_status import _npu_clear_float_status_tbe
from .npu_get_float_status import _npu_get_float_status_tbe
from .npu_alloc_float_status import _npu_alloc_float_status_tbe
from .one_hot import _one_hot_tbe
from .equal import _equal_tbe
from .less import _less_tbe
from .less_equal import _less_equal_tbe
from .logical_and import _logical_and_tbe
from .logical_not import _logical_not_tbe
from .logical_or import _logical_or_tbe
from .reduce_max import _reduce_max_tbe
from .reduce_sum import _reduce_sum_tbe
from .tanh import _tanh_tbe
from .tanh_grad import _tanh_grad_tbe
from .softmax import _softmax_tbe
from .square import _square_tbe
from .sqrt import _sqrt_tbe
from .transpose_d import _transpose_d_tbe
from .unsorted_segment_sum import _unsorted_segment_sum_tbe
from .logsoftmax_grad import _logsoftmax_grad_tbe
from .logsoftmax import _logsoftmax_tbe
from .select import _select_tbe
from .pow import _pow_tbe
from .maximum import _maximum_tbe
from .minimum import _minimum_tbe
from .minimum_grad import _minimum_grad_tbe
from .maximum_grad import _maximum_grad_tbe
from .concat import _concat_tbe
from .slice import _slice_tbe
from .greater import _greater_tbe
from .clip_by_norm_no_div_sum import _clip_by_norm_no_div_sum_tbe
from .clip_by_value import _clip_by_value_tbe
from .layer_norm_beta_gamma_backprop import _layer_norm_beta_gamma_backprop_tbe
from .layer_norm import _layer_norm_tbe
from .layer_norm_grad import _layer_norm_grad_tbe
from .layer_norm_x_backprop import _layer_norm_x_backprop_tbe
from .square_sum_v1 import _square_sum_v1_tbe
from .square_sum_v2 import _square_sum_v2_tbe
from .confusion_transpose_d import _confusion_transpose_d_tbe
from .confusion_softmax_grad import _confusion_softmax_grad_tbe
from .lamb_update_with_lr_v2 import _lamb_update_with_lr_v2_tbe
from .lamb_next_mv import _lamb_next_mv_tbe
from .lamb_next_mv_with_decay_v1 import _lamb_next_mv_with_decay_v1_tbe
from .lamb_update_with_lr import _lamb_update_with_lr_tbe
from .rsqrt import _rsqrt_tbe
from .sigmoid import _sigmoid_tbe
from .sigmoid_grad import _sigmoid_grad_tbe
from .resize_nearest_neighbor_d import _resize_nearest_neighbor_d_tbe
from .resize_nearest_neighbor_grad_d import _resize_nearest_neighbor_grad_d_tbe
from .pad_d import _pad_d_tbe
from .arg_max_with_value import _arg_max_with_value_tbe
from .arg_min_with_value import _arg_min_with_value_tbe
from .fused_mul_add import _fused_mul_add_tbe
from .fused_mul_add_n import _fused_mul_add_n_tbe
from .fused_mul_apply_momentum import _fused_mul_apply_momentum_tbe
