from commands import Command
from room import Room
from user import User
from app import PSBot

psb = PSBot()

""" Tests the commands that are within the Command method
"""


def test_test():
    test_room = Room('test')
    regular_user = User('user', False)
    reply = Command(psb, 'test', test_room, '', regular_user)
    assert(reply.text == 'test', 'no test command was found')


def test_latex():
    test_room = Room('test')
    regular_user = User('user', False)
    try:
        reply = Command(psb, 'latex', test_room, '$!+1$', regular_user)
    except Exception as e:
        assert(False, 'There was an error with the compiling of latex')

