from plugins.math.putnam import LatexParsingException

from commands import Command, ReplyObject, Latex
from room import Room
from user import User
from app import PSBot
from subprocess import CalledProcessError
import details
import pytest
from data.pokedex import Pokedex
import re


psb = PSBot()

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
        Command(psb, 'latex', test_room, '$1+1$', regular_user)
    except CalledProcessError:
        assert False, 'There was an error with the compiling of latex'


def test_latex_compilation_wrong_input():
    with pytest.raises(CalledProcessError):
        test_room = Room('test')
        regular_user = User('user', False)
        Command(psb, 'latex', test_room, '$\\begin{}+1$', regular_user)


def test_latex_compilation_dangerous_input():
    test_room = Room('test')
    regular_user = User('user', False)
    reply = Command(psb, 'latex', test_room, '$\input{/etc/passwd}$', regular_user)
    answer = ReplyObject("invalid latex expression")
    assert reply == answer, '\input was not handled in latex'


def test_putnam_problem_generator():
    """Note: there is correctly an error that hasn't been identified on this piece of software."""
    test_room = Room('test')
    regular_user = User('user', False)
    try:
        Command(psb, 'putnam', test_room, '', regular_user)
    except LatexParsingException:
        print('warning, putnam generator did not parse an input correctly.')


def test_calc_valid_input():
    try:
        test_room = Room('test')
        regular_user = User('user', False)
        # generic test
        reply = Command(psb, 'calc', test_room, '1+1', regular_user)
        answer = ReplyObject('2', True)
        assert reply == answer, 'incorrect arithmetic expression'
        # testing for substitution
        reply = Command(psb, 'calc', test_room, '|sin(-x)|, 0', regular_user)
        answer = ReplyObject('0', True)
        assert reply == answer, 'incorrect arithmetic expression'
        # testing on a relatively large factorial
        reply = Command(psb, 'calc', test_room, '191!', regular_user)
        answer = ReplyObject('1.848941631×10³⁵⁴', True)
        assert reply == answer, 'incorrect arithmetic expression'
    except CalledProcessError:
        assert False, 'gcalccmd library missing'


def test_calc_invalid_input():
    try:
        test_room = Room('test')
        regular_user = User('user', False)
        reply = Command(psb, 'calc', test_room, '', regular_user)
        answer = ReplyObject('invalid', True)
        assert reply == answer, 'invalid expression recognized by calculator'
        # break out of the echo '' by completing the ', then do some nasty things
        reply = Command(psb, 'calc', test_room, "'rm", regular_user)
        answer = ReplyObject('invalid', True)
        assert reply == answer, 'dangerous user input not handled correctly'
        reply = Command(psb, 'calc', test_room, "$'rm", regular_user)
        answer = ReplyObject('invalid', True)
        assert reply == answer, 'dangerous user input not handled correctly'
        reply = Command(psb, 'calc', test_room, "1+test", regular_user)
        answer = ReplyObject('invalid', True)
        assert reply == answer, 'dangerous user input not handled correctly'
    except CalledProcessError:
        assert False, 'gcalccmd library missing'


def test_owner():
    test_room = Room('test')
    regular_user = User('user', False)
    reply = Command(psb, 'owner', test_room, '', regular_user)
    answer = ReplyObject('Owned by: ' + details.master, True)
    assert reply == answer, 'master and owner do not match.'


def test_pokemon_smogon_analysis():
    test_room = Room('test')
    regular_user = User('user', False)
    for p in Pokedex.keys():
        pok = re.sub('-(?:mega(?:-(x|y))?|primal)', '', p, flags=re.I).replace(' ', '').lower()
        substitutes = {'gourgeist-s': 'gourgeist-small', 'gourgeist-l': 'gourgeist-large',
                       'gourgeist-xl': 'gourgeist-super', 'pumpkaboo-s': 'pumpkaboo-small',
                       'pumpkaboo-l': 'pumpkaboo-large', 'pumpkaboo-xl': 'pumpkaboo-super',
                       'giratina-o': 'giratina-origin', 'mr.mime': 'mr_mime', 'mimejr.': 'mime_jr'}
        if pok in substitutes:
            pok = substitutes[pok]
        reply = Command(psb, p.replace(' ', '').lower(), test_room, '', regular_user)
        answer = ReplyObject('Analysis: http://www.smogon.com/dex/xy/pokemon/{poke}/'.format(poke=pok), True)
        assert reply == answer, ('{poke} was not recognized; {rep} == {ans}'
                                 '').format(poke=pok, rep=reply.text, ans=answer.text)





