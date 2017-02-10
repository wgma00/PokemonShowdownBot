from commands import Command, ReplyObject, Latex
from room import Room
from user import User
from app import PSBot
import os
from subprocess import CalledProcessError
import pytest
import pyimgur

psb = PSBot()
if not Latex._client_id:
    Latex._client_id = os.environ['IMGUR_API']
    Latex._client_id = Latex._client = pyimgur.Imgur(Latex._client_id)

""" Tests the commands that are within the Command method
"""


def test_test():
    test_room = Room('test')
    regular_user = User('user', False)
    reply = Command(psb, 'test', test_room, '', regular_user)
    # should be acessible by any user
    answer = ReplyObject('test', True, False, False, False, False)
    assert reply == answer, 'no test command was found'


def test_source():
    test_room = Room('test')
    regular_user = User('user', False)
    reply_one = Command(psb, 'git', test_room, '', regular_user)
    reply_two = Command(psb, 'source', test_room, '', regular_user)
    answer = ReplyObject('Source code can be found at: https://github.com/wgma00/PokemonShowdownBot/')
    assert reply_one == answer and reply_two == answer, 'source has been changed'


def test_credits():
    test_room = Room('test')
    regular_user = User('user', False)
    reply = Command(psb, 'credits', test_room, '', regular_user)
    answer = ReplyObject('Credits can be found: https://github.com/wgma00/PokemonShowdownBot/')
    assert reply == answer, 'credits have been changed'


def test_latex_compilation_expected_input():
    test_room = Room('test')
    regular_user = User('user', False)
    try:
        reply = Command(psb, 'latex', test_room, '$1+1$', regular_user)
    except CalledProcessError as e:
        assert False, 'There was an error with the compiling of latex'


def test_latex_compilation_wrong_input():
    with pytest.raises(CalledProcessError):
        test_room = Room('test')
        regular_user = User('user', False)
        Command(psb, 'latex', test_room, '$\\begin{}+1$', regular_user)





