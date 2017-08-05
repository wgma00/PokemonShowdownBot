import pytest
from commands import Command
from plugins.Send import Send
from plugins.Credits import Credits
from plugins.math.Latex import Latex
from plugins.math.Calculator import Calculator
from plugins.Machine import Machine
from plugins.Xkcd import Xkcd
from plugins.Dilbert import Dilbert


from room import Room
from user import User
from robot import ReplyObject


test_room = Room('test')
test_user = User('user')
test_owner = User('user', ' ',  True)


@pytest.fixture
def before():
    global test_user
    global test_room
    global test_owner
    test_user = User('test')
    test_room = Room('test')
    test_owner = User('test', ' ', True)


def test_commands_delegation():
    cmd_out = Command(None, 'send', test_room, 'testing', test_owner)
    answer = ReplyObject('testing', True, True)
    assert cmd_out == answer, "delegation to modules doesn't work"

    cmd_out = Command(None, 'machine', test_room, '', test_user)
    answer = ReplyObject('I am the machine!', True)
    assert cmd_out == answer, "delegation to modules doesn't work"

    cmd_out = Command(None, 'secret', test_room, '', test_owner)
    answer = ReplyObject('This is a secret command!', True)
    assert cmd_out == answer, "delegation to secret commands doesn't work"


def test_send():
    cmd = Send()

    reply = cmd.response(test_room, test_user, ['hi'])
    answer = ReplyObject("This command is reserved for this bot's owner", True)
    assert reply == answer, 'send command does not handle permissions correctly'

    reply = cmd.response(test_room, test_owner, ['hi'])
    answer = ReplyObject('hi', True, True)
    assert reply == answer, "send command's success output is incorrect"

    reply = cmd.response(test_room, test_user, ['help'])
    answer = ReplyObject('Responds with arguments passed to this command, reserved for bot owner', True)
    assert reply == answer, "send command's help output incorrect"


def test_credits():
    cmd = Credits()

    reply = cmd.response(test_room, test_user, [])
    answer = ReplyObject("Source code can be found at: https://github.com/wgma00/quadbot/", True)
    assert reply == answer, "Credit command's success output is incorrect"

    reply = cmd.response(test_room, test_owner, ['arg1', 'arg2'])
    answer = ReplyObject("This command doesn't take any arguments", True)
    assert reply == answer, "Credit command shouldn't take any arguments"

    reply = cmd.response(test_room, test_user, ['help'])
    answer = ReplyObject("Responds with url to this bot's source code", True)
    assert reply == answer, "Credit command's help output incorrect"


def test_latex():
    cmd = Latex()

    reply = cmd.response(test_room, test_user, [])
    answer = ReplyObject("Insufficient arguments provided. Should have a LaTeX expression surrounded by $.\n", True)
    assert reply == answer, 'insufficient arguments not handled correctly'

    reply = cmd.response(test_room, test_user, ['$1+1$'])
    assert reply.text.startswith('http'), "Compiling and/or uploading to imgur doesn't work"

    test_room.rank = '*'
    reply = cmd.response(test_room, test_user, ['$1+1$', 'showimage'])
    assert 'http' in reply.text, "Compiling, showimaging, and/or  uploading to imgur doesn't work"

    test_room.rank = ' '
    reply = cmd.response(test_room, test_user, ['$1+1$', 'showimage'])
    answer = ReplyObject('This bot requires * or # rank to showimage in chat', True)
    assert reply == answer, "Showimages with insufficient privileges not handled correctly"

    reply = cmd.response(test_room, test_user, ['$\\begin{}+1$'])
    answer = ReplyObject('There was an internal error. Check your LaTeX expression for any errors', True)
    assert reply == answer, "Exceptions aren't handled correctly"

    reply = cmd.response(test_room, test_user, '$\input{/etc/passwd}$')
    answer = ReplyObject( ('You have inputted an invalid LaTeX expression. You may have forgotten to surround '
                           'your expression with $. Or you may have used restricted LaTeX commands'), True)
    assert reply == answer, 'Dangerous input not handled correctly'

    reply = cmd.response(test_room, test_owner, ['tikz-cd', 'addpackage'])
    answer = ReplyObject('tikz-cd has been added. This is not saved on restart', True, True)
    assert reply == answer, 'addpackage functionality not working'

    reply = cmd.response(test_room, test_owner, ['tiks-cd', 'addpackage'])
    answer = ReplyObject(('You may only install one package at a time. i.e. latex tikz-cd, addpackage . If that '
                          'is not the issue then it is possible that the package specified is not available on '
                          'the host system'), True)
    assert reply == answer, 'addpackage package installation error not correct'

    reply = cmd.response(test_room, test_user, ['tikz-cd', 'addpackage'])
    answer = ReplyObject('This command is reserved for RoomOwners', True)
    assert reply == answer, 'addpackage functionality not working'

    test_room.isPM = True
    reply = cmd.response(test_room, test_user, ['$1+1$', 'showimage'])
    answer = ReplyObject('This bot cannot showimage in PMs.', True)
    assert reply == answer, 'Showimages in PMs not handled correctly'
    test_room.isPm = False


