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

import subprocess

MATH_CONST = {"pi":"π"}

def solve(user_input):
    """ Solves a mathematical expresion using the gnome calculator software."""
    for const in MATH_CONST:
        user_input = user_input.replace(const, MATH_CONST[const])
    out = subprocess.check_output("echo '{uinput}' | gcalccmd".format(uinput=user_input), shell=True)
    ret = out.decode("utf-8")
    return ret[ret.index(">")+1:ret[ret.index(">")+1:].index(">")].strip()                                          

if __name__ == "__main__":
    print(solve("1+2"))
    print(solve("|sin(-pi)|"))

