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
"""
The context of mindspore, used to configure the current execution environment,
including execution mode, execution backend and other feature switches.
"""
import os
import time
import threading
from collections import namedtuple
from types import FunctionType
from mindspore import log as logger
from mindspore._c_expression import MSContext
from mindspore._checkparam import args_type_check
from mindspore.parallel._auto_parallel_context import _set_auto_parallel_context, _get_auto_parallel_context, \
    _reset_auto_parallel_context

__all__ = ['GRAPH_MODE', 'PYNATIVE_MODE', 'set_context', 'get_context', 'set_auto_parallel_context',
           'get_auto_parallel_context', 'reset_auto_parallel_context']

GRAPH_MODE = 0
PYNATIVE_MODE = 1
# The max memory size of graph plus variable.
_DEVICE_APP_MEMORY_SIZE = 31


def _make_directory(path):
    """Make directory."""
    real_path = None
    if path is None or not isinstance(path, str) or path.strip() == "":
        raise ValueError(f"Input path `{path}` is invalid type")

    # convert the relative paths
    path = os.path.realpath(path)
    logger.debug("The absolute path is %r", path)

    # check whether the path is already existed and has written permissions
    if os.path.exists(path):
        real_path = path
    else:
        # All exceptions need to be caught because create directory maybe have some limit(permissions)
        logger.debug("The directory(%s) doesn't exist, will create it", path)
        try:
            os.makedirs(path)
            real_path = path
        except PermissionError as e:
            logger.error(f"No write permission on the directory `{path}, error = {e}")
            raise ValueError(f"No write permission on the directory `{path}`.")
    return real_path


def _get_print_file_name(file_name):
    """Add timestamp suffix to file name. Rename the file name:  file_name + "." + time(seconds)."""
    time_second = str(int(time.time()))
    file_name = file_name + "." + time_second
    if os.path.exists(file_name):
        ValueError("This file {} already exists.".format(file_name))
    return file_name


class _ThreadLocalInfo(threading.local):
    """
    Thread local Info used for store thread local attributes.
    """

    def __init__(self):
        super(_ThreadLocalInfo, self).__init__()
        self._reserve_class_name_in_scope = True

    @property
    def reserve_class_name_in_scope(self):
        """Gets whether to save the network class name in the scope."""
        return self._reserve_class_name_in_scope

    @reserve_class_name_in_scope.setter
    def reserve_class_name_in_scope(self, reserve_class_name_in_scope):
        """Sets whether to save the network class name in the scope."""
        if not isinstance(reserve_class_name_in_scope, bool):
            raise ValueError(
                "Set reserve_class_name_in_scope value must be bool!")
        self._reserve_class_name_in_scope = reserve_class_name_in_scope


_ContextRecord = namedtuple(
    "_ContextRecord", ["is_pynative_mode", "switch_context_fn"])


class _ContextSwitchInfo(threading.local):
    """
    Record of context switch information.

    Args:
        is_pynative (bool): Whether to adopt the PyNative mode.
    """

    def __init__(self, is_pynative):
        super(_ContextSwitchInfo, self).__init__()
        self.context_stack = []
        if is_pynative:
            self.push(True, None)

    def push(self, is_pynative, switch_context_fn):
        """
        Push a context switch record onto the stack.

        Args:
            is_pynative (bool): Whether context switch to PyNative mode.
            switch_context_fn (Function): A callable that executes the context switch.
        """
        if isinstance(switch_context_fn, FunctionType):
            switch_context_fn()
        self.context_stack.append(
            _ContextRecord(is_pynative, switch_context_fn))

    def pop(self):
        self.context_stack.pop()


