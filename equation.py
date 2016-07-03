#The MIT License (MIT)
#
# Copyright (c) 2015
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


def prec(op, unary):
    """ Determines the precidence of each operator.

    Assigns a presedence to an op depending on BEDMAS rules and gives
    more presedence to unary type variables.

    Args:
        unary: Bool specifiying if this is a unary variable in fornt of this
               variable (for example: -1).
    Returns:
        integer which is the presedence of operator.
    Raises:
        None.
    """
    if unary:
        if op == '+' or op == '-':
            return 3
        return 0
    if op == '*' or op == '/':
        return 2
    if op == '+' or op == '-':
        return 1
    return 0


def calc1(op, val):
    """performs unary operation"""
    if op == '+':
        return val
    if op == '-':
        return -val


def calc2(op, L, R):
    """performs arithmetic on operands L,R"""
    if op == '+':
        return L+R
    if op == '-':
        return L-R
    if op == '*':
        return L*R
    if op == '/':
        return L/R


def is_operand(s):
    '''Checks if it's an operand defined in our prec function'''
    return s != '(' and s != ')' and not prec(s, 0) and not prec(s, 1)


def eval(E):
    """Evaluates a list in postfix(Reverse Polish) expression.

    Args:
        E: list of str, the expression parsed into its individuals components.
    Returns:
        An integer reprsenting the evaulated expression
    Raises:
        ArithmeticError: division by 0
    """
    E = ['('] + E + [')']
    print(E)
    ops = []
    vals = []
    for i in range(len(E)):
        if is_operand(E[i]):
            vals.append(int(E[i]))
            continue
        if E[i] == '(':
            ops.append(('(', False))
            continue
        if prec(E[i], 1) and (i == 0 or E[i-1] == '(' or prec(E[i-1], 0)):
            ops.append((E[i], True))
            continue
        while prec(ops[-1][0], ops[-1][1]) >= prec(E[i], 0):
            op = ops[-1][0]
            is_unary = ops[-1][1]
            ops.pop()
            if op == '(':
                break
            y = vals[-1]
            vals.pop()
            if is_unary:
                vals.append(calc1(op, y))
            else:
                x = vals[-1]
                vals.pop()
                vals.append(calc2(op, x, y))
        if E[i] != ')':
            ops.append((E[i], 0))
    return vals[-1]


def split_expr(s, delim=' \n\t\v\f\r'):
    """Split a string expression to tokens.

    Split a string expression to tokens, ignoring whitespace delimiters.
    A vector of tokens is a more flexible format since you can decide to
    parse the expression however you wish just by modifying this function.

    Args:
        s: string, the expression to be parsed into its individuals components.
    Returns:
        An integer reprsenting the evaulated expression
        example:
        >>> split_expr("1+(51*-100)")
        ["1","+","(","51","*","-","100",")"]

    Raises:
        OutofBoundsError: an empty string is given
    """
    ret = []
    acc = ''
    for i in range(len(s)):
        if s[i].isdigit():
            acc += s[i]
        else:
            if i > 0 and s[i-1].isdigit():
                ret.append(acc)
            acc = ''
            if s[i] in delim:
                continue
            ret.append(s[i])
    if s[len(s)-1].isdigit():
        ret.append(acc)
    return ret


def evaluate(s):
    """Evaluates an expression in infix notation"""
    return eval(split_expr(s))

if __name__ == "__main__":
    print(evaluate("1+1"))
    print(evaluate("1+(51 * -100)"))

T License (MIT)
#
# Copyright (c) 2015
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


def prec(op, unary):
    """ Determines the precidence of each operator.

    Assigns a presedence to an op depending on BEDMAS rules and gives
    more presedence to unary type variables.

    Args:
        unary: Bool specifiying if this is a unary variable in fornt of this
               variable (for example: -1).
    Returns:
        integer which is the presedence of operator.
    Raises:
        None.
    """
    if unary:
        if op == '+' or op == '-':
            return 3
        return 0
    if op == '*' or op == '/':
        return 2
    if op == '+' or op == '-':
        return 1
    return 0


def calc1(op, val):
    """performs unary operation"""
    if op == '+':
        return val
    if op == '-':
        return -val


def calc2(op, L, R):
    """performs arithmetic on operands L,R"""
    if op == '+':
        return L+R
    if op == '-':
        return L-R
    if op == '*':
        return L*R
    if op == '/':
        return L/R


def is_operand(s):
    '''Checks if it's an operand defined in our prec function'''
    return s != '(' and s != ')' and not prec(s, 0) and not prec(s, 1)


def eval(E):
    """Evaluates a list in postfix(Reverse Polish) expression.

    Args:
        E: list of str, the expression parsed into its individuals components.
    Returns:
        An integer reprsenting the evaulated expression
    Raises:
        ArithmeticError: division by 0
    """
    E = ['('] + E + [')']
    print(E)
    ops = []
    vals = []
    for i in range(len(E)):
        if is_operand(E[i]):
            vals.append(int(E[i]))
            continue
        if E[i] == '(':
            ops.append(('(', False))
            continue
        if prec(E[i], 1) and (i == 0 or E[i-1] == '(' or prec(E[i-1], 0)):
            ops.append((E[i], True))
            continue
        while prec(ops[-1][0], ops[-1][1]) >= prec(E[i], 0):
            op = ops[-1][0]
            is_unary = ops[-1][1]
            ops.pop()
            if op == '(':
                break
            y = vals[-1]
            vals.pop()
            if is_unary:
                vals.append(calc1(op, y))
            else:
                x = vals[-1]
                vals.pop()
                vals.append(calc2(op, x, y))
        if E[i] != ')':
            ops.append((E[i], 0))
    return vals[-1]


def split_expr(s, delim=' \n\t\v\f\r'):
    """Split a string expression to tokens.

    Split a string expression to tokens, ignoring whitespace delimiters.
    A vector of tokens is a more flexible format since you can decide to
    parse the expression however you wish just by modifying this function.

    Args:
        s: string, the expression to be parsed into its individuals components.
    Returns:
        An integer reprsenting the evaulated expression
        example:
        >>> split_expr("1+(51*-100)")
        ["1","+","(","51","*","-","100",")"]

    Raises:
        OutofBoundsError: an empty string is given
    """
    ret = []
    acc = ''
    for i in range(len(s)):
        if s[i].isdigit():
            acc += s[i]
        else:
            if i > 0 and s[i-1].isdigit():
                ret.append(acc)
            acc = ''
            if s[i] in delim:
                continue
            ret.append(s[i])
    if s[len(s)-1].isdigit():
        ret.append(acc)
    return ret


def evaluate(s):
    """Evaluates an expression in infix notation"""
    return eval(split_expr(s))

if __name__ == "__main__":
    print(evaluate("1+1"))
    print(evaluate("1+(51 * -100)"))

