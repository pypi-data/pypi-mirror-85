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
"""
The module text.transforms is inheritted from _c_dataengine
which is implemented basing on icu4c and cppjieba in C++.
It's a high performance module to process nlp text.
Users can use Vocab to build their own dictionary,
use appropriate tokenizers to split sentences into different tokens,
and use Lookup to find the index of tokens in Vocab.

.. Note::
    Constructor's arguments for every class in this module must be saved into the
    class attributes (self.xxx) to support save() and load().

Examples:
    >>> import mindspore.dataset as ds
    >>> import mindspore.dataset.text as text
    >>> dataset_file = "path/to/text_file_path"
    >>> # sentences as line data saved in a file
    >>> dataset = ds.TextFileDataset(dataset_file, shuffle=False)
    >>> # tokenize sentence to unicode characters
    >>> tokenizer = text.UnicodeCharTokenizer()
    >>> # load vocabulary form list
    >>> vocab = text.Vocab.from_list(['深', '圳', '欢', '迎', '您'])
    >>> # lookup is an operation for mapping tokens to ids
    >>> lookup = text.Lookup(vocab)
    >>> dataset = dataset.map(operations=[tokenizer, lookup])
    >>> for i in dataset.create_dict_iterator():
    >>>     print(i)
    >>> # if text line in dataset_file is:
    >>> # 深圳欢迎您
    >>> # then the output will be:
    >>> # {'text': array([0, 1, 2, 3, 4], dtype=int32)}
"""
import os
import re
import platform
import numpy as np

import mindspore._c_dataengine as cde

from .utils import JiebaMode, NormalizeForm, to_str, SPieceTokenizerOutType, SPieceTokenizerLoadType
from .validators import check_lookup, check_jieba_add_dict, \
    check_jieba_add_word, check_jieba_init, check_with_offsets, check_unicode_script_tokenizer, \
    check_wordpiece_tokenizer, check_regex_tokenizer, check_basic_tokenizer, check_ngram, check_pair_truncate, \
    check_to_number, check_bert_tokenizer, check_python_tokenizer, check_slidingwindow
from ..core.datatypes import mstype_to_detype


class Lookup(cde.LookupOp):
    """
    Lookup operator that looks up a word to an id.

    Args:
        vocab(Vocab): a Vocab object.
        unknown_token(str, optional): word to use for lookup if the word being looked up is out of Vocabulary (oov).
            If unknown_token is oov, runtime error will be thrown (default=None).
    """

    @check_lookup
    def __init__(self, vocab, unknown_token=None):
        super().__init__(vocab, unknown_token)


class SlidingWindow(cde.SlidingWindowOp):
    """
    TensorOp to construct a tensor from data (only 1-D for now), where each element in the dimension axis
    is a slice of data starting at the corresponding position, with a specified width.

    Args:
        width (int): The width of the window. Must be an integer and greater than zero.
        axis (int, optional): The axis along which sliding window is computed (default=0).

    Examples:
        >>> # Data before
        >>> # |    col1     |
        >>> # +-------------+
        >>> # | [1,2,3,4,5] |
        >>> # +-------------+
        >>> data = data.map(operations=SlidingWindow(3, 0))
        >>> # Data after
        >>> # |     col1    |
        >>> # +-------------+
        >>> # |  [[1,2,3],  |
        >>> # |   [2,3,4],  |
        >>> # |   [3,4,5]]  |
        >>> # +--------------+
    """

    @check_slidingwindow
    def __init__(self, width, axis=0):
        super().__init__(width, axis)



