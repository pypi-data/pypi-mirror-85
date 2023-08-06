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

"""Inner operators."""

from ..._checkparam import Rel
from ..._checkparam import Validator as validator
from ... import context
from ...common import dtype as mstype
from ..primitive import PrimitiveWithInfer, prim_attr_register
from ..operations.math_ops import _infer_shape_reduce


class StridedSliceAICPU(PrimitiveWithInfer):
    r"""

    Extracts a strided slice of a tensor.

    Given an input tensor, this operation inserts a dimension of length 1 at the dimension.
    This operation extracts a fragment of size (end-begin)/stride from the given
    'input_tensor'. Starting from the position specified by the begin, the fragment
    continues adding stride to the index until all dimensions are not less than end.

    Note:
        The stride may be negative value, which causes reverse slicing.
        The shape of `begin`, `end` and `strides` must be the same.

    Args:
        begin_mask (int): Starting index of the slice. Default: 0.
        end_mask (int): Ending index of the slice. Default: 0.
        ellipsis_mask (int): An int mask. Default: 0.
        new_axis_mask (int): An int mask. Default: 0.
        shrink_axis_mask (int): An int mask. Default: 0.
        Currently all the masks are not in used. Use default 0 only.

    Inputs:
        - **input_x** (Tensor) - The input Tensor.
        - **begin** (tuple[int]) - A tuple which represents the location where to start. Only
          constant value is allowed.
        - **end** (tuple[int]) - A tuple or which represents the maximum location where to stop.
          Only constant value is allowed.
        - **strides** (tuple[int]) - A tuple which represents the stride continuously added
          before reach the maximum location. Only constant value is allowed.

    Outputs:
        Tensor.
        Explain with the following example.
            - In the 0th dim, begin is 1, end is 2, and strides is 1,
              because :math:`1+1=2\geq2`, the interval is :math:`[1,2)`.
              Thus, return the element with :math:`index = 1` in 0th dim, i.e., [[3, 3, 3], [4, 4, 4]].
            - In the 1st dim, similarly, the interval is :math:`[0,1)`.
              Based on the return value of the 0th dim, return the element with :math:`index = 0`,
              i.e., [3, 3, 3].
            - In the 2nd dim, similarly, the interval is :math:`[0,3)`.
              Based on the return value of the 1st dim, return the element with :math:`index = 0,1,2`,
              i.e., [3, 3, 3].
            - Finally, the output is [3, 3, 3].

    Examples
        >>> input_x = Tensor([[[1, 1, 1], [2, 2, 2]], [[3, 3, 3], [4, 4, 4]],
        >>>                   [[5, 5, 5], [6, 6, 6]]], mindspore.float32)
        >>> slice = P.StridedSliceAICPU()
        >>> output = slice(input_x, (1, 0, 0), (2, 1, 3), (1, 1, 2))
        >>> output.shape
        (1, 1, 2)
        >>> output
        [[[3, 3]]]
    """

    @prim_attr_register
    def __init__(self,
                 begin_mask=0,
                 end_mask=0,
                 ellipsis_mask=0,
                 new_axis_mask=0,
                 shrink_axis_mask=0):
        """Initialize StrideSlice"""
        self.init_prim_io_names(inputs=['x', 'begin', 'end', 'strides'], outputs=['output'])
        validator.check_value_type('begin_mask', begin_mask, [int], self.name)
        validator.check_value_type('end_mask', end_mask, [int], self.name)
        validator.check_value_type('ellipsis_mask', ellipsis_mask, [int], self.name)
        validator.check_value_type('new_axis_mask', new_axis_mask, [int], self.name)
        validator.check_value_type('shrink_axis_mask', shrink_axis_mask, [int], self.name)

    def __infer__(self, x, begin, end, strides):
        begin_v, end_v, strides_v = begin['value'], end['value'], strides['value']
        validator.check_value_type("begin", begin_v, [tuple], self.name)
        validator.check_value_type("end", end_v, [tuple], self.name)
        validator.check_value_type("strides", strides_v, [tuple], self.name)

        x_shape = x['shape']
        x_shp_len = len(x_shape)
        if len(begin_v) != x_shp_len or len(end_v) != x_shp_len or len(strides_v) != x_shp_len:
            raise ValueError(f"For \'{self.name}\' the length of begin index{begin_v}, end index{end_v} and "
                             f"strides{strides_v} must be equal to the dims({x_shp_len}) of input.")

        ret_shape = []
        append_dimensions = []
        shrink_pos = bin(self.shrink_axis_mask)[::-1]
        new_pos = bin(self.new_axis_mask)[::-1]
        for i in range(x_shp_len):
            # After the integer is converted to binary, it is a str and the first two chars are the flag char '0b'
            if i < (len(new_pos) - 2) and new_pos[i] == '1':
                ret_shape.append(1)
                append_dimensions.append(x_shape[x_shp_len - 1 - len(append_dimensions)])
                continue
            if i < (len(shrink_pos) - 2) and shrink_pos[i] == '1':
                validator.check_integer(f'begin[{i}]', begin_v[i], -x_shape[i], Rel.GE, self.name)
                validator.check_integer(f'begin[{i}]', begin_v[i], x_shape[i], Rel.LT, self.name)
                continue

            begin_idx = begin_v[i]
            end_idx = end_v[i]
            strides_idx = strides_v[i]
            if self.begin_mask:
                begin_idx = 0
            if self.end_mask:
                end_idx = x_shape[i]
            validator.check_integer(f'begin[{i}]', begin_idx, x_shape[i], Rel.LE, self.name)
            validator.check_integer(f'end[{i}]', end_idx, x_shape[i], Rel.LE, self.name)
            validator.check_integer(f'strides[{i}]', strides_idx, 0, Rel.NE, self.name)
            if strides_idx > 0:
                # If sliced forward , end_idx >= begin_idx
                validator.check(f'begin[{i}]', begin_idx, f'end[{i}]', end_idx, Rel.LE)
                if begin_idx < 0 < end_idx:
                    # Turn negative begin_idx into positive values
                    begin_idx = x_shape[i] + begin_idx
                num_elems = (end_idx - begin_idx + strides_idx - 1) // strides_idx
            else:
                # If sliced backwards, end_idx <= begin_idx
                validator.check(f'begin[{i}]', begin_idx, f'end[{i}]', end_idx, Rel.GE)
                if end_idx < 0 < begin_idx:
                    # Turn negative end_idx into positive values
                    end_idx = x_shape[i] + end_idx
                num_elems = (end_idx - begin_idx + strides_idx + 1) // strides_idx

            ret_shape.append(num_elems)
        if append_dimensions:
            ret_shape += append_dimensions[::-1]
        return {'shape': ret_shape,
                'dtype': x['dtype'],
                'value': None}


