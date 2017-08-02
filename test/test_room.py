from room import Room
from user import User
import pytest


def test_adding_user():
    test_room = Room('test')
    test_user = User('bot', ' ', owner=True)
    test_room.addUser(test_user)
    assert test_room.getUser('bot'), 'adding bots to room has failed'


def test_renamed_user():
    test_room = Room('test')
    test_user = User('bot', ' ', owner=True)
    test_room.addUser(test_user)
    test_room.renamedUser(test_user, User('bot2', ' ', owner=True))
    assert test_room.getUser('bot2'), 'renaming user has failed'


def test_whitelist():
    test_room = Room('test')
    test_user = User('bot', ' ', owner=False)
    test_room.addUser(test_user)
    assert not test_room.isWhitelisted(test_user), 'user should not be in white list'
    print(test_room.addToWhitelist(test_user))
    print([usr.id for usr in test_room.tourwhitelist], test_room.isWhitelisted(test_user))
    assert test_room.isWhitelisted(test_user), 'user should be in white list'