class Ngram(cde.NgramOp):
    """
    TensorOp to generate n-gram from a 1-D string Tensor.

    Refer to https://en.wikipedia.org/wiki/N-gram#Examples for an overview of what n-gram is and how it works.

    Args:
        n (list[int]):  n in n-gram, n >= 1. n is a list of positive integers, for e.g. n=[4,3], The result
            would be a 4-gram followed by a 3-gram in the same tensor. If number of words is not enough to make up for
            a n-gram, an empty string would be returned. For e.g. 3 grams on ["mindspore","best"] would result in an
            empty string be produced.
        left_pad (tuple, optional): ("pad_token", pad_width). Padding performed on left side of the sequence. pad_width
            will be capped at n-1. left_pad=("_",2) would pad left side of the sequence with "__" (default=None).
        right_pad (tuple, optional): ("pad_token", pad_width). Padding performed on right side of the sequence.
            pad_width will be capped at n-1. right_pad=("-":2) would pad right side of the sequence with "--"
            (default=None).
        separator (str, optional): symbol used to join strings together. for e.g. if 2-gram the ["mindspore", "amazing"]
            with separator="-" the result would be ["mindspore-amazing"] (default=None, which means whitespace is
            used).
    """

    @check_ngram
    def __init__(self, n, left_pad=("", 0), right_pad=("", 0), separator=" "):
        super().__init__(n, left_pad[1], right_pad[1], left_pad[0], right_pad[0], separator)


DE_C_INTER_JIEBA_MODE = {
    JiebaMode.MIX: cde.JiebaMode.DE_JIEBA_MIX,
    JiebaMode.MP: cde.JiebaMode.DE_JIEBA_MP,
    JiebaMode.HMM: cde.JiebaMode.DE_JIEBA_HMM
}


class JiebaTokenizer(cde.JiebaTokenizerOp):
    """
    Tokenize Chinese string into words based on dictionary.

    Args:
        hmm_path (str): the dictionary file is used by  HMMSegment algorithm,
            the dictionary can be obtained on the official website of cppjieba.
        mp_path (str): the dictionary file is used by MPSegment algorithm,
            the dictionary can be obtained on the official website of cppjieba.
        mode (JiebaMode, optional): Valid values can be any of [JiebaMode.MP, JiebaMode.HMM,
            JiebaMode.MIX](default=JiebaMode.MIX).

            - JiebaMode.MP, tokenize with MPSegment algorithm.
            - JiebaMode.HMM, tokenize with Hiddel Markov Model Segment algorithm.
            - JiebaMode.MIX, tokenize with a mix of MPSegment and HMMSegment algorithm.
        with_offsets (bool, optional): If or not output offsets of tokens (default=False).

    Examples:
        >>> # If with_offsets=False, default output one column {["text", dtype=str]}
        >>> tokenizer_op = JiebaTokenizer(HMM_FILE, MP_FILE, mode=JiebaMode.MP, with_offsets=False)
        >>> data = data.map(operations=tokenizer_op)
        >>> # If with_offsets=False, then output three columns {["token", dtype=str], ["offsets_start", dtype=uint32],
        >>> #                                                   ["offsets_limit", dtype=uint32]}
        >>> tokenizer_op = JiebaTokenizer(HMM_FILE, MP_FILE, mode=JiebaMode.MP, with_offsets=True)
        >>> data = data.map(input_columns=["text"], output_columns=["token", "offsets_start", "offsets_limit"],
        >>>                 columns_order=["token", "offsets_start", "offsets_limit"], operations=tokenizer_op)
    """

    @check_jieba_init
    def __init__(self, hmm_path, mp_path, mode=JiebaMode.MIX, with_offsets=False):
        if not isinstance(mode, JiebaMode):
            raise TypeError("Wrong input type for mode, should be JiebaMode.")

        self.mode = mode
        self.__check_path__(hmm_path)
        self.__check_path__(mp_path)
        self.with_offsets = with_offsets
        super().__init__(hmm_path, mp_path,
                         DE_C_INTER_JIEBA_MODE[mode],
                         self.with_offsets)

    @check_jieba_add_word
    def add_word(self, word, freq=None):
        """
        Add user defined word to JiebaTokenizer's dictionary.

        Args:
            word (str): The word to be added to the JiebaTokenizer instance.
                The added word will not be written into the built-in dictionary on disk.
            freq (int, optional): The frequency of the word to be added, The higher the frequency,
                the better change the word will be tokenized(default=None, use default frequency).
        """

        if freq is None:
            super().add_word(word, 0)
        else:
            super().add_word(word, freq)

    @check_jieba_add_dict
    def add_dict(self, user_dict):
        """
        Add user defined word to JiebaTokenizer's dictionary.

        Args:
            user_dict (Union[str, dict]): Dictionary to be added, file path or Python dictionary,
                Python Dict format: {word1:freq1, word2:freq2,...}.
                Jieba dictionary format : word(required), freq(optional), such as:

                .. code-block::

                    word1 freq1
                    word2
                    word3 freq3
        """

        if isinstance(user_dict, str):
            self.__add_dict_py_file(user_dict)
        elif isinstance(user_dict, dict):
            for k, v in user_dict.items():
                self.add_word(k, v)
        else:
            raise ValueError("the type of user_dict must str or dict")

    def __add_dict_py_file(self, file_path):
        """Add user defined word by file"""
        words_list = self.__parser_file(file_path)
        for data in words_list:
            if data[1] is None:
                freq = 0
            else:
                freq = int(data[1])
            self.add_word(data[0], freq)

    def __parser_file(self, file_path):
        """parser user defined word by file"""
        if not os.path.exists(file_path):
            raise ValueError(
                "user dict file {} is not exist".format(file_path))
        real_file_path = os.path.realpath(file_path)
        file_dict = open(real_file_path)
        data_re = re.compile('^(.+?)( [0-9]+)?$', re.U)
        words_list = []
        for item in file_dict:
            data = item.strip()
            if not isinstance(data, str):
                data = self.__decode(data)
            words = data_re.match(data).groups()
            if len(words) != 2:
                raise ValueError(
                    "user dict file {} format error".format(real_file_path))
            words_list.append(words)
        file_dict.close()
        return words_list

    def __decode(self, data):
        """decode the dict file to utf8"""
        try:
            data = data.decode('utf-8')
        except UnicodeDecodeError:
            raise ValueError("user dict file must utf8")
        return data.lstrip('\ufeff')

    def __check_path__(self, model_path):
        """check model path"""
        if not os.path.exists(model_path):
            raise ValueError(
                " jieba mode file {} is not exist".format(model_path))


