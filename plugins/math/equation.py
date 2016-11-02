# Copyright (C) 2016 William Granados<wiliam.granados@wgma00.me>
# 
# This file is part of PokemonShowdownBot.
# 
# PokemonShowdownBot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# PokemonShowdownBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with PokemonShowdownBot.  If not, see <http://www.gnu.org/licenses/>.

import subprocess
import threading
import queue

def MATH_CONST(): return  {"pi":"π"}

def sanatize_input(user_input):
    """ Removes nasty stuff that could bork the system."""
    user_input = user_input.replace('$', '')
    user_input = user_input.replace('|', '')
    user_input = user_input.replace('>', '')
    user_input = user_input.replace("'", '')
    user_input = user_input.replace('"', '')
    user_input = user_input.replace('rm', '')
    user_input = user_input.replace('quit', '')
    user_input = user_input.replace('exit', '')
    return user_input

def solve(user_input, x=""):
    """Solves a mathematical expresion using the gnome calculator software."""
    # sanatize input to avoid security errors
    user_input = sanatize_input(user_input)
    x = sanatize_input(x)
    for const in MATH_CONST():
        user_input = user_input.replace(const, MATH_CONST()[const])
        x = x.replace(const, MATH_CONST()[const])
    user_input = user_input.replace("x", x)
    out = subprocess.check_output("echo '{uinput}' | gcalccmd".format(uinput=user_input), shell=True)
    ret = out.decode("utf-8")
    if(ret == None or ret.count('>') != 2):
        return "invalid"
    if(ret.count('>') == 2 and ret[ret.index(">")+1:ret[ret.index(">")+1:].index(">")].strip().replace(' ','') == ''):
        return "invalid"
    else:
        return ret[ret.index(">")+1:ret[ret.index(">")+1:].index(">")].strip()                                          

if __name__ == "__main__":
    print(solve("1+2"))
    print(solve("|sin(-x)|", "0"))
    print(solve("0.5!"))
    q = queue.Queue()
    test_cases = ["1+2", "|sin(-0)|", "0.5!","1!"]
    threading.TIMEOUT_MAX = 5
    for test in test_cases:
        t = threading.Thread(target=solve, args=(test,))
        t.daemon = True
        t.start()
    while(not q.empty()):
        s = q.pop()
        print(s)