class _Context:
    """
    _Context is the environment in which operations are executed

    Note:
        Create a context through instantiating Context object is not recommended.
        should use context() to get the context since Context is singleton.
    """
    _instance = None
    _instance_lock = threading.Lock()

    def __init__(self):
        self._thread_local_info = _ThreadLocalInfo()
        self._context_switches = _ContextSwitchInfo(True)
        self._context_handle = MSContext.get_instance()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance_lock.acquire()
            cls._instance = object.__new__(cls)
            cls._instance_lock.release()
        return cls._instance

    def __getattribute__(self, attr):
        value = object.__getattribute__(self, attr)
        if attr == "_context_handle" and value is None:
            raise ValueError("Context handle is none in context!!!")
        return value

    @property
    def mode(self):
        return self._context_handle.get_execution_mode()

    @mode.setter
    def mode(self, mode):
        """
        Switch between Graph mode and PyNative mode.

        Args:
            mode (int): GRAPH_MODE or PYNATIVE_MODE.
        """
        self._context_handle.set_execution_mode(mode)
        if mode == PYNATIVE_MODE:
            if self.enable_debug_runtime:
                self.set_backend_policy("vm")
            self._context_switches.push(True, None)
        else:
            if self.enable_debug_runtime:
                self.set_backend_policy("ge")
            self._context_switches.push(False, None)

    def set_backend_policy(self, policy):
        success = self._context_handle.set_backend_policy(policy)
        if not success:
            raise RuntimeError("Backend policy must be one of ge, vm, ms.")

    @property
    def precompile_only(self):
        return self._context_handle.get_precompile_only()

    @precompile_only.setter
    def precompile_only(self, precompile_only):
        self._context_handle.set_precompile_only(precompile_only)

    @property
    def save_graphs(self):
        return self._context_handle.get_save_graphs_flag()

    @save_graphs.setter
    def save_graphs(self, save_graphs_flag):
        self._context_handle.set_save_graphs_flag(save_graphs_flag)

    @property
    def save_graphs_path(self):
        return self._context_handle.get_save_graphs_path()

    @save_graphs_path.setter
    def save_graphs_path(self, save_graphs_path):
        self._context_handle.set_save_graphs_path(
            _make_directory(save_graphs_path))

    @property
    def device_target(self):
        return self._context_handle.get_device_target()

    @device_target.setter
    def device_target(self, target):
        success = self._context_handle.set_device_target(target)
        if not success:
            raise ValueError("Target device name is invalid!!!")
        if self.enable_debug_runtime and self.device_target == "CPU":
            self.set_backend_policy("vm")

    @property
    def device_id(self):
        return self._context_handle.get_device_id()

    @device_id.setter
    def device_id(self, device_id):
        if device_id < 0 or device_id > 4095:
            raise ValueError(
                "Device id must be in [0, 4095], but got {}".format(device_id))
        success = self._context_handle.set_device_id(device_id)
        if not success:
            raise RuntimeError("Device id set failed!!!")

    @property
    def max_call_depth(self):
        return self._context_handle.get_max_call_depth()

    @max_call_depth.setter
    def max_call_depth(self, max_call_depth):
        if max_call_depth <= 0:
            raise ValueError(
                "Max call depth must be greater than 0, but got {}".format(max_call_depth))
        self._context_handle.set_max_call_depth(max_call_depth)

    @property
    def enable_auto_mixed_precision(self):
        return self._context_handle.get_auto_mixed_precision_flag()

    @enable_auto_mixed_precision.setter
    def enable_auto_mixed_precision(self, enable_auto_mixed_precision):
        self._context_handle.set_auto_mixed_precision_flag(
            enable_auto_mixed_precision)

    @property
    def enable_reduce_precision(self):
        return self._context_handle.get_enable_reduce_precision_flag()

    @enable_reduce_precision.setter
    def enable_reduce_precision(self, enable_reduce_precision):
        self._context_handle.set_enable_reduce_precision_flag(
            enable_reduce_precision)

    @property
    def enable_dump(self):
        return self._context_handle.get_enable_dump()

    @enable_dump.setter
    def enable_dump(self, enable_dump):
        self._context_handle.set_enable_dump(enable_dump)

    @property
    def save_dump_path(self):
        return self._context_handle.get_save_dump_path()

    @save_dump_path.setter
    def save_dump_path(self, save_dump_path):
        self._context_handle.set_save_dump_path(save_dump_path)

    @property
    def enable_profiling(self):
        return self._context_handle.get_enable_profiling()

    @enable_profiling.setter
    def enable_profiling(self, flag):
        self._context_handle.set_enable_profiling(flag)

    @property
    def profiling_options(self):
        return self._context_handle.get_profiling_options()

    @profiling_options.setter
    def profiling_options(self, option):
        options = ["training_trace", "task_trace",
                   "task_trace:training_trace", "training_trace:task_trace", "op_trace"]
        if option not in options:
            raise ValueError("Profiling options must be in 'training_trace' 'task_trace' "
                             "'task_trace:training_trace' 'training_trace:task_trace' or 'op_trace'.")
        self._context_handle.set_profiling_options(option)

    @property
    def enable_graph_kernel(self):
        return self._context_handle.get_enable_graph_kernel()

    @enable_graph_kernel.setter
    def enable_graph_kernel(self, graph_kernel_switch_):
        self._context_handle.set_enable_graph_kernel(graph_kernel_switch_)

    @property
    def reserve_class_name_in_scope(self):
        """Gets whether to save the network class name in the scope."""
        return self._thread_local_info.reserve_class_name_in_scope

    @reserve_class_name_in_scope.setter
    def reserve_class_name_in_scope(self, reserve_class_name_in_scope):
        """Sets whether to save the network class name in the scope."""
        self._thread_local_info.reserve_class_name_in_scope = reserve_class_name_in_scope

    @property
    def variable_memory_max_size(self):
        return None

    @variable_memory_max_size.setter
    def variable_memory_max_size(self, variable_memory_max_size):
        if not check_input_format(variable_memory_max_size):
            raise ValueError(
                "Context param variable_memory_max_size should be in correct format! Such as \"5GB\"")
        if int(variable_memory_max_size[:-2]) >= _DEVICE_APP_MEMORY_SIZE:
            raise ValueError(
                "Context param variable_memory_max_size should be less than 31GB.")
        variable_memory_max_size_ = variable_memory_max_size[:-
                                                             2] + " * 1024 * 1024 * 1024"
        graph_memory_max_size = _DEVICE_APP_MEMORY_SIZE - \
            int(variable_memory_max_size[:-2])
        graph_memory_max_size_ = str(
            graph_memory_max_size) + " * 1024 * 1024 * 1024"
        self._context_handle.set_variable_memory_max_size(
            variable_memory_max_size_)
        self._context_handle.set_graph_memory_max_size(graph_memory_max_size_)

    @property
    def enable_ge(self):
        return self._context_handle.get_backend_policy() == 'ge'

    @property
    def enable_debug_runtime(self):
        return self._thread_local_info.debug_runtime

    @enable_debug_runtime.setter
    def enable_debug_runtime(self, enable):
        thread_info = self._thread_local_info
        thread_info.debug_runtime = enable

    @property
    def check_bprop(self):
        return self._context_handle.get_check_bprop_flag()

    @check_bprop.setter
    def check_bprop(self, check_bprop_flag):
        self._context_handle.set_check_bprop_flag(check_bprop_flag)

    @property
    def max_device_memory(self):
        return self._context_handle.get_max_device_memory()

    @max_device_memory.setter
    def max_device_memory(self, max_device_memory):
        if not check_input_format(max_device_memory):
            raise ValueError("Context param max_device_memory should be in correct format! Such as \"3.5GB\"")
        max_device_memory_value = float(max_device_memory[:-2])
        if max_device_memory_value == 0:
            raise ValueError("Context param max_device_memory should be in correct format! Such as \"3.5GB\"")
        self._context_handle.set_max_device_memory(max_device_memory_value)

    @property
    def print_file_path(self):
        return None

    @print_file_path.setter
    def print_file_path(self, file_path):
        """Add timestamp suffix to file name. Sets print file path."""
        print_file_path = os.path.realpath(file_path)
        if os.path.isdir(print_file_path):
            raise IOError("Print_file_path should be file path, but got {}.".format(file_path))

        if os.path.exists(print_file_path):
            _path, _file_name = os.path.split(print_file_path)
            path = _make_directory(_path)
            file_name = _get_print_file_name(_file_name)
            full_file_name = os.path.join(path, file_name)
        else:
            full_file_name = print_file_path
        self._context_handle.set_print_file_path(full_file_name)

    @property
    def enable_sparse(self):
        return self._context_handle.get_enable_sparse()

    @enable_sparse.setter
    def enable_sparse(self, enable_sparse):
        self._context_handle.set_enable_sparse(enable_sparse)

