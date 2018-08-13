from typing import Optional

from src.operators import calc_op_map


def _build_binary_expression(op: str, left: (int, str), right: (int, str), enforce_bracket: Optional[bool]):
    with_bracket = [f'({op} {left} {right})']
    without_bracket = [f'{op} {left} {right}']

    if enforce_bracket is True:
        return with_bracket
    elif enforce_bracket is False:
        return without_bracket
    else:
        return with_bracket + without_bracket


def unary_generator(inputs):
    result = []
    for it in inputs:
        for expr in [f'{it}', f'0{it}', f'({it})', f'(00{it})']:
                result.append((expr, it))
    return result


def binary_generator(llist: [int], rlist: [int], op_key: str, enforce_bracket: Optional[bool]):
    result = []
    for left, right in [(l, r) for l in llist for r in rlist if op_key != '/' or r != 0]:
        calculated = calc_op_map[op_key](left, right)
        for expr in _build_binary_expression(op_key, left, right, enforce_bracket):
            result.append((expr, calculated))
    return result


def ternary_generator(llist, rlist, fst_op, sec_op, enforce_bracket: Optional[bool]):
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


def ternary_generator_all_op(llist, rlist, enforce_bracket: Optional[bool]):
    result = []
    for fst_op, sec_op in [(l, r) for l in calc_op_map.keys() for r in calc_op_map.keys()]:
        result += ternary_generator(llist, rlist, fst_op, sec_op, enforce_bracket)
    return result
