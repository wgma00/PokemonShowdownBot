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

from cleverbot import Cleverbot


class Clever(object):

    def __init__(self):
        self.bot = Cleverbot()
        self.last = ""

    def update(self, last_msg):
        self.last = last_msg

    def reply(self):
        return self.bot.ask(self.last)


if __name__ == "__main__":
    c = Clever()
    c.update("hello")
    print(c.reply())
