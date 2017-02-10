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


def test_user_owner():
    reg_user = User('user', ' ', True)
    assert reg_user.hasRank('~'), 'owner is not recognized in rank comparison'


def test_user_rank_untested():
    with pytest.raises(UnSpecifiedUserRankException):
        reg_user = User('user', '+', False)
        reg_user.hasRank('not valid')


