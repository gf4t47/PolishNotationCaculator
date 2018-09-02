import functools
from typing import Optional, Tuple

from src.operators import calc_op_map


def _build_nary_expression(number: int, enforce_bracket: Optional[bool])->[str]:
    with_bracket = [f'({number})']
    without_bracket = [str(number)]

    if enforce_bracket is True:
        return with_bracket
    elif enforce_bracket is False:
        return without_bracket
    else:
        return with_bracket + without_bracket


def _build_binary_expression(op: str, left: (int, str), right: (int, str), enforce_bracket: Optional[bool])->[str]:
    with_bracket = [f'({op} {left} {right})']
    without_bracket = [f'{op} {left} {right}']

    if enforce_bracket is True:
        return with_bracket
    elif enforce_bracket is False:
        return without_bracket
    else:
        return with_bracket + without_bracket


def _build_multiple_operands(op: str, operands: [(int, str)], enforce_bracket: Optional[bool])->[str]:
    expr = functools.reduce(lambda accu, it: accu + ' ' + str(it), operands, op)
    without_bracket = [expr]
    with_bracket = [f'({expr})']

    if enforce_bracket is True:
        return with_bracket
    elif enforce_bracket is False:
        return without_bracket
    else:
        return with_bracket + without_bracket


def unary_generator(inputs, enforce_bracket: Optional[bool])->[Tuple[str, int]]:
    result = []
    for it in inputs:
        result.extend([(expr, it) for expr in _build_nary_expression(it, enforce_bracket)])
    return result


def binary_generator(llist: [int], rlist: [int], op_key: str, enforce_bracket: Optional[bool])->[Tuple[str, int]]:
    result = []
    for left, right in [(l, r) for l in llist for r in rlist if op_key != '/' or r != 0]:
        calculated = calc_op_map[op_key](left, right)
        for expr in _build_binary_expression(op_key, left, right, enforce_bracket):
            result.append((expr, calculated))
    return result


def multiple_generator(operands: [int], op_key: str, enforce_bracket: Optional[bool])-> [Tuple[str, int]]:
    if len(operands) < 2:
        raise TypeError(f'Invalid test data: at least two operands for operator {op_key}')
    if op_key is '/' and any(it == 0 for it in operands[1::]):
        raise ValueError("Can't divide 0")

    calculated = functools.reduce(calc_op_map[op_key], operands)
    return [(expr, calculated) for expr in _build_multiple_operands(op_key, operands, enforce_bracket)]


def ternary_generator(llist: [int], rlist: [int], fst_op: str, sec_op: str, enforce_bracket: Optional[bool])->[Tuple[str, int]]:
    result = []
    for binary_expr, binary_calculated in binary_generator(llist, rlist, fst_op, enforce_bracket):
        for l in llist:
            if sec_op != '/' or binary_calculated != 0:
                calculated = calc_op_map[sec_op](l, binary_calculated)
                for expr in _build_binary_expression(sec_op, l, binary_expr, enforce_bracket):
                    result.append((expr, calculated))
        for r in rlist:
            if sec_op != '/' or r != 0:
                calculated = calc_op_map[sec_op](binary_calculated, r)
                for expr in _build_binary_expression(sec_op, binary_expr, r, enforce_bracket):
                    result.append((expr, calculated))
    return result


def binary_generator_all_op(llist: [int], rlist: [int], enforce_bracket: Optional[bool])->[Tuple[str, int]]:
    result = []
    for op in calc_op_map.keys():
        result.extend(binary_generator(llist, rlist, op, enforce_bracket))
    return result


def ternary_generator_all_op(llist: [int], rlist: [int], enforce_bracket: Optional[bool])->[Tuple[str, int]]:
    result = []
    for fst_op, sec_op in [(l, r) for l in calc_op_map.keys() for r in calc_op_map.keys()]:
        result.extend(ternary_generator(llist, rlist, fst_op, sec_op, enforce_bracket))
    return result


def multiple_generator_all_op(operands: [int], enforce_bracket: Optional[bool])->[Tuple[str, int]]:
    result = []
    for op in calc_op_map.keys():
        if op is not '/' or not any(it == 0 for it in operands[1::]):
            result.extend(multiple_generator(operands, op, enforce_bracket))
    return result
