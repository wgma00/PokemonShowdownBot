from room import Room
from user import User
from datetime import datetime


def test_add_banned_word():
    test_room = Room('test')
    test_room.moderation.addBan('phrase', 'CATFISH')
    assert test_room.moderation.isBanword('catfish'), 'catfish should be a banned phrase'


def test_remove_banned_word():
    test_room = Room('test')
    test_room.moderation.addBan('phrase', 'CATFISH')
    test_room.moderation.removeBan('phrase', 'catfish')
    assert not test_room.moderation.isBanword('catfish'), 'catfish should not be a banned phrase'


def test_findingURL():
    test_room = Room('test')
    assert test_room.moderation.containUrl('http://github.com is a good website'), 'Should find an url in this string'


def test_stretching():
    test_room = Room('test')
    assert test_room.moderation.isStretching('oioioioioioio', test_room.users), 'Should be recognized as stretching'


def test_caps():
    test_room = Room('test')
    assert test_room.moderation.isCaps('GITHUB IS A GOOD WEBSITE', test_room.users), 'should recognize it as caps'


def test_spam():
    test_room = Room('test')
    test_user = User('user')
    assert not test_room.moderation.isSpam('1', test_user, datetime.utcfromtimestamp(1)), 'should not be spam'
    assert not test_room.moderation.isSpam('2', test_user, datetime.utcfromtimestamp(2)), 'should not be spam'
    assert not test_room.moderation.isSpam('3', test_user, datetime.utcfromtimestamp(3)), 'should not be spam'
    assert not test_room.moderation.isSpam('4', test_user, datetime.utcfromtimestamp(4)), 'should not be spam'
    assert test_room.moderation.isSpam('5', test_user, datetime.utcfromtimestamp(5)), 'should be spam now'


def test_config():
    test_room = Room('test', {
        'moderate': {'room':
                     'test',
                     'anything': True,
                     'spam': False,
                     'banword': False,
                     'stretching': False,
                     'caps': True,
                     'groupchats': False,
                     'urls': False},
        'allow games': False,
        'broadcastrank': ' ',
        'tourwhitelist': []}
    )
    test_user = User('user')
    assert 'caps' == test_room.moderation.shouldAct('OIOIOIOIOIOIOIOI', test_user, 0), 'should be punished for caps not stretching'


def test_punishment_increase():
    test_room = Room('test')
    test_user = User('user')
    first_action, reply = test_room.moderation.getAction(test_room, test_user, 'caps', 0)
    second_action, reply = test_room.moderation.getAction(test_room, test_user, 'flooding', 0)
    assert not first_action == second_action, '{} == {}; should get escalated punishment'.format(first_action, second_action)
