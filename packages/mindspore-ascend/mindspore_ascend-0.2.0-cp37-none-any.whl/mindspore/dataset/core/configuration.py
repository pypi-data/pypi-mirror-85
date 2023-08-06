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
The configuration manager.
"""

import mindspore._c_dataengine as cde

INT32_MAX = 2147483647
UINT32_MAX = 4294967295


class ConfigurationManager:
    """The configuration manager"""

    def __init__(self):
        self.config = cde.GlobalContext.config_manager()

    def set_seed(self, seed):
        """
        Set the seed to be used in any random generator. This is used to produce deterministic results.

        Args:
            seed(int): seed to be set

        Raises:
            ValueError: If seed is invalid (< 0 or > MAX_UINT_32).

        Examples:
            >>> import mindspore.dataset as ds
            >>> con = ds.engine.ConfigurationManager()
            >>> # sets the new seed value, now operators with a random seed will use new seed value.
            >>> con.set_seed(1000)
        """
        if seed < 0 or seed > UINT32_MAX:
            raise ValueError("Seed given is not within the required range")
        self.config.set_seed(seed)

    def get_seed(self):
        """
        Get the seed

        Returns:
            Int, seed.
        """
        return self.config.get_seed()

    def set_prefetch_size(self, size):
        """
        Set the number of rows to be prefetched.

        Args:
            size: total number of rows to be prefetched.

        Raises:
            ValueError: If prefetch_size is invalid (<= 0 or > MAX_INT_32).

        Examples:
            >>> import mindspore.dataset as ds
            >>> con = ds.engine.ConfigurationManager()
            >>> # sets the new prefetch value.
            >>> con.set_prefetch_size(1000)
        """
        if size <= 0 or size > INT32_MAX:
            raise ValueError("Prefetch size given is not within the required range")
        self.config.set_op_connector_size(size)

    def get_prefetch_size(self):
        """
        Get the prefetch size in number of rows.

        Returns:
            Size, total number of rows to be prefetched.
        """
        return self.config.get_op_connector_size()

    def set_num_parallel_workers(self, num):
        """
        Set the default number of parallel workers

        Args:
            num: number of parallel workers to be used as a default for each operation

        Raises:
            ValueError: If num_parallel_workers is invalid (<= 0 or > MAX_INT_32).

        Examples:
            >>> import mindspore.dataset as ds
            >>> con = ds.engine.ConfigurationManager()
            >>> # sets the new parallel_workers value, now parallel dataset operators will run with 8 workers.
            >>> con.set_num_parallel_workers(8)
        """
        if num <= 0 or num > INT32_MAX:
            raise ValueError("Num workers given is not within the required range")
        self.config.set_num_parallel_workers(num)

    def get_num_parallel_workers(self):
        """
        Get the default number of parallel workers.

        Returns:
            Int, number of parallel workers to be used as a default for each operation
        """
        return self.config.get_num_parallel_workers()

    def __str__(self):
        """
        String representation of the configurations.

        Returns:
            Str, configurations.
        """
        return str(self.config)

    def load(self, file):
        """
        Load configuration from a file.

        Args:
            file: path the config file to be loaded

        Raises:
            RuntimeError: If file is invalid and parsing fails.

        Examples:
            >>> import mindspore.dataset as ds
            >>> con = ds.engine.ConfigurationManager()
            >>> # sets the default value according to values in configuration file.
            >>> con.load("path/to/config/file")
            >>> # example config file:
            >>> # {
            >>> #     "logFilePath": "/tmp",
            >>> #     "rowsPerBuffer": 32,
            >>> #     "numParallelWorkers": 4,
            >>> #     "workerConnectorSize": 16,
            >>> #     "opConnectorSize": 16,
            >>> #     "seed": 5489
            >>> # }
        """
        self.config.load(file)


config = ConfigurationManager()
