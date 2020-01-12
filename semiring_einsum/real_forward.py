import torch

from .equation import Equation
from .extend import semiring_einsum_forward

def real_einsum_forward(
        equation: Equation,
        *args: torch.Tensor,
        block_size : int) -> torch.Tensor:
    r"""Einsum where addition and multiplication have their usual meanings.

    When dealing with summations over more than two input tensors at once,
    this can be even more memory efficient (if slower) than
    :py:func:`torch.einsum`.

    :param equation: A pre-compiled equation.
    :param args: Input tensors. The number of input tensors must be compatible
        with ``equation``.
    :return: Output of einsum.
    """
    return semiring_einsum_forward(equation, args, block_size, _callback)

def _callback(compute_sum):
    return compute_sum(_add_in_place, _sum_block, _multiply_in_place)

def _add_in_place(a, b):
    a.add_(b)

def _sum_block(a, dims):
    return torch.sum(a, dim=dims)

def _multiply_in_place(a, b):
    a.mul_(b)
