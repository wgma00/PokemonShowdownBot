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


# This is the master class for the Python PS bot.
# Every general-purpose command is included in this file, with the sole
# exception being onMessage(), as derived applications may need to access
# this function.
#
# As such, unless a valid onMessage() function is supplied when creating an
# instance, this will not run.
#
# To run this, the following modules are required:
# PyYAML == 3.11
# requests == 2.5.1
# simplejson == 3.6.5
# websocket-client == 0.23.0

import websocket
import requests
import json
import re

from room import Room
from user import User
from plugins.battling.battleHandler import BattleHandler
from plugins.math.markov import Markov
import details


class PokemonShowdownBot:
    """This class contains most of the functionality of the bot.

    This class handles connecting to the websocket and some basic commands
    functionalities like holding a message for a user.

    Attributes:
        details: a map mapping serveral variables to sensitive information.
        owner: string, the user this bot responds too
        name: string, the name of the bot in chat
        id: string, a simplified string for identifying a user
        rooms: Room object, that keeps track of information in a given room.
        rooms_markov: a map mapping room names to markov objects used to
                      generate sentences for certain rooms.
        commandchar: string, string that is used to execute certain commands.
        url: string, the url for pokemon showdown's open port that the
             websocket will attempt connecting to.
    """
    def __init__(self, url, onMessage=None):
        self.owner = details.master
        self.name = details.bot_name
        self.id = details.bot_id
        self.rooms = {}
        self.rooms_markov = {}
        self.commandchar = details.command_char
        self.intro()
        self.splitMessage = onMessage if onMessage else self.onMessage
        self.url = url
        # websocket.enableTrace(True)
        self.openConnection()

    def onError(self, ws, error):
        """Error message to be printed on error with websocket."""
        print('Websocket Error:', error)

    def onClose(self, message):
        """Error message to be printed on closing the websocket."""
        self.rooms = {}
        print('Websocket closed')

    def onOpen(self, message):
        """Error message to be printed on opening the websocket."""
        print('Websocket opened')

    def openConnection(self):
        """Open the websocket connection and setups pokemon battle handler."""
        self.ws = websocket.WebSocketApp(self.url,
                                         on_message = self.splitMessage,
                                         on_error = self.onError,
                                         on_close = self.onClose)
        self.ws.on_open = self.onOpen
        self.bh = BattleHandler(self.ws, self.name)

    def closeConnection(self):
        self.ws.close()
        self.ws = None

    def intro(self):
        """Simple intro at startup"""
        print("+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+")
        print("|                        Pokemon Showdown Bot                                      |")
        print("|Copyright (C) 2015, QuiteQuiet<https://github.com/QuiteQuiet>                     |")
        print("|Copyright (C) 2016, William Granados<william.granados@wgma00.me>                  |")
        print("|This program comes with ABSOLUTELY NO WARRANTY; for details check the LICENSE file|")
        print("|and the NOTICE file. This is free software, and you are welcome to redistribute it|")
        print("|under the certain conditions outlined in the aforementioned files.                |")
        print("+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+")


    def log(self, sort, msg, user):
        """Log commands made by users in chat.
        Args:
            sort: string, type of command made by a user (think '.git').
            msg: string, substring after the first command character.
            user: string, name of the user
        """
        print("""{sort}: {cmd} (user: {user})
              """.format(sort=sort, cmd=msg, user=user))

    def userIsSelf(self, user):
        """Checks if the user is the the bot itself"""
        return self.name == user

    def send(self, msg):
        """Sends a message to the websocket."""
        self.ws.send(msg)

    def login(self, challenge, challengekeyid):
        """Logins the bot to the pokemon showdown server.
        TODO: add better explanations for variables
        Args:
            challenge: string,
            challengekeyid: string,
        """
        payload = { 'act':'login',
                    'name': self.name,
                    'pass': details.password,
                    'challengekeyid': challengekeyid,
                    'challenge': challenge
                    }
        r = requests.post('http://play.pokemonshowdown.com/action.php',
                          data=payload)
        assertion = json.loads(r.text[1:])['assertion']

        if assertion:
            self.send(('|/trn '+ self.name + ',0,' + str(assertion)
                      ).encode('utf-8'))
            return True
        else:
            print('Assertion failed')
            return False

    def updateUser(self, name, result):
        """Updates the bots credentials on pokemon showdown.

        Args:
            name: string, name of the bot
            result: string, result code of the websocket after websocket is
                    opened.
        """
        if self.name not in name:
            return
        if not result == '1':
            print('login failed, still guest')
            print('crashing now; have a nice day :)')
            exit()

        if details.avatar >= 0:
            self.send('|/avatar {num}'.format(num=details.avatar))
        print('{name}: Successfully logged in.'.format(name=self.name))
        for rooms in details.joinRooms:
            name = [n for n in rooms][0] # joinRoom entry is a list of dicts
            self.joinRoom(name, rooms[name])

    def joinRoom(self, room, data = None):
        """ Joins a room in pokemon showdown.

        Args:
            room: string, name of the room
            data: dict or string, moderations settings you want to set in the
                  room.
                  example:
                    data = {'moderate': False, 'allow games': False,
                            'tourwhitelist': []}
        """
        if room in self.rooms:
            return
        self.send('|/join ' + room)
        self.rooms_markov[room] = Markov(room)
        self.rooms[room] = Room(room, data)

    def leaveRoom(self, room):
        ''' Attempts to leave a PS room

        Returns:
            True if succesful, False otherwise.
        '''
        if room not in self.rooms:
            print("""Error! {name} not in {room}

                  """.format(name = self.name, room = room))
            return False
        self.send('|/leave ' + room)
        self.rooms.pop(room, None)
        return True

    def getRoom(self, roomName):
        """Returns a the room object associated with this room.

        Args:
            roomName: string, name of the room object we want.
                example:
                'techcode'
        Returns:
            Room object. If the Room is a room we are not already in then a
                         an empty room object room object is returned.
        """
        if roomName not in self.rooms:
            return Room('Empty')
        alias = {'nu':'neverused'}
        if roomName in alias:
            roomName = alias[roomName]
        if roomName not in self.rooms:
            self.rooms[roomName] = Room(roomName)
        return self.rooms[roomName]

    def say(self, room, msg):
        """Replies with this message in the specified room.

        Args:
            room:string, room we want to send the message to.
            msg:string, message to be sent.
        """
        if '\n' in msg:
            for m in msg.split('\n'):
                self.send('{room}|{text}'.format(room=room, text=m))
        else:
            self.send('{room}|{text}'.format(room=room, text=msg))

    def sendPm(self, user, msg):
        """Sends the specified user a private message.

        Args:
            user:string, name of user.
            msg:string, message to be sent.
        """
        if '\n' in msg:
            for m in msg.split('\n'):
                self.send('|/pm {usr}, {text}'.format(usr=user, text=m))
        else:
            self.send('|/pm {usr}, {text}'.format(usr=user, text=msg))

    def reply(self, room, user, response, samePlace):
        """Replies with a response to the specified area.

        Args:
            room: string, the room we are in.
            user: user object, the user who executed this command.
            response: string, reponse after command
            samePlace: boolean, whether this message should be sent to the
                       room or the user.
        """
        if samePlace:
            self.say(room, response)
        else:
            self.sendPm(user.id, response)

    # Helpful functions
    def toId(self, thing):
        """Assigns a unique ID to everyone"""
        return re.sub(r'[^a-zA-z0-9,]', '', thing).lower()

    def escapeText(self, line):
        """Adjust message to avoid errors in the chat."""
        if line:
            if line[0] == '/':
                return '/' + line
            elif line[0] == '!':
                return ' ' + line
        return line

    def removeSpaces(self, text):
        """removes spaces from a string"""
        return text.replace(' ','')

    def extractCommand(self, msg):
        """Extracts the command character i.e. '.' from the message."""
        return msg[len(self.commandchar):].split(' ')[0].lower()

    def takeAction(self, room, user, action, reason):
        """Takes authorative(mod) action against a user."""
        self.log('Action', action, user.id)
        self.send("""{room}|/{act} {user}, {reason}
                  """.format(room = room, act = action,
                  user = user.id, reason = reason))

    def canHTMLBox(self, room):
        return User.compareRanks(room.rank, '*')

    # Rank checks
    def canPunish(self, room):
        return User.compareRanks(room.rank, '%')

    def canBan(self, room):
        return User.compareRanks(room.rank, '@')

    def canStartTour(self, room):
        return User.compareRanks(room.rank, '@')

    # Generic permissions test for users
    def isOwner(self, name):
        return self.owner == self.toId(name)


    def evalRoomPermission(self, user, room):
        return user.hasRank(room.broadcast_rank)

    def saveDetails(self, newAutojoin = False):
        """Saves the current details to the details.yaml."""
        details = {k:v for k,v in self.details.items() if not k == 'rooms' and
                   not k == 'joinRooms'}
        details['joinRooms'] = {}
        for e in self.rooms:
            # no need to save details for group chats as they expire
            if e.startswith('groupchat'):
                continue
            if not newAutojoin and e not in self.details['joinRooms']:
                continue
            room = self.getRoom(e)
            details['joinRooms'][e] = {'moderate': room.moderate,
                                       'allow games':room.allowGames,
                                       'tourwhitelist': room.tourwhitelist}
        with open('details.yaml', 'w') as yf:
            yaml.dump(details, yf, default_flow_style = False, explicit_start = True)

    # Default onMessage if none is given (This only support logging in,
    # nothing else). To get any actual use from the bot, create a custom
    # onMessage function.
    def onMessage(self, ws, message):
        """Only attempts logging in the bot.

        Args:
            ws: websocket that is using this method.
            message: string given by websocket.
        Returns:
            None.
        Raises:
            None.
        """
        if not message: return
        parts = message.split('|')
        if parts[1] == 'challstr':
            print('Attempting to log in...')
            self.login(message[3], message[2])
        elif parts[1] == 'updateuser':
            self.updateUser(parts[2], parts[3])


class ReplyObject:
    """Reply object containing important information about how to handle an
    event to a user.

    Attributes:
        text: str, text to be said to the user
        samePlace: bool, whether this message should be said in the same place
                   the event was intiated. i.e. should a command be replied to
                   in public chat or in PMs.
        ignoreEscaping: bool, ignore escape characteres like '\n'
        ignoreBroadcastPermission: bool, ignore room broadcast permissions.
        gameCommand: bool, this is a gameCommand and requires special
                     attention.
        canPmReply: bool, send this message to PMs.
    """
    def __init__(self, res = '', reply = False, escape = False,
                 broadcast = False, game = False, pmreply = False):
        self.text = res
        self.samePlace = reply
        self.ignoreEscaping = escape
        self.ignoreBroadcastPermission = broadcast
        self.gameCommand = game
        self.canPmReply = pmreply

    def __eq__(self, other):
        if type(other) == ReplyObject:
            return (self.text == other.text
                    and self.ignoreEscaping == other.ignoreEscaping
                    and self.ignoreBroadcastPermission == other.ignoreBroadcastPermission
                    and self.gameCommand == other.gameCommand
                    and self.canPmReply == other.canPmReply)
        else:
            return False

    def response(self, text):
        self.text = text
        return self
