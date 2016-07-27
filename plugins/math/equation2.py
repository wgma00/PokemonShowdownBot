# The MIT License (MIT)
#
# Copyright (c) 2016 William Granados
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

import math
import parser

UNARY_OPS = {'sin': 'math.sin', 'cos':'math.cos', 'tan':'math.tan', 
             'log': 'math.log', 'sqrt':'math.sqrt'}

MATH_CONST = {'pi': 'math.pi', 'e':'math.e'}

def evaluation(eqn, x=""):
    """Evaluates an equation that follows proper python syntax.

    Args:
        eqn: string, equation to be parsed.
    Returns:
        Number representing the result of this solving this equation.
    Raises:
        None.
    """
    # Replace keywords with proper library functions
    for key in UNARY_OPS:
        eqn = eqn.replace(key, UNARY_OPS[key])
        x = x.replace(key, UNARY_OPS[key])
    for key in MATH_CONST:
        eqn = eqn.replace(key, MATH_CONST[key])
        x = x.replace(key, MATH_CONST[key])

  
    eqn = eqn.replace("x", x)

    try:
        code = parser.expr(eqn).compile()
        return eval(code)
    except NameError:
        return "Unrecognized symbol in equation"
    except ValueError:
        return "Domain error, you have gone out of bounds for a specific function"
    except ZeroDivisionError:
        return "You have devided by zero"
    else:
        return "What did you do!" 


if __name__ == "__main__":
    print(evaluation("sin(x)", "pi"))
