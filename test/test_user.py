from user import User
from user import UnSpecifiedUserRankException
import pytest


def test_user_rank():
    reg_user = User('user', '~', False)
    assert reg_user.hasRank('+'), 'rank comparison is off'
    reg_user = User('user', '*', False)
    assert reg_user.hasRank('@'), 'rank comparison is off'
    reg_user = User('user', '%', False)
    assert reg_user.hasRank('+'), 'rank comparison is off'


def test_user_owner_privileges():
    reg_user = User('user', ' ', False)
    owner = User('user', ' ',  True)
    assert owner.hasRank('~'), 'owner is not recognized in rank comparison'
    assert owner.isOwner(), 'owner is not owner'
    assert not reg_user.isOwner(), 'regular user is recognized as owner'


def test_user_rank_untested():
    with pytest.raises(UnSpecifiedUserRankException):
        reg_user = User('user', '+', False)
        reg_user.hasRank('not valid')


def test_unspecified_user_rank():
    with pytest.raises(UnSpecifiedUserRankException):
        User.compareRanks('^', '*')

    try:
        User.compareRanks('^', '*')
    except UnSpecifiedUserRankException as e:
        assert str(e) == 'Unsupported user class:^'