class UnicodeCharTokenizer(cde.UnicodeCharTokenizerOp):
    """
    Tokenize a scalar tensor of UTF-8 string to Unicode characters.

    Args:
        with_offsets (bool, optional): If or not output offsets of tokens (default=False).

    Examples:
        >>> # If with_offsets=False, default output one column {["text", dtype=str]}
        >>> tokenizer_op = text.UnicodeCharTokenizer()
        >>> dataset = dataset.map(operations=tokenizer_op)
        >>> # If with_offsets=False, then output three columns {["token", dtype=str], ["offsets_start", dtype=uint32],
        >>> #                                                   ["offsets_limit", dtype=uint32]}
        >>> tokenizer_op = text.UnicodeCharTokenizer(True)
        >>> data = data.map(input_columns=["text"], output_columns=["token", "offsets_start", "offsets_limit"],
        >>>                 columns_order=["token", "offsets_start", "offsets_limit"], operations=tokenizer_op)
    """

    @check_with_offsets
    def __init__(self, with_offsets=False):
        self.with_offsets = with_offsets
        super().__init__(self.with_offsets)


class WordpieceTokenizer(cde.WordpieceTokenizerOp):
    """
    Tokenize scalar token or 1-D tokens to 1-D subword tokens.

    Args:
        vocab (Vocab): a Vocab object.
        suffix_indicator (str, optional): Used to show that the subword is the last part of a word(default='##').
        max_bytes_per_token (int, optional): Tokens exceeding this length will not be further split(default=100).
        unknown_token (str, optional): When we can not found the token: if 'unknown_token' is empty string,
            return the token directly, else return 'unknown_token'(default='[UNK]').
        with_offsets (bool, optional): If or not output offsets of tokens (default=False).

    Examples:
        >>> # If with_offsets=False, default output one column {["text", dtype=str]}
        >>> tokenizer_op = text.WordpieceTokenizer(vocab=vocab, unknown_token=['UNK'],
        >>>                                       max_bytes_per_token=100, with_offsets=False)
        >>> dataset = dataset.map(operations=tokenizer_op)
        >>> # If with_offsets=False, then output three columns {["token", dtype=str], ["offsets_start", dtype=uint32],
        >>> #                                                   ["offsets_limit", dtype=uint32]}
        >>> tokenizer_op = text.WordpieceTokenizer(vocab=vocab, unknown_token=['UNK'],
        >>>                                       max_bytes_per_token=100, with_offsets=True)
        >>> data = data.map(input_columns=["text"], output_columns=["token", "offsets_start", "offsets_limit"],
        >>>                 columns_order=["token", "offsets_start", "offsets_limit"], operations=tokenizer_op)
    """

    @check_wordpiece_tokenizer
    def __init__(self, vocab, suffix_indicator='##', max_bytes_per_token=100,
                 unknown_token='[UNK]', with_offsets=False):
        self.vocab = vocab
        self.suffix_indicator = suffix_indicator
        self.max_bytes_per_token = max_bytes_per_token
        self.unknown_token = unknown_token
        self.with_offsets = with_offsets
        super().__init__(self.vocab, self.suffix_indicator, self.max_bytes_per_token,
                         self.unknown_token, self.with_offsets)


