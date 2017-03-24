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


# Each PS room joined creates an object here.
# Objects control settings on a room-per-room basis, meaning every room can
# be treated differently.

import json
from collections import deque
from plugins.tournaments import Tournament
import robot as r


class Room:
    """ Contains all important information of a pokemon showdown room.

    Attributes:
        users: map, maps user ids to users.
        loading: Bool, if this room is still loading information.
        title: string, name of the room.
        rank: string, the rank of this bot in this room.
        moderate: Bool, if this bot should moderate this room.
        allowGames: Bool, if this bot will allow games in this room.
        tour: Bool, if this bot will allow tours in this room.
        activity: Workshop object, if this room is a workshop.
        tourwhiteList: list of str, users who are not moderators but who have
                       permission to start a tour.
    """
    def __init__(self, room, data=None):
        """Intializes room with preliminary information."""
        if not data:
            # This is to support both strings and dicts as input
            data = {'moderate': False, 'allow games': False,
                    'tourwhitelist': [], 'broadcastrank':' '}
        self.users = {}
        self.loading = True
        self.title = room
        self.broadcast_rank = data['broadcastrank']
        self.rank = ' '
        self.moderate = data['moderate']
        self.allowGames = data['allow games']
        self.tour = None
        self.activity = None
        self.tourwhitelist = data['tourwhitelist']
        self.chatlog = deque({'': -1}, 20) # we will log the past 20 messages

    def doneLoading(self):
        """Set loading status to False"""
        self.loading = False

    def addUser(self, user):
        """Adds user to room."""
        if user.id not in self.users:
            self.users[user.id] = user

    def removeUser(self, userid):
        """Removes user from this room."""
        if userid in self.users:
            return self.users.pop(userid)

    def renamedUser(self, old, new):
        """updates user credentials."""
        self.removeUser(old)
        self.addUser(new)

    def getUser(self, name):
        """Returns true if this user is in this room."""
        if name in self.users:
            return self.users[name]

    def logChat(self, user, message):
        """Logs the message unto our message queue"""
        self.chatlog.append({user.id: len(message)})

    def isWhitelisted(self, user):
        """Returns true if this user is white listed for tours."""
        return user.hasRank('@') or user in self.tourwhitelist

    def addToWhitelist(self, user):
        """Adds user to whitelist"""
        if user in self.tourwhitelist:
            return False
        self.tourwhitelist.append(user)
        return True

    def delFromWhitelist(self, target):
        """Returns true if the operation was succesful."""
        if target not in self.tourwhitelist:
            return False
        self.tourwhitelist.remove(target)
        return True

    def createTour(self, ws, form):
        """Creates a tour with the specified format.

        Args:
            ws: websocket.
            form: string, type of format for this tournament.
        """
        self.tour = Tournament(ws, self.title, form)

    def getTourWinner(self, msg):
        """Returns the winner of the current game.
        Args:
            msg:str, winning message from the tour.
        Returns:
            tuple (str,str) , represeting the user and the format won.
        """
        things = json.loads(msg)
        return things['results'][0], things['format']

    def endTour(self):
        """Ends the current tournament."""
        self.tour = None


# Commands
def allowgames(bot, cmd, room, msg, user):
    """Determines if a user is allowed to commence a chat game of any sort.
    Args:
        bot: Robot, connection between this funciton and the main program.
        cmd: str, the command the user is executing.
        msg: str, any message found after the command.
        user: user object.
    Returns:
        Reply object denoting the mesage to be returned and whether or not it
        the message should be sent in PMs or public chat.
    """
    reply = r.ReplyObject()
    if not user.hasRank('#'):
        return reply.response(('You do not have permission to change this.'
                               ' (Requires #)'))
    if room.title == 'pm':
        return reply.response("You can't use this command in a pm.")
    msg = bot.removeSpaces(msg)
    if msg in ['true','yes','y','True']:
        if room.allowGames:
            return reply.response(('Chatgames are already allowed'
                                   'in this room.'))
        room.allowGames = True
        return reply.response('Chatgames are now allowed in this room.')

    elif msg in ['false', 'no', 'n',' False']:
        room.allowGames = False
        return reply.response('Chatgames are no longer allowed in this room.')
    return reply.response(('{param} is not a supported parameter')
                          .format(param=msg))

def tour(bot, cmd, room, msg, user):
    """Determines if a user is allowed to commence a tour of any sort.
    Args:
        bot: Robot, connection between this funciton and the main program.
        cmd: str, the command the user is executing.
        msg: str, any message found after the command.
        user: user object.
    Returns:
        Reply object denoting the mesage to be returned and whether or not it
        the message should be sent in PMs or public chat.
    """
    reply = r.ReplyObject('', True, True, True)
    if room.title == 'pm':
        return reply.response("You can't use this command in a pm.")
    if not room.isWhitelisted(user):
        return reply.response(("You are not allowed to use this command. "
                               "(Requires whitelisting by a Room Owner)"))
    if not bot.canStartTour(room):
        return reply.response("I don't have the rank required to start a tour")
    return reply.response(("/tour {rest}\n"
                           "/modnote From {user}")
                           .format(rest=msg, user=user.name))

def tourwl(bot, cmd, room, msg, user):
    """Adds a user to the whitelist of people who can start a tour.
    Args:
        bot: Robot, connection between this funciton and the main program.
        cmd: str, the command the user is executing.
        msg: str, any message found after the command.
        user: user object.
    Returns:
        Reply object denoting the mesage to be returned and whether or not it
        the message should be sent in PMs or public chat.
    """
    reply = r.ReplyObject('', True)
    if not user.hasRank('#'):
        return reply.response(("You do not have permission to change this."
                              " (Requires #)"))
    target = bot.toId(msg)
    if not room.addToWhitelist(target):
        return reply.response('This user is already whitelisted in that room.')
    bot.saveDetails()
    return reply.response(("{name} added to the whitelist in this room.")
                           .format(name = msg))

def untourwl(bot, cmd, room, msg, user):
    """Attempts to remove a user from the whistlist of people who start tours.
    Args:
        bot: Robot, connection between this funciton and the main program.
        cmd: str, the command the user is executing.
        msg: str, any message found after the command.
        user: user object.
    Returns:
        Reply object denoting the mesage to be returned and whether or not it
        the message should be sent in PMs or public chat.
    """
    reply = r.ReplyObject('', True)
    if not user.hasRank('#'):
        return reply.response(("You do not have permission to change this."
                              " (Requires #)"))
    target = bot.toId(msg)
    if not room.delFromWhitelist(target):
        return reply.response('This user is not whitelisted in that room.')
    bot.saveDetails()
    return reply.response(("{name} removed from the whitelist in this room.")
                           .format(name = msg))

RoomCommands = {
    'allowgames': allowgames,
    'tour': tour,
    'tourwl': tourwl,
    'untourwl': untourwl
}
