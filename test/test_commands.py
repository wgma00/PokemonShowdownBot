from commands import Command, ReplyObject, Latex, ExternalCommands
from room import Room
from user import User
from app import PSBot
from subprocess import CalledProcessError
import details
import pytest
from data.pokedex import Pokedex
import re


psb = PSBot()
test_room = Room('test')
test_user = User('user')

""" Tests the commands that are within the Command method
"""


def test_test():
    reply = Command(psb, 'test', test_room, '', test_user)
    # should be acessible by any user
    answer = ReplyObject('test', True, False, False, False, False)
    assert reply == answer, 'no test command was found'


def test_source():
    test_user = User('user', False)
    reply_one = Command(psb, 'git', test_room, '', test_user)
    reply_two = Command(psb, 'source', test_room, '', test_user)
    answer = ReplyObject('Source code can be found at: https://github.com/wgma00/quadbot/')
    assert reply_one == answer and reply_two == answer, 'source has been changed'


def test_latex_compilation_expected_input():
    try:
        Command(psb, 'latex', test_room, '$1+1$', test_user)
    except CalledProcessError:
        assert False, 'There was an error with the compiling of latex'


def test_latex_compilation_wrong_input():
    with pytest.raises(CalledProcessError):
        Command(psb, 'latex', test_room, '$\\begin{}+1$', test_user)


def test_latex_compilation_dangerous_input():
    reply = Command(psb, 'latex', test_room, '$\input{/etc/passwd}$', test_user)
    answer = ReplyObject("invalid latex expression")
    assert reply == answer, '\input was not handled in latex'


def test_putnam_problem_generator():
    Command(psb, 'putnam', test_room, '', test_user)


def test_calc_valid_input():
    try:
        # generic test
        reply = Command(psb, 'calc', test_room, '1+1', test_user)
        answer = ReplyObject('2', True)
        assert reply == answer, 'incorrect arithmetic expression'
        # testing for substitution
        reply = Command(psb, 'calc', test_room, '|sin(-x)|, 0', test_user)
        answer = ReplyObject('0', True)
        assert reply == answer, 'incorrect arithmetic expression'
        # testing for singular substitution 
        reply = Command(psb, 'calc', test_room, 'x', test_user)
        answer = ReplyObject('0', True)
        assert reply == answer, 'incorrect arithmetic expression'
        # testing on a relatively large factorial
        reply = Command(psb, 'calc', test_room, '191!', test_user)
        answer = ReplyObject('1.848941631×10³⁵⁴', True)
        assert reply == answer, 'incorrect arithmetic expression'
    except CalledProcessError:
        assert False, 'gcalccmd library missing'


def test_calc_invalid_input():
    try:
        reply = Command(psb, 'calc', test_room, '', test_user)
        answer = ReplyObject('invalid', True)
        assert reply == answer, 'invalid expression recognized by calculator'
        # break out of the echo '' by completing the ', then do some nasty things
        reply = Command(psb, 'calc', test_room, "'rm", test_user)
        answer = ReplyObject('invalid', True)
        assert reply == answer, 'dangerous user input not handled correctly'
        reply = Command(psb, 'calc', test_room, "$'rm", test_user)
        answer = ReplyObject('invalid', True)
        assert reply == answer, 'dangerous user input not handled correctly'
        reply = Command(psb, 'calc', test_room, "1+test", test_user)
        answer = ReplyObject('invalid', True)
        assert reply == answer, 'dangerous user input not handled correctly'
    except CalledProcessError:
        assert False, 'gcalccmd library missing'



def test_owner():
    reply = Command(psb, 'owner', test_room, '', test_user)
    answer = ReplyObject('Owned by: ' + details.master, True)
    assert reply == answer, 'master and owner do not match.'


def test_invalid_command():
    reply = Command(psb, 'test_command', test_room, '', test_user)
    assert reply.text == ReplyObject('test_command is not a valid command').text, 'Invalid command not properly recognized; {}'.format(reply.text)


def test_add_external_command():
    def test_command(bot, cmd, room, msg, user): return ReplyObject('')
    ExternalCommands.update({'test_command': test_command})
    reply = Command(psb, 'test_command', test_room, '', test_user)
    assert reply.text == ReplyObject('').text, 'External command was not properly recognized'

def test_pokemon_smogon_analysis():
    for p in Pokedex:
        pok = re.sub('-(?:mega(?:-(x|y))?|primal)', '', p, flags=re.I).replace(' ', '').lower()
        substitutes = {'gourgeist-s':'gourgeist-small',
                       'gourgeist-l':'gourgeist-large',
                       'gourgeist-xl':'gourgeist-super',
                       'pumpkaboo-s':'pumpkaboo-small',
                       'pumpkaboo-l':'pumpkaboo-large',
                       'pumpkaboo-xl':'pumpkaboo-super',
                       'giratina-o':'giratina-origin',
                       'mr.mime':'mr_mime',
                       'mimejr.':'mime_jr'}
        pok2 = pok
        if pok in substitutes:
            pok2 = substitutes[pok]
        reply = Command(psb, p.replace(' ', '').lower(), test_room, '', test_user)
        answer = ReplyObject('Analysis: http://www.smogon.com/dex/sm/pokemon/{poke}/'.format(poke=pok2), True)
        assert reply.text == answer.text, '{poke} was not recognized; {rep} == {ans}'.format(poke=pok, rep=reply.text, ans=answer.text)

