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

MATH_CONST = {"pi":"π"}

def solve(user_input, x=""):
    """ Solves a mathematical expresion using the gnome calculator software."""
    for const in MATH_CONST:
        user_input = user_input.replace(const, MATH_CONST[const])
        x = x.replace(const, MATH_CONST[const])
    user_input = user_input.replace("x", x)
    out = subprocess.check_output("echo '{uinput}' | gcalccmd".format(uinput=user_input), shell=True)
    ret = out.decode("utf-8")
    return ret[ret.index(">")+1:ret[ret.index(">")+1:].index(">")].strip()                                          

if __name__ == "__main__":
    print(solve("1+2"))
    print(solve("|sin(-x)|", "0"))