def test_machine():
    cmd = Machine()

    reply = cmd.response(test_room, test_user, ['help'])
    answer = ReplyObject("Responds with I am the machine! [[The Machine - Bert Kreischer: THE MACHINE]]", True)
    assert reply == answer, "Help command output isn't correct"

    reply = cmd.response(test_room, test_user, ["whodamachine?"])
    answer = ReplyObject("This command doesn't take any arguments", True)
    assert reply == answer, "Help command Amount of arguments taken is incorrect"

    reply = cmd.response(test_room, test_user, [])
    answer = ReplyObject("I am the machine!", True)
    assert reply == answer, "Help command success output not correct"


def test_calc():
    cmd = Calculator()

    # generic test
    reply = cmd.response(test_room, test_user, ['1+1'])
    answer = ReplyObject('2', True)
    assert reply == answer, 'incorrect arithmetic expression'

    # testing for substitution
    reply = cmd.response(test_room, test_user, ['|sin(-x)|', '0'])
    answer = ReplyObject('0', True)
    assert reply == answer, 'incorrect arithmetic expression'

    # testing for singular substitution
    reply = cmd.response(test_room, test_user, ['x'])
    answer = ReplyObject('0', True)
    assert reply == answer, 'incorrect arithmetic expression'

    # testing on a relatively large factorial
    reply = cmd.response(test_room, test_user, ['191!'])
    answer = ReplyObject('1.848941631×10³⁵⁴', True)
    assert reply == answer, 'incorrect arithmetic expression'

    # testing on incorrect input
    reply = cmd.response(test_room, test_user, [])
    answer = ReplyObject('There should be an expression optionally followed by substitution', True)
    assert reply == answer, 'invalid expression recognized by calculator'

    # break out of the echo '' by completing the ', then do some nasty things
    reply = cmd.response(test_room, test_user, ["'rm"])
    answer = ReplyObject('invalid input', True)
    assert reply == answer, 'dangerous user input not handled correctly'

    reply = cmd.response(test_room, test_user, ["$'rm"])
    answer = ReplyObject('invalid input', True)
    assert reply == answer, 'dangerous user input not handled correctly'

    reply = cmd.response(test_room, test_user, ["1+test"])
    answer = ReplyObject('invalid input', True)
    assert reply == answer, 'dangerous user input not handled correctly'


def test_xkcd():
    cmd = Xkcd()

    reply = cmd.response(test_room, test_user, [])
    assert reply.text.startswith('https'), "xkcd command proper url isn't sent"

    reply = cmd.response(test_room, test_user, ['1'])
    answer = ReplyObject('https://imgs.xkcd.com/comics/barrel_cropped_(1).jpg', True)
    assert reply == answer, 'xkcd command individual xkcd article not found'

    reply = cmd.response(test_room, test_user, ['help'])
    answer = ReplyObject(("Responds with url to random xkcd article, number can also be specified. And this command "
                          "supports showimages."), True)
    assert reply == answer, 'xkcd command help function is incorrect'


def test_dilbert():
    cmd = Dilbert()

    reply = cmd.response(test_room, test_user, ['help'])
    answer = ReplyObject(("Responds with url to random xkcd article, number can also be specified. And this command "
                          "supports showimages."), True)
    assert reply == answer, 'Help command for Dilbert is incorrect'

    reply = cmd.response(test_room, test_user, [])
    assert reply.text.startswith('http'), 'Dilbert command url not generated.'

    reply = cmd.response(test_room, test_user, ['args1', 'args2'])
    answer = ReplyObject("This command doesn't take any arguments", True)
    assert reply == answer, 'arguments passed to Dilbert command when they should not'