def check_input_format(x):
    import re
    pattern = r'[1-9][0-9]*(\.)?[0-9]*GB|0\.[0-9]*GB'
    result = re.match(pattern, x)
    return result is not None


_k_context = None


def _context():
    """
    Get the global _context, if context is not created, create a new one.

    Returns:
        _Context, the global context in PyNative mode.
    """
    global _k_context
    if _k_context is None:
        default_backend = 'debug'
        try:
            from mindspore import default_config
            default_backend = default_config.__backend__
        except ImportError:
            logger.error("import default config fail")
        _k_context = _Context()
        _k_context.enable_debug_runtime = False
        if default_backend == 'debug':
            _k_context.enable_debug_runtime = True
            default_backend = 'vm'
        _k_context.set_backend_policy(default_backend)
    return _k_context


@args_type_check(device_num=int, global_rank=int, mirror_mean=bool, cast_before_mirror=bool, parallel_mode=str,
                 auto_parallel_search_mode=str, parameter_broadcast=bool, strategy_ckpt_load_file=str,
                 strategy_ckpt_save_file=str, full_batch=bool, enable_parallel_optimizer=bool)
def set_auto_parallel_context(**kwargs):
    """
    Set auto parallel context.

    Note:
        Attribute name is required for setting attributes.
        If a program has tasks with different parallel modes, then before setting new parallel mode for
        next task, interface mindspore.context.reset_auto_parallel_context() needs to be called to reset
        the configuration.
        Setting or changing parallel modes must be called before any Initializer created, or RuntimeError
        may be raised when compile network.

    Args:
        device_num (int): Available device number, the value must be in [1, 4096]. Default: 1.
        global_rank (int): Global rank id, the value must be in [0, 4095]. Default: 0.
        mirror_mean (bool): Whether to perform mean operator after all-reduce of mirror.
                     "stand_alone" do not support mirror_mean. Default: False.
        cast_before_mirror (bool): Insert Mirror Op after the cast if this flag is True.
                     "stand_alone", "data_parallel" and "hybrid_parallel" do not support
                     cast_before_mirror. Default: True.
        parallel_mode (str): There are five kinds of parallel modes, "stand_alone", "data_parallel",
                     "hybrid_parallel", "semi_auto_parallel" and "auto_parallel". Default: "stand_alone".

                     - stand_alone: Only one processor working.

                     - data_parallel: Distributing the data across different processors.

                     - hybrid_parallel: Achieving data parallelism and model parallelism manually.

                     - semi_auto_parallel: Achieving data parallelism and model parallelism by
                       setting parallel strategies.

                     - auto_parallel: Achieving parallelism automatically.
        auto_parallel_search_mode (str): There are two kinds of search modes, "recursive_programming"
                     and "dynamic_programming". Default: "dynamic_programming".

                     - recursive_programming: Recursive programming search mode.

                     - dynamic_programming: Dynamic programming search mode.
        parameter_broadcast (bool): Indicating whether to broadcast parameters before training.
                       "stand_alone", "semi_auto_parallel" and "auto_parallel" do not support parameter
                       broadcast. Default: False.
        strategy_ckpt_load_file (str): The path to load parallel strategy checkpoint. Default: ''
        strategy_ckpt_save_file (str): The path to save parallel strategy checkpoint. Default: ''
        full_batch (bool): Whether to load the whole batch on each device. Default: False.
        enable_parallel_optimizer(bool): This is a developing feature, which shards the weight update  computation in
                       data parallel training in the benefit of time and memory saving.
        max_call_depth(int): Specify the function call depth limit. Default: 1000.


    Raises:
        ValueError: If input key is not attribute in auto parallel context.

    Examples:
        >>> context.set_auto_parallel_context(device_num=8)
        >>> context.set_auto_parallel_context(global_rank=0)
        >>> context.set_auto_parallel_context(mirror_mean=True)
        >>> context.set_auto_parallel_context(cast_before_mirror=False)
        >>> context.set_auto_parallel_context(parallel_mode="auto_parallel")
        >>> context.set_auto_parallel_context(parameter_broadcast=False)
        >>> context.set_auto_parallel_context(strategy_ckpt_load_file="./strategy_stage1.ckpt")
        >>> context.set_auto_parallel_context(strategy_ckpt_save_file="./strategy_stage1.ckpt")
        >>> context.set_auto_parallel_context(max_call_depth=80)
    """
    _set_auto_parallel_context(**kwargs)


