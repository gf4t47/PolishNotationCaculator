from src.calculator import op_calc_map


def unary_generator(inputs):
    result = []
    for it in inputs:
        for expr in [f'{it}', f'0{it}', f'({it})', f'(00{it})']:
                result.append((expr, it))
    return result


def binary_generator(llist, rlist, op_key):
    result = []
    for left, right in [(l, r) for l in llist for r in rlist if op_key != '/' or r != 0]:
        calculated = op_calc_map[op_key](left, right)
        for expr in [f'{op_key} {left} {right}', f'{op_key} 00{left} {right}', f'({op_key} {left} {right})', f'({op_key} {left} 0{right})']:
            result.append((expr, calculated))
    return result


def ternary_generator(llist, rlist, fst_op, sec_op):
    result = []
    for binary_expr, binary_calculated in binary_generator(llist, rlist, fst_op):
        for l in llist:
            if sec_op != '/' or binary_calculated != 0:
                calculated = op_calc_map[sec_op](l, binary_calculated)
                for expr in [f'{sec_op} {l} {binary_expr}', f'{sec_op} {l} ({binary_expr})', f'({sec_op} {l} ({binary_expr}))']:
                    result.append((expr, calculated))
        for r in rlist:
            if sec_op != '/' or r != 0:
                calculated = op_calc_map[sec_op](binary_calculated, r)
                for expr in [f'{sec_op} {binary_expr} {r}', f'{sec_op} {binary_expr} ({r})', f'({sec_op} {binary_expr} ({r}))']:
                    result.append((expr, calculated))
    return result
