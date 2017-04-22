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
import platform
import tempfile
import os


def MATH_CONST():
    return {"pi": "π"}


def sanitize_input(user_input):
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



def solve_on_standard_posix(user_input, x):
    """Solves the equation on a normal unix or unix like operating system"""
    user_input = sanitize_input(user_input)
    x = sanitize_input(x)
    for const in MATH_CONST():
        user_input = user_input.replace(const, MATH_CONST()[const])
        x = x.replace(const, MATH_CONST()[const])
    user_input = user_input.replace("x", x)
    out = subprocess.check_output("echo '{uinput}' | gcalccmd".format(uinput=user_input), shell=True)
    ret = out.decode("utf-8")
    # return is generally returned as a string starting with > followed by a new line and some white space
    # followed by the output, then followed by the another >
    if ret is None or ret.count('>') != 2:
        return "invalid"
    # checks if there is an empty line between the two >
    if ret.count('>') == 2 and ret[ret.index(">")+1:ret[ret.index(">")+1:].index(">")].strip().replace(' ', '') == '':
        return "invalid"
    else:
        return ret[ret.index(">")+1:ret[ret.index(">")+1:].index(">")].strip()


def solve_on_windows_running_ubuntu_bash(user_input, x):
    user_input = sanitize_input(user_input)
    x = sanitize_input(x)
    for const in MATH_CONST():
        user_input = user_input.replace(const, MATH_CONST()[const])
        x = x.replace(const, MATH_CONST()[const])
    user_input = user_input.replace("x", x)
    out = subprocess.check_output("echo '{uinput}' | gcalccmd".format(uinput=user_input), shell=True,
                                  executable="C:\\Windows\\System32\\bash.exe")
    ret = out.decode("utf-8")
    print(ret)
    if ret or ret.count('>') != 2:
        return "invalid"
    if(ret.count('>') == 2
       and ret[ret.index(">") + 1:ret[ret.index(">") + 1:].index(">")].strip().replace(' ', '') == ''):
        return "invalid"
    else:
        return ret[ret.index(">") + 1:ret[ret.index(">") + 1:].index(">")].strip()


def solve(user_input, x=""):
    """Solves a mathematical expresion using the gnome calculator software."""
    # sanatize input to avoid security errors
    if os.name != 'nt':
        return solve_on_standard_posix(user_input, x)
    else:
        return solve_on_windows_running_ubuntu_bash(user_input, x)


def wintolin(path):
    path = os.path.abspath(path)
    if path[1:2] == ':':
        drive = path[:1].lower()
        return '/mnt/' + drive + path[2:].replace('\\', '/')

if __name__ == "__main__":
    is32bit = (platform.architecture()[0] == '32bit')
    system32 = os.path.join(os.environ['SystemRoot'],
                            'SysNative' if is32bit else 'System32')
    bash = os.path.join(system32, 'cmd.exe')

    #subprocess.check_call('"%s" -c "echo \'hello world\'"' % bash)
    out = subprocess.check_output("bash -c pwd", shell=True, executable=bash, stderr=subprocess.PIPE)
    ret = out.decode("utf-8")
    print(ret)