def get_auto_parallel_context(attr_key):
    """
    Gets auto parallel context attribute value according to the key.

    Args:
        attr_key (str): The key of the attribute.

    Returns:
        Returns attribute value according to the key.

    Raises:
        ValueError: If input key is not attribute in auto parallel context.
    """
    return _get_auto_parallel_context(attr_key)


def reset_auto_parallel_context():
    """
    Reset auto parallel context attributes to the default values:

    - device_num: 1.
    - global_rank: 0.
    - mirror_mean: False.
    - cast_before_mirror: True.
    - parallel_mode: "stand_alone".
    - parameter_broadcast: False.
    - strategy_ckpt_load_file: "".
    - strategy_ckpt_save_file: "".
    - enable_parallel_optimizer: False.
    """
    _reset_auto_parallel_context()


@args_type_check(mode=int, precompile_only=bool, device_target=str, device_id=int, save_graphs=bool,
                 save_graphs_path=str, enable_dump=bool,
                 save_dump_path=str, enable_reduce_precision=bool, variable_memory_max_size=str,
                 enable_profiling=bool, profiling_options=str, enable_auto_mixed_precision=bool,
                 enable_graph_kernel=bool, check_bprop=bool, max_device_memory=str, print_file_path=str,
                 enable_sparse=bool, max_call_depth=int)
