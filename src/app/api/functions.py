from fastapi import HTTPException

ops = {
    "+": (lambda a, b: a + b),
    "-": (lambda a, b: a - b),
    "*": (lambda a, b: a * b),
    "/": (lambda a, b: a / b),
}


def eval_polish_expr(expression: str):
    """
    Evaluate an polish inverted expression.

    Args:
        expression : str

    """
    tokens = expression.split()
    stack = []

    for token in tokens:
        if token in ops:
            arg2 = stack.pop()
            arg1 = stack.pop()
            result = ops[token](arg1, arg2)
            stack.append(result)
        else:
            try:
                stack.append(int(token))
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail="Error: only real numbers or %s." % ""
                    .join(ops.keys()),
                )

    return stack.pop()