class ExtractImagePatches(PrimitiveWithInfer):
    """
    Extracts patches from images.
    The input tensor must be a 4-D tensor and the data format is NHWC.

    Args:
        ksizes (Union[tuple[int], list[int]]): The size of sliding window, must be a tuple or a list of integers,
            and the format is [1, ksize_row, ksize_col, 1].
        strides (Union[tuple[int], list[int]]): Distance between the centers of the two consecutive patches,
            must be a tuple or list of int, and the format is [1, stride_row, stride_col, 1].
        rates (Union[tuple[int], list[int]]): In each extracted patch, the gap between the corresponding dimension
            pixel positions, must be a tuple or a list of integers, and the format is [1, rate_row, rate_col, 1].
        padding (str): The type of padding algorithm, is a string whose value is "same" or "valid",
            not case sensitive. Default: "valid".

            - same: Means that the patch can take the part beyond the original image, and this part is filled with 0.

            - valid: Means that the taken patch area must be completely covered in the original image.

    Inputs:
        - **input_x** (Tensor) - A 4-D tensor whose shape is [in_batch, in_row, in_col, in_depth] and
          data type is number.

    Outputs:
        Tensor, a 4-D tensor whose data type is same as 'input_x',
        and the shape is [out_batch, out_row, out_col, out_depth], the out_batch is the same as the in_batch.
    """

    @prim_attr_register
    def __init__(self, ksizes, strides, rates, padding="valid"):
        """init"""
        def _check_tuple_or_list(arg_name, arg_val, prim_name):
            validator.check_value_type(f"{arg_name}s", ksizes, [tuple, list], self.name)
            if len(arg_val) != 4 or arg_val[0] != 1 or arg_val[3] != 1:
                raise ValueError(f"For \'{prim_name}\' the format of {arg_name}s should be [1, {arg_name}_row, "
                                 f"{arg_name}_col, 1], but got {arg_val}.")
            if not isinstance(arg_val[1], int) or not isinstance(arg_val[2], int) or arg_val[1] < 1 or arg_val[2] < 1:
                raise ValueError(f"For '{prim_name}' the {arg_name}_row and {arg_name}_col in {arg_name}s should be an "
                                 f"positive integer number, but got {arg_name}_row is {arg_val[1]}, {arg_name}_col "
                                 f"is {arg_val[2]}")

        _check_tuple_or_list("ksize", ksizes, self.name)
        _check_tuple_or_list("stride", strides, self.name)
        _check_tuple_or_list("rate", rates, self.name)
        self.padding = validator.check_string('padding', padding.upper(), ['VALID', 'SAME'], self.name)
        self.add_prim_attr("padding", self.padding)
        self.add_prim_attr("io_format", "NHWC")
        self.is_ge = context.get_context("enable_ge")

    def infer_shape(self, input_x):
        """infer shape"""
        in_batch, in_depth, in_row, in_col = input_x
        if self.is_ge:
            in_batch, in_row, in_col, in_depth = input_x
        _, ksize_row, ksize_col, _ = self.ksizes
        _, stride_row, stride_col, _ = self.strides
        _, rate_row, rate_col, _ = self.rates
        if len(input_x) != 4:
            raise ValueError("The `input_x` should be a 4-D tensor, "
                             f"but got a {len(input_x)}-D tensor whose shape is {input_x}")

        out_batch = in_batch
        out_depth = ksize_row * ksize_col * in_depth

        if self.padding == "VALID":
            out_row = \
                (in_row - (ksize_row + (ksize_row - 1) * (rate_row - 1))) // stride_row + 1
            out_col = \
                (in_col - (ksize_col + (ksize_col - 1) * (rate_col - 1))) // stride_col + 1
        else:
            out_row = (in_row - 1) // stride_row + 1
            out_col = (in_col - 1) // stride_col + 1

        out_shape = [out_batch, out_depth, out_row, out_col]
        if self.is_ge:
            out_shape = [out_batch, out_row, out_col, out_depth]
        return out_shape

    def infer_dtype(self, input_x):
        """infer dtype"""
        validator.check_tensor_type_same({"input_x": input_x}, mstype.number_type, self.name)
        return input_x