def set_context(**kwargs):
    """
    Sets context for running environment.

    Context should be configured before running your program. If there is no configuration,
    the "Ascend" device target will be used by default. GRAPH_MODE or
    PYNATIVE_MODE can be set by `mode` attribute and both modes support all backends, default
    mode is PYNATIVE_MODE.

    When the `save_graphs` attribute is set to True, attribute of `save_graphs_path` is used to set the
    intermediate compilation graph storage path. By default, the graphs are saved in the current directory.
    As for other configurations and arguments, please refer to the corresponding module
    description, the configuration is optional and can be enabled when needed.

    Note:
        Attribute name is required for setting attributes.
        The mode is not recommended to be changed after net was initilized because the implementations of some
        operations are different in graph mode and pynative mode. Default: PYNATIVE_MODE.

    Args:
        mode (int): Running in GRAPH_MODE(0) or PYNATIVE_MODE(1).
        device_target (str): The target device to run, support "Ascend", "GPU", "CPU". Default: "Ascend".
        device_id (int): Id of target device, the value must be in [0, device_num_per_host-1],
                    while device_num_per_host should no more than 4096. Default: 0.
        save_graphs (bool): Whether to save graphs. Default: False.
        save_graphs_path (str): Path to save graphs. Default: "."
        enable_auto_mixed_precision (bool): Whether to enable auto mixed precision. Default: True.
        enable_graph_kernel (bool): Whether to enable composition of basic primitives. These primitives would be
            compiled into a fused kernel automatically. Default: False.
        reserve_class_name_in_scope (bool) : Whether to save the network class name in the scope. Default: True.
        enable_reduce_precision (bool): Whether to enable precision reduction. Default: True.
        enable_dump (bool): Whether to enable dump. Default: False.
        save_dump_path (str): When the program is executed on Ascend, operators can dump data here.
            The root dump path is configured in /home/HwHiAiUser/ide_daemon/ide_daemon.cfg.
            So the real dump path is "{configured root dump path}/{`save_dump_path`}". Default: ".".
        variable_memory_max_size (str): Sets variable memory max size. Default: "5GB".
        enable_profiling (bool): Whether to open profiling. Default: False.
        profiling_options (str): Sets profiling collection options, operators can profiling data here.
            Profiling collection options, the values are as follows, supporting the collection of multiple data.

            - training_trace: collect iterative trajectory data, that is, the training task and software information of
              the AI software stack, to achieve performance analysis of the training task, focusing on data
              enhancement, forward and backward calculation, gradient aggregation update and other related data.

            - task_trace: collect task trajectory data, that is, the hardware information of the HWTS/AICore of
              the Ascend 910 processor, and analyze the information of start and end of the task.

            - op_trace: collect single operator performance data.
            The profiling can choose training_trace, task_trace, training_trace and task_trace combination and
            separated by colons; single operator can choose op_trace, op_trace cannot be combined with
            training_trace and task_trace. Default: "training_trace".
        check_bprop (bool): Whether to check bprop. Default: False.
        max_device_memory (str): Sets the maximum memory available for device, currently only supported on GPU.
            The format is "xxGB". Default: "1024GB".
        print_file_path (str): The path of print data to save. If this parameter is set, print data is saved to
            a file by default, and turn off printing to the screen. If the file already exists, add a timestamp
            suffix to the file.
        enable_sparse (bool): Whether to enable sparsity feature. Default: False.

    Raises:
        ValueError: If input key is not an attribute in context.

    Examples:
        >>> context.set_context(mode=context.GRAPH_MODE)
        >>> context.set_context(mode=context.PYNATIVE_MODE)
        >>> context.set_context(device_target="Ascend")
        >>> context.set_context(device_id=0)
        >>> context.set_context(save_graphs=True, save_graphs_path="./model.ms")
        >>> context.set_context(enable_reduce_precision=True)
        >>> context.set_context(enable_dump=True, save_dump_path=".")
        >>> context.set_context(reserve_class_name_in_scope=True)
        >>> context.set_context(variable_memory_max_size="6GB")
        >>> context.set_context(mode=context.GRAPH_MODE,
        >>>                     device_target="Ascend",device_id=0, save_graphs=True,
        >>>                     save_graphs_path="/mindspore")
        >>> context.set_context(enable_profiling=True, profiling_options="training_trace")
        >>> context.set_context(max_device_memory="3.5GB")
        >>> context.set_context(print_file_path="print.pb")
    """
    for key, value in kwargs.items():
        if not hasattr(_context(), key):
            raise ValueError("Set context keyword %s is not recognized!" % key)
        setattr(_context(), key, value)


def get_context(attr_key):
    """
    Gets context attribute value according to the input key.

    Args:
        attr_key (str): The key of the attribute.

    Returns:
        Object, The value of given attribute key.

    Raises:
        ValueError: If input key is not an attribute in context.
    """
    if not hasattr(_context(), attr_key):
        raise ValueError(
            "Get context keyword %s is not recognized!" % attr_key)
    return getattr(_context(), attr_key)
