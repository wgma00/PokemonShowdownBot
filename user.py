# Copyright (C) 2016 William Granados<wiliam.granados@wgma00.me>
#
# This file is part of PokemonShowdownBot.
#
# PokemonShowdownBot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PokemonShowdownBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PokemonShowdownBot.  If not, see <http://www.gnu.org/licenses/>.
#
# This file incorporates work covered by the following copyright and
# permission notice:
#
#     The MIT License (MIT)
#
#     Copyright (c) 2015 QuiteQuiet<https://github.com/QuiteQuiet>
#
#     Permission is hereby granted, free of charge, to any person obtaining a
#     copy of this software and associated documentation files (the "Software")
#     , to deal in the Software without restriction, including without
#     limitation the rights to use, copy, modify, merge, publish, distribute
#     sublicense, and/or sell copies of the Software, and to permit persons to
#     whom the Software is furnished to do so, subject to the following
#     conditions:
#
#     The above copyright notice and this permission notice shall be included
#     in all copies or substantial portions of the Software.
#
#     THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
#     OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#     MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#     IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
#     CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
#     TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#     SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import re


class UnSpecifiedUserRankException(Exception):
    """This error is thrown in the case that there is a new user added by the
    admins of PokemonShowdown, i.e. when they added the new bot user rank.
    """
    def __init__(self,user_class):
        self.user_class = user_class
    def __str__(self):
        return 'Unsupported user class:' + self.user_class

class User:
    """Very basic class for a pokemon showdown user.
    Attributes:
        Groups: map, ranks presedence of user ranks by symbols.
        name:string, username.
        id:string, simplifid unique username.
        rank:string, user rank.
        owner:Bool, is this you.
    """
    Groups = {' ':0,'+':1,'★':1,'%':2,'@':3,'*':3.1,'&':4,'#':5,'~':6}

    def __init__(self, name, rank, owner = False):
        """Initializes user.
        Args:
            name:string, username.
            rank:string, user rank.
            owner:Bool, is this you.
        """
        self.name = name
        self.id = re.sub(r'[^a-zA-z0-9]', '', name).lower()
        self.rank = rank
        self.owner = owner

    @staticmethod
    def compareRanks(rank1, rank2):
        """Compares two user ranks.
        Args:
            rank1: char, user rank of first person
            rank2: char, user rank of second person
        Returns:
            True if user rank 1 is greater than user rank 2
        Exception:
            UnSpecifiedUserClassException
        """
        try:
            return User.Groups[rank1] >= User.Groups[rank2]
        except:
            if not rank1 in User.Groups:
                raise UnSpecifiedUserClassException
            if not rank2 in User.Groups:
                raise UnSpecifiedUserClassException
            return False

    def isOwner(self):
        """Checks if the current user object is the master(hence you)"""
        return self.owner

    def hasRank(self, rank):
        """Determines if a user has sufficient staff rights"""
        return self.owner or User.compareRanks(self.rank, rank)


if __name__ == '__main__':
    u = User("bot","*", False)
    print(u.hasRank("@"))