class Range(PrimitiveWithInfer):
    r"""
    Creates a sequence of numbers.
    Set `input_x` as :math:`x_i` for each element, `output` as follows:

    .. math::
        \text{output}(x_i) = x_i * \text{delta} + \text{start}

    Args:
        start (float): If `limit` is `None`, the value acts as limit in the range and first entry
            defaults to `0`. Otherwise, it acts as first entry in the range.
        limit (float): Acts as upper limit of sequence. If `None`, defaults to the value of `start`
            while set the first entry of the range to `0`. It can not be equal to `start`.
        delta (float): Increment of the range. It can not be equal to zero. Default: 1.0.

    Inputs:
        - **input_x** (Tensor) - The assistant data. A `1-D` tensor of type float32 or int32.

    Outputs:
        Tensor, has the same shape and dtype as `input_x`.

    Examples:
        >>> range = P.Range(1.0, 8.0, 2.0)
        >>> x = Tensor(np.array([1, 2, 3, 2]), mindspore.int32)
        >>> range(x)
        [3, 5, 7, 5]
    """

    @prim_attr_register
    def __init__(self, start, limit=None, delta=1.0):
        self.init_prim_io_names(inputs=['x'], outputs=['y'])
        self.delta = validator.check_value_type("delta", delta, [float], self.name)
        validator.check_value_type("start", start, [float], self.name)
        if limit is None:
            self.start = 0.0
            self.limit = start
            self.add_prim_attr("start", self.start)
            self.add_prim_attr("limit", self.limit)
        else:
            validator.check_value_type("limit", limit, [float], self.name)
        validator.check('start', self.start, 'limit', self.limit, Rel.NE, self.name)
        if self.delta == 0.0:
            raise ValueError("The input of `delta` can not be equal to zero.")
        if self.delta > 0.0 and self.start > self.limit:
            raise ValueError(f"Limit should be greater than start when delta:{self.delta} is more than zero, "
                             f"but got start:{self.start}, limit:{self.limit}")
        if self.delta < 0.0 and self.start < self.limit:
            raise ValueError(f"Start should be greater than limit when delta:{self.delta} is less than zero, "
                             f"but got start:{self.start}, limit:{self.limit}")

    def infer_shape(self, x_shape):
        return x_shape

    def infer_dtype(self, x_dtype):
        validator.check_tensor_type_same({'x_dtype': x_dtype}, [mstype.float32, mstype.int32], self.name)
        return x_dtype


