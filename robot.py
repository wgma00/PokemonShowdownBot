# The MIT License (MIT)
#
# Copyright (c) 2015
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
import yaml
from time import sleep
import datetime
import re

from room import Room
from user import User
from plugins.battling.battleHandler import BattleHandler

class PokemonShowdownBot:
    ''' Controls the most basic aspects of connecting to Pokemon Showdown 
        as well as commands.
    '''

    def __init__(self, url, onMessage = None):
        '''(PokemonShowdownBot, str, fcn) -> None'''
        with open("details.yaml", 'r') as yaml_file:
            self.details = yaml.load(yaml_file)
            self.owner = self.toId(self.details['master'])
            self.name = self.details['user']
            self.id = self.toId(self.name)
            self.rooms = {}
            self.commandchar = self.details['command']
            self.intro()
            self.splitMessage = onMessage if onMessage else self.onMessage
            self.url = url
            #websocket.enableTrace(True)
            self.openWebsocket()
            self.addBattleHandler()

    def onError(self, ws, error):
        '''(PokemonShowdownBot, websocket, str) -> None'''
        print('Websocket Error:', error)

    def onClose(self, message):
        '''(PokemonShowdownBot, str) -> None'''
        print('Websocket closed')

    def onOpen(self, message):
        '''(PokemonShowdownBot, str) -> None'''
        print('Websocket opened')

    def openWebsocket(self):
        '''(PokemonShowdownBot) -> None'''
        self.ws = websocket.WebSocketApp(self.url,
                                         on_message = self.splitMessage,
                                         on_error = self.onError,
                                         on_close = self.onClose)
        self.ws.on_open = self.onOpen

    def addBattleHandler(self):
        '''(PokemonShowdownBot) -> None'''
        self.bh = BattleHandler(self.ws, self.name)

    def intro(self):
        '''(PokemonShowdownBot) -> None'''
        print('+~~~~~~~~~~~~~~~~~~~~~~~~+')
        print('|  Pokemon Showdown Bot  |')
        print('|      Created by:       |')
        print('|      Quite Quiet       |')
        print('|      Contributor:      |')
        print('|      wgma00            |')
        print('+~~~~~~~~~~~~~~~~~~~~~~~~+')

    def log(self, sort, msg, user):
        '''(PokemonShowdownBot, str, str, User) -> None'''
        print("""{sort}: {cmd} (user: {user})
              """.format(sort=sort, cmd=msg, user=user))

    def userIsSelf(self, user):
        '''(PokemonShowdownBot, User) -> Bool'''
        return self.name == user

    def send(self, msg):
        '''(PokemonShowdownBot, str) -> None'''
        self.ws.send(msg)

    def login(self, challenge, challengekeyid):
        payload = { 'act':'login',
                    'name': self.name,
                    'pass': self.details['password'],
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
        if self.name not in name: return
        if not result == '1':
            print('login failed, still guest')
            print('crashing now; have a nice day :)')
            exit()

        if self.details['avatar'] >= 0:
            self.send('|/avatar {num}'.format(num = self.details['avatar']))
        print('{name}: Successfully logged in.'.format(name = self.name))
        for rooms in self.details['joinRooms']:
            name = [n for n in rooms][0] # joinRoom entry is a list of dicts
            self.joinRoom(name, rooms[name])

    def joinRoom(self, room, data = None):
        self.send('|/join ' + room)
        self.rooms[room] = Room(room, data)

    def leaveRoom(self, room):
        ''' Attempts to leave a PS room '''
        if room not in self.rooms:
            print("""Error! {name} not in {room}
                  """.format(name = self.name, room = room))
            return False
        self.send('|/leave ' + room)
        self.rooms.pop(room, None)
        return True

    def getRoom(self, roomName):
        if roomName not in self.rooms: return Room('Empty')
        alias = {'nu':'neverused', 'tsb':'thestable'}
        if roomName in alias:
            roomName = alias[roomName]
        return self.rooms[roomName]

    def say(self, room, msg):
        if '\n' in msg:
            for m in msg.split('\n'):
                self.send('{room}|{text}'.format(room = room, text = m))
        else:
            self.send('{room}|{text}'.format(room = room, text = msg))

    def sendPm(self, user, msg):
        if '\n' in msg:
            for m in msg.split('\n'):
                self.send('|/pm {usr}, {text}'.format(usr = user, text = m))
        else:
            self.send('|/pm {usr}, {text}'.format(usr = user, text = msg))

    def reply(self, room, user, response, samePlace):
        if samePlace:
            self.say(room, response)
        else:
            self.sendPm(user.id, response)

    # Helpful functions
    def toId(self, thing):
        return re.sub(r'[^a-zA-z0-9,]', '', thing).lower()

    def escapeText(self, line):
        if line[0] == '/':
            return '/' + line
        elif line[0] == '!':
            return ' ' + line
        return line
    def removeSpaces(self, text):
        return text.replace(' ','')

    def extractCommand(self, msg):
        return msg[len(self.commandchar):].split(' ')[0].lower()

    def takeAction(self, room, user, action, reason):
        self.log('Action', action, user.id)
        self.send("""{room}|/{act} {user}, {reason}
                  """.format(room = room, act = action,
                  user = user.id, reason = reason))

    # Rank checks
    def canPunish(self, room):
        return User.Groups[room.rank] >= User.Groups['%']

    def canBan(self, room):
        return User.Groups[room.rank] >= User.Groups['@']

    def canStartTour(self, room):
        return User.Groups[room.rank] >= User.Groups['@']

    # Generic permissions test for users
    def isOwner(self, name):
        return self.owner == self.toId(name)

    def evalPermission(self, user):
        return User.Groups[user.rank] >= User.Groups[self.details['broadcastrank']] or self.isOwner(user.id)

    def userHasPermission(self, user, rank):
        return self.isOwner(user.id) or User.Groups[user.rank] >= User.Groups[rank]

    def saveDetails(self):
        details = {k:v for k,v in self.details.items() if not k == 'rooms' and 
                   not k == 'joinRooms'}
        details['joinRooms'] = []
        for e in self.rooms:
            room = self.getRoom(e)
            details['joinRooms'].append({e:{'moderate':room.moderate,
                                            'allow games':room.allowGames,
                                            'tourwhitelist':room.tourwhitelist}
                                        })
        details['rooms'] = {}
        with open('details.yaml', 'w') as yf:
            yaml.dump(details, yf, default_flow_style = False)

    # Default onMessage if none is given (This only support logging in,
    # nothing else). To get any actual use from the bot, create a custom 
    # onMessage function.
    def onMessage(self, ws, message):
        if not message: return
        parts = message.split('|')
        if parts[1] == 'challstr':
            print('Attempting to log in...')
            self.login(message[3], message[2])
        elif parts[1] == 'updateuser':
            self.updateUser(parts[2], parts[3])