DE_C_INTER_SENTENCEPIECE_LOADTYPE = {
    SPieceTokenizerLoadType.FILE: cde.SPieceTokenizerLoadType.DE_SPIECE_TOKENIZER_LOAD_KFILE,
    SPieceTokenizerLoadType.MODEL: cde.SPieceTokenizerLoadType.DE_SPIECE_TOKENIZER_LOAD_KMODEL
}

DE_C_INTER_SENTENCEPIECE_OUTTYPE = {
    SPieceTokenizerOutType.STRING: cde.SPieceTokenizerOutType.DE_SPIECE_TOKENIZER_OUTTYPE_KString,
    SPieceTokenizerOutType.INT: cde.SPieceTokenizerOutType.DE_SPIECE_TOKENIZER_OUTTYPE_KINT
}


class SentencePieceTokenizer(cde.SentencePieceTokenizerOp):
    """
    Tokenize scalar token or 1-D tokens to tokens by sentencepiece.

    Args:
        mode(Union[str, SentencePieceVocab]): If the input parameter is a file, then it is of type string,
            if the input parameter is a SentencePieceVocab object, then it is of type SentencePieceVocab.
        out_type(Union[str, int]): The type of output.
    """

    def __init__(self, mode, out_type):
        self.out_type = out_type
        if isinstance(mode, str):
            model_path, model_filename = os.path.split(mode)
            super().__init__(model_path, model_filename,
                             DE_C_INTER_SENTENCEPIECE_LOADTYPE[SPieceTokenizerLoadType.FILE],
                             DE_C_INTER_SENTENCEPIECE_OUTTYPE[out_type])
        elif isinstance(mode, cde.SentencePieceVocab):
            super().__init__(mode, DE_C_INTER_SENTENCEPIECE_LOADTYPE[SPieceTokenizerLoadType.MODEL],
                             DE_C_INTER_SENTENCEPIECE_OUTTYPE[out_type])