class Quant(PrimitiveWithInfer):
    r"""
    Returns the quantized value of input_x.

    If `sqrt_mode` is False:

    .. math::
        y = round(scale * x + offset)

    If `sqrt_mode` is True:

    .. math::
        y = round(scale * x * scale + offset)

    Note:
        This operation only support Ascend 310 inference environment.

    Args:
        scale (float) : Specifies the scaling ratio.
        offset (float): Specifies the offset.
        sqrt_mode (bool) : Specifies whether to perform square root on `scale`. Default: False.
        round_mode (str): Specifies the way to round. Must be one of ["Round", "Floor", "Ceil", "Trunc"].
          Default: "Round".

    Inputs:
        - **input_x** (Tensor) : Input tensor. Its data type must be mindspore.float16 or mindspore.float32.

    Outputs:
        - Tensor: The quantized output tensor of type mindspore.int8.

    Examples:
        >>> input_x = Tensor([100.0, 150.0], mstype.float32)
        >>> quant = P.Quant(80.0, 0.0, False, "Round")
        >>> y = quant(input_x)
    """

    @prim_attr_register
    def __init__(self, scale, offset, sqrt_mode=False, round_mode="Round"):
        self.scale = validator.check_value_type("scale", scale, [float], self.name)
        self.offset = validator.check_value_type("offset", offset, [float], self.name)
        self.sqrt_mode = validator.check_value_type("sqrt_mode", sqrt_mode, [bool], self.name)
        self.round_mode = validator.check_string("round_mode", round_mode,
                                                 ["Round", "Floor", "Ceil", "Trunc"], self.name)
        self.add_prim_attr("io_format", "ND")

    def infer_shape(self, x_shape):
        return x_shape

    def infer_dtype(self, x_type):
        validator.check_subclass("input_x", x_type, mstype.tensor, self.name)
        validator.check_type_name("input_x", x_type, [mstype.float16, mstype.float32], self.name)
        return mstype.int8


class Dequant(PrimitiveWithInfer):
    r"""
    Returns the dequantized value of input_x.
    This operation will do ReLU to the dequantized value if `relu_flag` is True.

    If `sqrt_mode` is False:

    .. math::
        y = x * deq\_scale

    If `sqrt_mode` is True:

    .. math::
        y = x * deq\_scale * deq\_scale

    Note:
        This operation only support Ascend 310 inference environment.

    Args:
        sqrt_mode (bool) : Specifies whether to perform square root on `scale`. Default: False.
        relu_flag (bool): Specifies whether to perform ReLU. Default: False.

    Inputs:
        - **input_x** (Tensor) : Input tensor. Must be mindspore.int32.
        - **deq_scale** (Tensor) : Specifies the scaling ratio.
          Data type must be mindspore.float16 or mindspore.uint64

    Outputs:
        - Tensor: The quantized output tensor of type mindspore.float16.

    Examples:
        >>> input_x = Tensor([100.0, 150.0], mstype.float32)
        >>> dequant = P.Dequant(False, False)
        >>> y = dequant(input_x)
    """
    @prim_attr_register
    def __init__(self, sqrt_mode=False, relu_flag=False):
        self.sqrt_mode = validator.check_value_type("sqrt_mode", sqrt_mode, [bool], self.name)
        self.relu_flag = validator.check_value_type("relu_flag", relu_flag, [bool], self.name)
        self.add_prim_attr("dtype", mstype.float16)
        self.add_prim_attr("io_format", "ND")

    def infer_shape(self, x_shape, deq_scale_shape):
        return x_shape

    def infer_dtype(self, x_type, deq_scale_type):
        validator.check_subclass("x", x_type, mstype.tensor, self.name)
        validator.check_type_name("x", x_type, [mstype.int32], self.name)
        validator.check_type_name("deq_scale", deq_scale_type, [mstype.float16, mstype.uint64], self.name)
        return mstype.float16


