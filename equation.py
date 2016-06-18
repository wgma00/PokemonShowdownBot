# temp code take from rosettacode and interactivepython
from collections import namedtuple
from pprint import pprint as pp

OpInfo = namedtuple('OpInfo', 'prec assoc')
L, R = 'Left Right'.split()

ops = {
 '^': OpInfo(prec=4, assoc=R),
 '*': OpInfo(prec=3, assoc=L),
 '/': OpInfo(prec=3, assoc=L),
 '+': OpInfo(prec=2, assoc=L),
 '-': OpInfo(prec=2, assoc=L),
 '(': OpInfo(prec=9, assoc=L),
 ')': OpInfo(prec=0, assoc=L),
 }

NUM, LPAREN, RPAREN = 'NUMBER ( )'.split()


def get_input(inp):
    '''(str) -> [(TOKENTYPE, tokenvalue)]
       Inputs an expression and returns parsed list
    '''
    #inp = inp.replace(' ', '')
    tokens = inp.strip().split()
    tokenvals = []
    for token in tokens:
        if token in ops:
            tokenvals.append((token, ops[token]))
        elif token in (LPAREN, RPAREN):
            tokenvals.append((token, token))
        else:
            tokenvals.append((NUM, token))
    return tokenvals

def shunting(tokenvals):
    '''([(TOKENTYPE, tokenvalue)] -> str
        Turns the infix expression to a postfix expression
        Allows for parenthesis and unary operators
    '''
    outq, stack = [], []
    table = ['TOKEN,ACTION,RPN OUTPUT,OP STACK,NOTES'.split(',')]
    for token, val in tokenvals:
        note = action = ''
        if token is NUM:
            action = 'Add number to output'
            outq.append(val)
            table.append( (val, action, ' '.join(outq), ' '.join(s[0] for s in stack), note) )
        elif token in ops:
            t1, (p1, a1) = token, val
            v = t1
            note = 'Pop ops from stack to output'
            while stack:
                t2, (p2, a2) = stack[-1]
                if (a1 == L and p1 <= p2) or (a1 == R and p1 < p2):
                    if t1 != RPAREN:
                        if t2 != LPAREN:
                            stack.pop()
                            action = '(Pop op)'
                            outq.append(t2)
                        else:
                            break
                    else:
                        if t2 != LPAREN:
                            stack.pop()
                            action = '(Pop op)'
                            outq.append(t2)
                        else:
                            stack.pop()
                            action = '(Pop & discard "(")'
                            table.append( (v, action, ' '.join(outq), ' '.join(s[0] for s in stack), note) )
                            break
                    table.append( (v, action, ' '.join(outq), ' '.join(s[0] for s in stack), note) )
                    v = note = ''
                else:
                    note = ''
                    break
                note = ''
            note = ''
            if t1 != RPAREN:
                stack.append((token, val))
                action = 'Push op token to stack'
            else:
                action = 'Discard ")"'
            table.append( (v, action, ' '.join(outq), ' '.join(s[0] for s in stack), note) )
    note = 'Drain stack to output'
    while stack:
        v = ''
        t2, (p2, a2) = stack[-1]
        action = '(Pop op)'
        stack.pop()
        outq.append(t2)
        table.append( (v, action, ' '.join(outq), ' '.join(s[0] for s in stack), note) )
        v = note = ''
    return table


def postfixEval(postfixExpr):
    operandStack = []
    tokenList = postfixExpr.split()

    for token in tokenList:
        if token in "0123456789":
            operandStack.append(int(token))
        else:
            operand2 = operandStack.pop()
            operand1 = operandStack.pop()
            result = doMath(token,operand1,operand2)
            operandStack.append(result)
    return operandStack.pop()

def doMath(op, op1, op2):
    if op == "*":
        return op1 * op2
    elif op == "/":
        return op1 / op2
    elif op == "+":
        return op1 + op2
    else:
        return op1 - op2

if __name__ == '__main__':
    infix = '(1 + 2) + 3'
