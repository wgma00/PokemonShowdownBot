import pytest
from plugins.Send import Send
from plugins.Credits import Credits
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