class LinSpace(PrimitiveWithInfer):
    r"""
    Generates values in an interval. And return the corresponding interpolation accroding to assist.

    Inputs:
        - **assist** (Tensor[float32]) - The assist value, With shape of 0-D or 1-D.
        - **start** (Tensor[float32]) - The start of interval, With shape of 0-D.
        - **stop** (Tensor[float32]) - The end of interval, With shape of 0-D.
        - **num** (Tensor[int32]) - ticks number in the interval, the ticks include start and stop value.
          With shape of 0-D.

    Outputs:
        Tensor, has the same shape as `assist`.

    Examples:
        >>> linspace = P.LinSpace()
        >>> assist = Tensor([5, 5.5], mindspore.float32)
        >>> start = Tensor(1, mindspore.float32)
        >>> stop = Tensor(10, mindspore.float32)
        >>> num = Tensor(5, mindspore.int32)
        >>> output = linspace(assist, start, stop, num)
        [12.25, 13.375]
    """

    @prim_attr_register
    def __init__(self):
        pass

    def infer_shape(self, assist, start, stop, num):
        return assist

    def infer_dtype(self, assist, start, stop, num):
        args = {"num": num}
        validator.check_tensor_type_same(args, (mstype.int32,), self.name)
        args = {"assist": assist, "start": start, "stop": stop}
        validator.check_tensor_type_same(args, (mstype.float32,), self.name)
        return assist


class MatrixDiag(PrimitiveWithInfer):
    """
    Returns a batched diagonal tensor with a given batched diagonal values.

    Inputs:
        - **x** (Tensor) - A tensor which to be element-wise multi by `assist`. It can be one of the following data
          types: float32, float16, int32, int8, and uint8.
        - **assist** (Tensor) - A eye tensor of the same type as `x`. It's rank must greater than or equal to 2 and
          it's last dimension must equal to the second to last dimension.

    Outputs:
        Tensor, has the same type and shape as input `assist`.

    Examples:
        >>> x = Tensor(np.array([1, -1]), mstype.float32)
        >>> assist = Tensor(np.arange(-12, 0).reshape(3, 2, 2), mindspore.float32)
        >>> matrix_diag = P.MatrixDiag()
        >>> result = matrix_diag(x, assist)
        [[[-12.   11.]
          [-10.    9.]]
         [[ -8.    7.]
          [ -6.    5.]]
         [[ -4.    3.]
          [ -2.    1.]]]
    """

    @prim_attr_register
    def __init__(self):
        """Initialize MatrixDiag"""

    def infer_dtype(self, x_dtype, assist_dtype):
        valid_type = [mstype.float16, mstype.float32, mstype.int32, mstype.int8, mstype.uint8]
        args = {"x": x_dtype, "assist": assist_dtype}
        validator.check_tensor_type_same(args, valid_type, self.name)
        return x_dtype

    def infer_shape(self, x_shape, assist_shape):
        validator.check_integer("assist rank", len(assist_shape), 2, Rel.GE, self.name)
        validator.check('rank of x', len(x_shape)+1,
                        'rank of assist', len(assist_shape), Rel.LE, self.name)
        validator.check('assist\'s penultimate dimension', assist_shape[-2], 'assist\'s last dimension',
                        assist_shape[-1], Rel.EQ, self.name)

        r_end_dim = -len(x_shape)
        r_idx = -1
        while r_idx >= r_end_dim:
            if x_shape[r_idx] != 1:
                validator.check("reverse x dim %d" % r_idx, x_shape[r_idx], "reverse assist dim %d" %
                                assist_shape[r_idx-1], assist_shape[r_idx-1], Rel.EQ, self.name)
            r_idx = r_idx - 1

        return assist_shape


