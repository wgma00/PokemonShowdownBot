from room import Room
from user import User


def test_adding_user():
    test_room = Room('test')
    test_user = User('bot', True)
    test_room.addUser(test_user)
    assert(test_room.getUser('bot'))

def test_renamed_user():
    test_room = Room('test')
    test_user = User('bot', True)
    test_room.addUser(test_user)
    test_room.renamedUser(test_user, User('bot2', True))
    assert(test_room.getUser('bot2'))