if platform.system().lower() != 'windows':
    class WhitespaceTokenizer(cde.WhitespaceTokenizerOp):
        """
        Tokenize a scalar tensor of UTF-8 string on ICU defined whitespaces(such as: ' ', '\\\\t', '\\\\r', '\\\\n').

        Args:
            with_offsets (bool, optional): If or not output offsets of tokens (default=False).

        Examples:
            >>> # If with_offsets=False, default output one column {["text", dtype=str]}
            >>> tokenizer_op = text.WhitespaceTokenizer()
            >>> dataset = dataset.map(operations=tokenizer_op)
            >>> # If with_offsets=False, then output three columns {["token", dtype=str],
            >>> #                                                   ["offsets_start", dtype=uint32],
            >>> #                                                   ["offsets_limit", dtype=uint32]}
            >>> tokenizer_op = text.WhitespaceTokenizer(True)
            >>> data = data.map(input_columns=["text"], output_columns=["token", "offsets_start", "offsets_limit"],
            >>>                 columns_order=["token", "offsets_start", "offsets_limit"], operations=tokenizer_op)
        """

        @check_with_offsets
        def __init__(self, with_offsets=False):
            self.with_offsets = with_offsets
            super().__init__(self.with_offsets)


    class UnicodeScriptTokenizer(cde.UnicodeScriptTokenizerOp):
        """
        Tokenize a scalar tensor of UTF-8 string on Unicode script boundaries.

        Args:
            keep_whitespace (bool, optional): If or not emit whitespace tokens (default=False).
            with_offsets (bool, optional): If or not output offsets of tokens (default=False).

        Examples:
            >>> # If with_offsets=False, default output one column {["text", dtype=str]}
            >>> tokenizer_op = text.UnicodeScriptTokenizerOp(keep_whitespace=True, with_offsets=False)
            >>> dataset = dataset.map(operations=tokenizer_op)
            >>> # If with_offsets=False, then output three columns {["token", dtype=str],
            >>> #                                                   ["offsets_start", dtype=uint32],
            >>> #                                                   ["offsets_limit", dtype=uint32]}
            >>> tokenizer_op = text.UnicodeScriptTokenizerOp(keep_whitespace=True, with_offsets=True)
            >>> data = data.map(input_columns=["text"], output_columns=["token", "offsets_start", "offsets_limit"],
            >>>                 columns_order=["token", "offsets_start", "offsets_limit"], operations=tokenizer_op)
        """

        @check_unicode_script_tokenizer
        def __init__(self, keep_whitespace=False, with_offsets=False):
            self.keep_whitespace = keep_whitespace
            self.with_offsets = with_offsets
            super().__init__(self.keep_whitespace, self.with_offsets)


    class CaseFold(cde.CaseFoldOp):
        """
        Apply case fold operation on utf-8 string tensor.
        """


    DE_C_INTER_NORMALIZE_FORM = {
        NormalizeForm.NONE: cde.NormalizeForm.DE_NORMALIZE_NONE,
        NormalizeForm.NFC: cde.NormalizeForm.DE_NORMALIZE_NFC,
        NormalizeForm.NFKC: cde.NormalizeForm.DE_NORMALIZE_NFKC,
        NormalizeForm.NFD: cde.NormalizeForm.DE_NORMALIZE_NFD,
        NormalizeForm.NFKD: cde.NormalizeForm.DE_NORMALIZE_NFKD
    }


    class NormalizeUTF8(cde.NormalizeUTF8Op):
        """
        Apply normalize operation on utf-8 string tensor.

        Args:
            normalize_form (NormalizeForm, optional): Valid values can be any of [NormalizeForm.NONE,
                NormalizeForm.NFC, NormalizeForm.NFKC, NormalizeForm.NFD,
                NormalizeForm.NFKD](default=NormalizeForm.NFKC).
                And you can see http://unicode.org/reports/tr15/ for details.

                - NormalizeForm.NONE, do nothing for input string tensor.
                - NormalizeForm.NFC, normalize with Normalization Form C.
                - NormalizeForm.NFKC, normalize with Normalization Form KC.
                - NormalizeForm.NFD, normalize with Normalization Form D.
                - NormalizeForm.NFKD, normalize with Normalization Form KD.
        """

        def __init__(self, normalize_form=NormalizeForm.NFKC):
            if not isinstance(normalize_form, NormalizeForm):
                raise TypeError("Wrong input type for normalization_form, should be NormalizeForm.")

            self.normalize_form = DE_C_INTER_NORMALIZE_FORM[normalize_form]
            super().__init__(self.normalize_form)


    class RegexReplace(cde.RegexReplaceOp):
        """
        Replace utf-8 string tensor with 'replace' according to regular expression 'pattern'.

        See http://userguide.icu-project.org/strings/regexp for support regex pattern.

        Args:
            pattern(str): the regex expression patterns.
            replace(str): the string to replace matched element.
            replace_all(bool, optional): If False, only replace first matched element;
                if True, replace all matched elements(default=True).
        """

        def __init__(self, pattern, replace, replace_all=True):
            self.pattern = pattern
            self.replace = replace
            self.replace_all = replace_all
            super().__init__(self.pattern, self.replace, self.replace_all)


    class RegexTokenizer(cde.RegexTokenizerOp):
        """
        Tokenize a scalar tensor of UTF-8 string by regex expression pattern.

        See http://userguide.icu-project.org/strings/regexp for support regex pattern.

        Args:
            delim_pattern(str): The pattern of regex delimiters.
                The original string will be split by matched elements.
            keep_delim_pattern(str, optional): The string matched by 'delim_pattern' can be kept as a token
                if it can be matched by 'keep_delim_pattern'. And the default value is empty str(''),
                in this situation, delimiters will not kept as a output token(default='').
            with_offsets (bool, optional): If or not output offsets of tokens (default=False).

        Examples:
            >>> # If with_offsets=False, default output one column {["text", dtype=str]}
            >>> tokenizer_op = text.RegexTokenizer(delim_pattern, keep_delim_pattern, with_offsets=False)
            >>> dataset = dataset.map(operations=tokenizer_op)
            >>> # If with_offsets=False, then output three columns {["token", dtype=str],
            >>> #                                                   ["offsets_start", dtype=uint32],
            >>> #                                                   ["offsets_limit", dtype=uint32]}
            >>> tokenizer_op = text.RegexTokenizer(delim_pattern, keep_delim_pattern, with_offsets=True)
            >>> data = data.map(input_columns=["text"], output_columns=["token", "offsets_start", "offsets_limit"],
            >>>                 columns_order=["token", "offsets_start", "offsets_limit"], operations=tokenizer_op)
        """

        @check_regex_tokenizer
        def __init__(self, delim_pattern, keep_delim_pattern='', with_offsets=False):
            self.delim_pattern = delim_pattern
            self.keep_delim_pattern = keep_delim_pattern
            self.with_offsets = with_offsets
            super().__init__(self.delim_pattern, self.keep_delim_pattern, self.with_offsets)


    class BasicTokenizer(cde.BasicTokenizerOp):
        """
        Tokenize a scalar tensor of UTF-8 string by specific rules.

        Args:
            lower_case(bool, optional): If True, apply CaseFold, NormalizeUTF8(NFD mode), RegexReplace operation
                on input text to make the text to lower case and strip accents characters; If False, only apply
                NormalizeUTF8('normalization_form' mode) operation on input text(default=False).
            keep_whitespace(bool, optional): If True, the whitespace will be kept in out tokens(default=False).
            normalization_form(NormalizeForm, optional): Used to specify a specific normalize mode,
                only effective when 'lower_case' is False. See NormalizeUTF8 for details(default=NormalizeForm.NONE).
            preserve_unused_token(bool, optional): If True, do not split special tokens like
                '[CLS]', '[SEP]', '[UNK]', '[PAD]', '[MASK]'(default=True).
            with_offsets (bool, optional): If or not output offsets of tokens (default=False).

        Examples:
            >>> # If with_offsets=False, default output one column {["text", dtype=str]}
            >>> tokenizer_op = text.BasicTokenizer(lower_case=False,
            >>>                                   keep_whitespace=False,
            >>>                                   normalization_form=NormalizeForm.NONE,
            >>>                                   preserve_unused_token=True,
            >>>                                   with_offsets=False)
            >>> dataset = dataset.map(operations=tokenizer_op)
            >>> # If with_offsets=False, then output three columns {["token", dtype=str],
            >>> #                                                   ["offsets_start", dtype=uint32],
            >>> #                                                   ["offsets_limit", dtype=uint32]}
            >>> tokenizer_op = text.BasicTokenizer(lower_case=False,
            >>>                                   keep_whitespace=False,
            >>>                                   normalization_form=NormalizeForm.NONE,
            >>>                                   preserve_unused_token=True,
            >>>                                   with_offsets=True)
            >>> data = data.map(input_columns=["text"], output_columns=["token", "offsets_start", "offsets_limit"],
            >>>                 columns_order=["token", "offsets_start", "offsets_limit"], operations=tokenizer_op)
        """

        @check_basic_tokenizer
        def __init__(self, lower_case=False, keep_whitespace=False, normalization_form=NormalizeForm.NONE,
                     preserve_unused_token=True, with_offsets=False):
            if not isinstance(normalization_form, NormalizeForm):
                raise TypeError("Wrong input type for normalization_form, should be NormalizeForm.")

            self.lower_case = lower_case
            self.keep_whitespace = keep_whitespace
            self.normalization_form = DE_C_INTER_NORMALIZE_FORM[normalization_form]
            self.preserve_unused_token = preserve_unused_token
            self.with_offsets = with_offsets
            super().__init__(self.lower_case, self.keep_whitespace, self.normalization_form,
                             self.preserve_unused_token, self.with_offsets)


    class BertTokenizer(cde.BertTokenizerOp):
        """
        Tokenizer used for Bert text process.

        Args:
            vocab(Vocab): a Vocab object.
            suffix_indicator(str, optional): Used to show that the subword is the last part of a word(default='##').
            max_bytes_per_token(int, optional): Tokens exceeding this length will not be further split(default=100).
            unknown_token(str, optional): When we can not found the token: if 'unknown_token' is empty string,
                return the token directly, else return 'unknown_token'(default='[UNK]').
            lower_case(bool, optional): If True, apply CaseFold, NormalizeUTF8(NFD mode), RegexReplace operation
                on input text to make the text to lower case and strip accents characters; If False, only apply
                NormalizeUTF8('normalization_form' mode) operation on input text(default=False).
            keep_whitespace(bool, optional): If True, the whitespace will be kept in out tokens(default=False).
            normalization_form(NormalizeForm, optional): Used to specify a specific normlaize mode,
                only effective when 'lower_case' is False. See NormalizeUTF8 for details(default='NONE').
            preserve_unused_token(bool, optional): If True, do not split special tokens like
                '[CLS]', '[SEP]', '[UNK]', '[PAD]', '[MASK]'(default=True).
            with_offsets (bool, optional): If or not output offsets of tokens (default=False).

        Examples:
            >>> # If with_offsets=False, default output one column {["text", dtype=str]}
            >>> tokenizer_op = text.BertTokenizer(vocab=vocab, suffix_indicator='##', max_bytes_per_token=100,
            >>>                                  unknown_token=100, lower_case=False, keep_whitespace=False,
            >>>                                  normalization_form=NormalizeForm.NONE, preserve_unused_token=True,
            >>>                                  with_offsets=False)
            >>> dataset = dataset.map(operations=tokenizer_op)
            >>> # If with_offsets=False, then output three columns {["token", dtype=str],
            >>> #                                                   ["offsets_start", dtype=uint32],
            >>> #                                                   ["offsets_limit", dtype=uint32]}
            >>> tokenizer_op = text.BertTokenizer(vocab=vocab, suffix_indicator='##', max_bytes_per_token=100,
            >>>                                  unknown_token=100, lower_case=False, keep_whitespace=False,
            >>>                                  normalization_form=NormalizeForm.NONE, preserve_unused_token=True,
            >>>                                  with_offsets=True)
            >>> data = data.map(input_columns=["text"], output_columns=["token", "offsets_start", "offsets_limit"],
            >>>                 columns_order=["token", "offsets_start", "offsets_limit"], operations=tokenizer_op)
        """

        @check_bert_tokenizer
        def __init__(self, vocab, suffix_indicator='##', max_bytes_per_token=100, unknown_token='[UNK]',
                     lower_case=False, keep_whitespace=False, normalization_form=NormalizeForm.NONE,
                     preserve_unused_token=True, with_offsets=False):
            if not isinstance(normalization_form, NormalizeForm):
                raise TypeError("Wrong input type for normalization_form, should be NormalizeForm.")

            self.vocab = vocab
            self.suffix_indicator = suffix_indicator
            self.max_bytes_per_token = max_bytes_per_token
            self.unknown_token = unknown_token
            self.lower_case = lower_case
            self.keep_whitespace = keep_whitespace
            self.normalization_form = DE_C_INTER_NORMALIZE_FORM[normalization_form]
            self.preserve_unused_token = preserve_unused_token
            self.with_offsets = with_offsets
            super().__init__(self.vocab, self.suffix_indicator, self.max_bytes_per_token, self.unknown_token,
                             self.lower_case, self.keep_whitespace, self.normalization_form,
                             self.preserve_unused_token, self.with_offsets)