class MatrixDiagPart(PrimitiveWithInfer):
    r"""
    Returns the batched diagonal part of a batched tensor.

    Inputs:
        - **x** (Tensor) - The batched tensor. It can be one of the following data types:
          float32, float16, int32, int8, uint8.
        - **assist** (Tensor) - A eye tensor of the same type as `x`. With shape same as `x`.

    Outputs:
        Tensor, data type same as input `x`. The shape must be x.shape[:-2] + [min(x.shape[-2:])].

    Examples:
        >>> x = Tensor([[[-1, 0], [0, 1]], [[-1, 0], [0, 1]], [[-1, 0], [0, 1]]], mindspore.float32)
        >>> assist = Tensor(np.arange(-12, 0).reshape(3, 2, 2), mindspore.float32)
        >>> matrix_diag_part = P.MatrixDiagPart()
        >>> result = matrix_diag_part(x, assist)
        [[12., -9.], [8., -5.], [4., -1.]]
    """

    @prim_attr_register
    def __init__(self):
        """Initialize MatrixDiagPart"""

    def infer_dtype(self, x_dtype, assist_dtype):
        valid_type = [mstype.float16, mstype.float32, mstype.int32, mstype.int8, mstype.uint8]
        args = {"x": x_dtype, "assist": assist_dtype}
        validator.check_tensor_type_same(args, valid_type, self.name)
        return x_dtype

    def infer_shape(self, x_shape, assist_shape):
        validator.check_integer("x rank", len(x_shape), 2, Rel.GE, self.name)
        validator.check("x shape", x_shape, "assist shape", assist_shape, Rel.EQ, self.name)

        if assist_shape[-2] < assist_shape[-1]:
            out_shape = assist_shape[:-1]
        else:
            out_shape = assist_shape[:-2] + assist_shape[-1:]
        return out_shape


class MatrixSetDiag(PrimitiveWithInfer):
    r"""
    Modifies the batched diagonal part of a batched tensor.

    Inputs:
        - **x** (Tensor) - The batched tensor. It can be one of the following data types:
          float32, float16, int32, int8, uint8.
        - **assist** (Tensor) - A eye tensor of the same type as `x`. With shape same as `x`.
        - **diagonal** (Tensor) - The diagonal values.

    Outputs:
        Tensor, data type same as input `x`. The shape same as `x`.

    Examples:
        >>> x = Tensor([[[-1, 0], [0, 1]], [[-1, 0], [0, 1]], [[-1, 0], [0, 1]]], mindspore.float32)
        >>> diagonal = Tensor([[-1., 2.], [-1., 1.], [-1., 1.]], mindspore.float32)
        >>> matrix_set_diag = P.MatrixSetDiag()
        >>> result = matrix_set_diag(x, diagonal)
        [[[-1, 0], [0, 2]], [[-1, 0], [0, 1]], [[-1, 0], [0, 1]]]

    """

    @prim_attr_register
    def __init__(self):
        """Initialize MatrixSetDiag"""

    def infer_dtype(self, x_dtype, diagonal_dtype, assist_dtype):
        valid_type = [mstype.float16, mstype.float32, mstype.int32, mstype.int8, mstype.uint8]
        args = {"x": x_dtype, "diagonal": diagonal_dtype, "assist": assist_dtype}
        validator.check_tensor_type_same(args, valid_type, self.name)
        return x_dtype

    def infer_shape(self, x_shape, diagonal_shape, assist_shape):
        validator.check_integer("x rank", len(x_shape), 2, Rel.GE, self.name)
        validator.check("x shape", x_shape, "assist shape", assist_shape, Rel.EQ, self.name)

        if x_shape[-2] < x_shape[-1]:
            validator.check("diagnoal shape", diagonal_shape, "x shape excluding the last dimension",
                            x_shape[:-1], Rel.EQ, self.name)
        else:
            validator.check("diagonal shape", diagonal_shape, "x shape excluding the second last dimension",
                            x_shape[:-2] + x_shape[-1:], Rel.EQ, self.name)

        return assist_shape


class ConfusionMulGrad(PrimitiveWithInfer):
    """
    `output0` is the dot product result of input0 and input1.

    `output1` is the dot product result of input0 and input1, then apply the reducesum operation on it.

    Args:
        axis (Union[int, tuple[int], list[int]]): The dimensions to reduce.
            Default:(), reduce all dimensions. Only constant value is allowed.
        keep_dims (bool):
            - If true, keep these reduced dimensions and the length as 1.
            - If false, don't keep these dimensions. Default:False.

    Inputs:
        - **input_0** (Tensor) - The input Tensor.
        - **input_1** (Tensor) - The input Tensor.
        - **input_2** (Tensor) - The input Tensor.

    Outputs:
        - **output_0** (Tensor) - The same shape as `input0`.
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
