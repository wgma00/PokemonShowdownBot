# This file is part of Alex's Anthology of Algorithms: Common Code 
# for Contests in Concise C++ (A3C5). It has been translated from its original
# C++ form to its current Python form.
# 
# A3C5 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# A3C5 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.

from fractions import Fraction

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
    if op == '^':
        return 4
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
    if op == '^':
        return L**R


def is_operand(s):
    '''Checks if it's an operand defined in our prec function'''
    return s != '(' and s != ')' and not prec(s, False) and not prec(s, True)


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
    ops = []
    vals = []
    print(E)
    for i in range(len(E)):

        if is_operand(E[i]):
            vals.append(Fraction(E[i]))
            continue

        if E[i] == '(':
            ops.append(('(', False))
            continue

        # This is a valid unary operator 
        if prec(E[i], True) and (i == 0 or E[i-1] == '(' or prec(E[i-1], False)):
            ops.append((E[i], True))
            continue

        while prec(ops[-1][0], ops[-1][1]) >= prec(E[i], False):
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
            print(vals[-1])
        if E[i] != ')':
            ops.append((E[i], 0))

    return float(vals[-1])


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
        # supports decimals and integers 
        if s[i].isdigit() or s[i] == '.':
            acc += s[i]
        else:
            if i > 0 and s[i-1].isdigit() or s[i-1] == '.':
                ret.append(Fraction(acc))
            acc = ''
            if s[i] in delim:
                continue
            ret.append(s[i])
    if s[len(s)-1].isdigit() or s[len(s)-1] == '.':
        ret.append(Fraction(acc))
    return ret


def evaluate(s):
    """Evaluates an expression in infix notation"""
    return eval(split_expr(s))

if __name__ == "__main__":
    print(evaluate("1.234 + 2.0"))
    print(evaluate("1/10"))
    # print(evaluate("1+1"))
    # print(evaluate("1+(51 * -100)"))
    # print(evaluate("(1/10) + (2/10)"))
    print(evaluate("((1/10) + (2/10) - (3/10))*1000000000000000000"))
    print(evaluate("(1/10) + (2/10) - (3/10)"))
    print(evaluate("-(1/10)^2"))