class TruncateSequencePair(cde.TruncateSequencePairOp):
    """
    Truncate a pair of rank-1 tensors such that the total length is less than max_length.

    This operation takes two input tensors and returns two output Tenors.

    Args:
        max_length(int): Maximum length required.

    Examples:
        >>> # Data before
        >>> # |  col1   |  col2   |
        >>> # +---------+---------|
        >>> # | [1,2,3] | [4,5]   |
        >>> # +---------+---------+
        >>> data = data.map(operations=TruncateSequencePair(4))
        >>> # Data after
        >>> # |  col1   |  col2   |
        >>> # +---------+---------+
        >>> # | [1,2]   | [4,5]   |
        >>> # +---------+---------+
    """

    @check_pair_truncate
    def __init__(self, max_length):
        super().__init__(max_length)


class ToNumber(cde.ToNumberOp):
    """
    Tensor operation to convert every element of a string tensor to a number.

    Strings are casted according to the rules specified in the following links:
    https://en.cppreference.com/w/cpp/string/basic_string/stof,
    https://en.cppreference.com/w/cpp/string/basic_string/stoul,
    except that any strings which represent negative numbers cannot be casted to an
    unsigned integer type.

    Args:
        data_type (mindspore.dtype): mindspore.dtype to be casted to. Must be
            a numeric type.

    Raises:
        RuntimeError: If strings are invalid to cast, or are out of range after being casted.
    """

    @check_to_number
    def __init__(self, data_type):
        data_type = mstype_to_detype(data_type)
        self.data_type = str(data_type)
        super().__init__(data_type)


class PythonTokenizer:
    """
    Callable class to be used for user-defined string tokenizer.
    Args:
        tokenizer (Callable): Python function that takes a `str` and returns a list of `str` as tokens.

    Examples:
        >>> def my_tokenizer(line):
        >>>     return line.split()
        >>> data = data.map(operations=PythonTokenizer(my_tokenizer))
    """

    @check_python_tokenizer
    def __init__(self, tokenizer):
        self.tokenizer = np.vectorize(lambda x: np.array(tokenizer(x), dtype='U'), signature='()->(n)')

    def __call__(self, in_array):
        in_array = to_str(in_array)
        tokens = self.tokenizer(in_array)
        return tokens
