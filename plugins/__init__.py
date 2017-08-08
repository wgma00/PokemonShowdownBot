# The MIT License (MIT)
#
# Copyright (c) 2015 QuiteQuiet<https://github.com/QuiteQuiet>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from plugins import messages
from plugins import moderation
from plugins import tournaments
from plugins import workshop
from plugins.games.anagram import anagram
from plugins.games.periodic import periodic 
from plugins.battling import battleHandler

# This is where you pick what the name of the command actually is, then map it to a function.
# Every command needs a function to work, with the parameters (bot, cmd, room, msg, user)
# in that order.
PluginCommands = {
    'moderate'      : moderation.moderate,
    'banuser'       : moderation.banthing,
    'banphrase'     : moderation.banthing,
    'unbanuser'     : moderation.unbanthing,
    'unbanphrase'   : moderation.unbanthing,
    'oldgentour'    : tournaments.oldgentour,
    'showranking'   : tournaments.getranking,
    'tell'          : messages.tell,
    'read'          : messages.read,
    'untell'        : messages.untell,
    'workshop'      : workshop.handler,
    'ws'            : workshop.handler,
    'anagram'       : anagram.start,
    'a'             : anagram.answer,
    'periodic'      : periodic.start,
    'pa'            : periodic.answer,
    'storeteam'     : battleHandler.acceptTeam
}
