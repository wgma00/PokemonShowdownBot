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

import asyncio
import aiohttp
import time
import websockets
import json
from details import ps_config as default_config
from room import Room
from user import User


class ClientException(Exception):
    """General wrapper for common errors encountered with API use of the client."""
    def __init__(self, reason):
        self.reason = reason

    def __str__(self):
        return self.reason


class Client:
    """Represents a client connection that connects to PokemonShowdown.

    This class handles the major client-side connection to the PokemonShowdown
    server. It also provides an API wrapper for the basic PS commands and 
    protocols PS abides by. 

    You should expect to be somewhat familiar with the PS protocols outlined below:
    https://github.com/Zarel/Pokemon-Showdown/blob/master/PROTOCOL.md
    if you want to make edits to the following piece of code.

    For the sake of simplicity, we assume that the command char used is ~ in 
    the documentation.

    Attributes:
        ws: websockets connection, asyncio compliant websocket client.
        rooms: map of Room, map containing all of the rooms this bot is in.
        config: dict, contains all relevant config details for the bot.
        session: session, coroutine session required for aiohttp connections.
        log_errors: bool, whether or not to log exceptions.
    """
    def __init__(self, config=None, url=None, log_errors=False):
        self.ws = None
        self.rooms = {}
        # attempt connectiong to the main PS server, unless otherwise specified
        self.log_errors = log_errors
        self.config = default_config if not config else config 
        self.url = 'ws://sim.psim.us:8000/showdown/websocket' if not url else url
        self.session = aiohttp.ClientSession()

    @asyncio.coroutine
    def make_connection(self):
        """Initiates a connection to the specified showdown server."""
        try:
            self.ws = yield from websockets.connect(self.url)
            while True:
                message_stream = yield from self.ws.recv()
                parsed_messages = [message_stream]  # assume the original message stream only contains one message
                room_name = 'Empty'
                print(message_stream)
                # message streams starting with > means we're provided serveral message protocols
                # delimited by new line characters
                if message_stream.startswith('>'):
                    # lines are delimited by new characters
                    lines = message_stream.split('\n')
                    # room names are always on the first line and are formatted like'>room_name'
                    room_name = lines[0][1:]
                    parsed_messages= lines[1:]
                parsed_messages = list(filter(lambda x: x != '', parsed_messages))  # remove empty lines
                for msg in parsed_messages:
                    # random prompt from PS which we don't need to interpret
                    if not msg.startswith('|'): continue
                    content = msg.split('|')
                    event = content[1].lower() # event capitalization not standardized
                    room = self.get_room(room_name) # create a new room object if we don't already have one
                    # battle rooms don't require the same interface as chatrooms or private messages
                    if room.name.startswith('battle-'):
                        message = MessageWrapper()
                        yield from self.battle_handler(message)
                    else:
                        if event == 'challstr':
                            challengekeyid, challenge = content[2], content[3]
                            yield from self.login(challengekeyid, challenge)
                        elif event == 'updateuser':
                            # attempt changing from a guest user to logged in user on showdown
                            name, result_code = content[2], content[3]
                            yield from self.update_bot(name, result_code)
                        elif event == 'c:' or event == 'chat': # chat protocol shortened to 'c' for bandwidth reasons
                            # |c:|unix_time|user| message => ['', 'c:', 'unix_time', 'user', 'message']
                            # we'll use our own unix time for now, since it's not standarized across pm's and
                            # chat messages
                            
                            unix_time, user_name, user_msg = str(int(time.time())), content[3], content[4]
                            user = User(user_name)
                            message = MessageWrapper(unix_time, user, user_msg, room, self.config)
                            # ignore messages on first loading a room, to avoid overloading on commands, and start fresh
                            if room.loaded: yield from self.chat_handler(message)
                        elif event == 'pm':
                            # |pm|user|recepient| message => ['', 'pm', 'user', 'recepient', 'message']
                            unix_time, user_name, other_name, user_msg = str(int(time.time())), content[2], content[3], content[4]
                            room.name = 'pm'  # change the room to a private message for better logging
                            user = User(user_name)
                            message = MessageWrapper(unix_time, user, user_msg, room, self.config)
                            yield from self.chat_handler(message)
                        # battle related stuff
                        elif event == 'updatechallenges':
                            # |updatechallenges|{"challengesFrom":{"wgma":"gen7randombattle", "amgw", "gen7randombattle"},"challengeTo":null}
                            challenge = json.loads(content[2])
                            if challenge['challengesFrom']:
                                opponents = [key for key in challenge['challengesFrom'].keys()]
                               # |request|{"active":[{"moves":[{"move":"Volt Switch","id":"voltswitch","pp":32,"maxpp":32,"target":"normal","disabled":false},{"move":"Focus Blast","id":"focusblast","pp":8,"maxpp":8,"target":"normal","disabled":false},{"move":"Encore","id":"encore","pp":8,"maxpp":8,"target":"normal","disabled":false},{"move":"Grass Knot","id":"grassknot","pp":32,"maxpp":32,"target":"normal","disabled":false}]}],"side":{"name":"octbot","id":"p2","pokemon":[{"ident":"p2: Raichu","details":"Raichu, L89, M","condition":"252/252","active":true,"stats":{"atk":165,"def":149,"spa":211,"spd":193,"spe":247},"moves":["voltswitch","focusblast","encore","grassknot"],"baseAbility":"lightningrod","item":"focussash","pokeball":"pokeball","ability":"lightningrod"},{"ident":"p2: Infernape","details":"Infernape, L82, M","condition":"259/259","active":false,"stats":{"atk":175,"def":164,"spa":218,"spd":164,"spe":224},"moves":["nastyplot","fireblast","vacuumwave","focusblast"],"baseAbility":"blaze","item":"fightiniumz","pokeball":"pokeball","ability":"blaze"},{"ident":"p2: Mew","details":"Mew, L80","condition":"291/291","active":false,"stats":{"atk":165,"def":206,"spa":206,"spd":206,"spe":206},"moves":["nastyplot","willowisp","psyshock","icebeam"],"baseAbility":"synchronize","item":"leftovers","pokeball":"pokeball","ability":"synchronize"},{"ident":"p2: Hitmonchan","details":"Hitmonchan, L88, M","condition":"231/231","active":false,"stats":{"atk":235,"def":189,"spa":112,"spd":244,"spe":184},"moves":["icepunch","bulkup","drainpunch","firepunch"],"baseAbility":"ironfist","item":"lifeorb","pokeball":"pokeball","ability":"ironfist"},{"ident":"p2: Arcanine","details":"Arcanine, L84, M","condition":"287/287","active":false,"stats":{"atk":233,"def":183,"spa":216,"spd":183,"spe":208},"moves":["extremespeed","flareblitz","willowisp","wildcharge"],"baseAbility":"intimidate","item":"lifeorb","pokeball":"pokeball","ability":"intimidate"},{"ident":"p2: Seismitoad","details":"Seismitoad, L86, M","condition":"321/321","active":false,"stats":{"atk":213,"def":178,"spa":195,"spd":178,"spe":177},"moves":["scald","sludgewave","earthquake","knockoff"],"baseAbility":"waterabsorb","item":"assaultvest","pokeball":"pokeball","ability":"waterabsorb"}]},"rqid":3}
                                for opp in opponents:
                                    battle_format = challenge['challengesFrom'][opp]
                                    if battle_format == 'gen7randombattle':
                                        team = ''
                                        yield from self.ws.send('|/utm {}'.format(team))
                                        yield from self.ws.send('|/accept {}'.format(opp))
                                    else:
                                        yield from self.ws.send_pm(opp, 'Sorry, I can\'t accept challnges in that format')
                        elif event == 'raw':
                            # |raw|<div class="infobox"> You joined Bot Development</div>
                            room.loaded = True
                        else:
                            print(event, 'is not implemented at the moment')

        except KeyboardInterrupt:
            print('program has been terminated by program interrupt')
            yield from self.ws.close()
            self.session.close()
            exit()
        except ClientException as e:
            print(e)
        finally:
            yield from self.ws.close()
            self.session.close()

    @asyncio.coroutine
    def login(self, challengekeyid, challenge):
        """Logins the bot to the pokemon showdown server.

        More information on how the 'challstr' protocol needs to be handled for
        the login proccess can be found in the link below 
        https://github.com/Zarel/Pokemon-Showdown/blob/master/PROTOCOL.md#global-messages.

        Args:
            challengekeyid: string, challenge key id obtained from |challstr|.
            challenge: string, challenge key obtained from |challstr|.
        Raises:
            ClientException
            username/password combination is incorrect.
        """
        url = 'http://play.pokemonshowdown.com/action.php'
        payload = {'act': 'login',
                   'name': self.config['bot_username'],
                   'pass': self.config['bot_password'],
                   'challengekeyid': challengekeyid,
                   'challenge': challenge}
        # first generate the post request content, then retrieve the relevant
        # login information we need for authentication.
        resp = yield from self.session.post(url, data=payload)
        resp = yield from resp.text()
        # can't directly convert to json since PS returns a weird format like
        # ']{json content}', so have to offset it by 1
        offset = 1
        assertion = json.loads(resp[offset:])['assertion']
        if assertion:
            yield from self.ws.send('|/trn {},0,{}'.format(self.config['bot_username'], assertion))
        else:
            raise ClientException('bot credentials are incorrect')

    @asyncio.coroutine
    def update_bot(self, name, result_code):
        """Updates the bots credentials on pokemon showdown.

        Args:
            name: string, name of the bot
            result_code: string, result code obtained from the websocket once 
                        user has been authenticated.
        """
        # we're still a guest user, so disregard this update user protocol
        if result_code == '0':
            return
        if self.config['avatar'] >= 0:
            yield from self.ws.send('|/avatar {num}'.format(num=self.config['avatar']))
        # add rooms that were prefined in our cofiguration file
        for room in self.config['join-rooms']:
            yield from self.join_room(room, self.config['join-rooms'][room])

    @asyncio.coroutine
    def join_room(self, room, room_setting):
        """ Joins a room on pokemon showdown.

        Note: We don't need to do error checking for rooms that don't exist 
        since PS handles this client side (i.e. you can't invite to rooms that don't exist)

        Args:
            room: string, name of the room
            room_setting: dict, moderation settings you want to set in this room.
                  example: data = {'moderate': False, 'allow games': False, 'tourwhitelist': []}
        """
        # if room in self.rooms: return
        yield from self.ws.send('|/join ' + room)
        self.rooms[room] = Room(room, room_setting)

    @asyncio.coroutine
    def send(self, message):
        """Sends a message through the websocket."""
        yield from self.ws.send(message)

    @asyncio.coroutine
    def send_pm(self, user, message):
        """Sends the specified user a private message.
        Args:
            user:string, name of user.
            msg:string, message to be sent.
        """
        parsed_messages = message.split('\n') if '\n' in message else [message]
        for msg in parsed_messages:
            content = '|/pm {user}, {msg}'.format(user=user, msg=msg)
            yield from self.ws.send(content)

    @asyncio.coroutine
    def send_room(self, room_name, message):
        """Replies in specified chat room with message; message can be delimited with newlines.
        Args:
            room_name: string, room we want to send the message to.
            message: string, message to be sent.
        """
        parsed_messages = message.split('\n') if '\n' in message else [message]
        for msg in parsed_messages:
            yield from self.send('{room}|{msg}'.format(room_name=room_name, msg=msg))

    def event(self, coro):
        """ Decorator for the main functions required by the API.

        Args:
            coro: function, function/coroutine to be used in place of default coroutines.
        Raises:
            ClientException
            Providing a function that is not a couroutine or providing a function that is not
            a valid coroutine required for the API.
        """
        if not asyncio.iscoroutinefunction(coro):
            raise ClientException('event registered must be a coroutine function')
        if coro.__name__ not in ['chat_handler', 'battle_handler']:
            raise ClientException('This is not a valid coroutine required for the API.')
        setattr(self, coro.__name__, coro)
        return coro

    @asyncio.coroutine
    def chat_handler(self, message):
        """
        """
        raise NotImplementedError

    @asyncio.coroutine
    def battle_handler(self, message):
        """
        """
        raise NotImplementedError

    def get_room(self, room_name):
        """Returns a the room object associated with this room.

        Note that this also handles room aliases for certain public rooms.

        Args:
            room_name: string, name of the room to look for i.e. 'techcode'
        Returns:
            Room object. If the Room is a room we are not already in then a
                         an empty room object room object is returned.
        """
        if room_name not in self.rooms:
            return Room('Empty')
        alias = {'nu': 'neverused', 'tc' : 'techcode'}
        if room_name in alias:
            room_name = alias[room_name]
        if room_name not in self.rooms:
            self.rooms[room_name] = Room(room_name)
        return self.rooms[room_name]


class MessageWrapper:
    """Message wrapper with several utilities for getting information from a message

    Attributes:
        unix_time: str, string containing the unix time of the message since 1970.
        user: user object, user object from the user to send this message.
        content: str, content of the message that was sent.
        room: room object, the room this message was sent from.
        _config: config object containing bot details.
        is_pm: bool, verify if this message is a private message or not.
    """
    def __init__(self, unix_time, user, content, room, config):
        self.unix_time = unix_time
        self.user = user
        self.content = content
        self.room = room
        self._config = config
        self.is_pm = room.name == 'pm'

    def from_self(self):
        """Determines if this message was from the bot instance itself."""
        return self.user.name == self._config['bot_username']

    def requests_command(self):
        """Determines if the message sent by the user starts with a command character."""
        return self.content.startswith(self._config['command_char'])

    def __str__(self):
        # |c:|unix_time|user| message => ['c:', 'unix_time', 'user', 'message']
        # or
        # |pm|user| message => ['pm', 'user', 'message']
        prt = 'pm' if self.is_pm else 'c:'
        return '|{prt}|{time}|{user}|{msg}'.format(prt, self.unix_time, self.user.id, self.content)

class BattleMessageWrapper:
    """Message wrapper with several utilities for getting information from a message

    Attributes:
        unix_time: str, string containing the unix time of the message since 1970.
        user: user object, user object from the user to send this message.
        content: str, content of the message that was sent.
        room: room object, the room this message was sent from.
        _config: config object containing bot details.
        is_pm: bool, verify if this message is a private message or not.
    """
    def __init__(self, unix_time, user, content, room, config):
        self.unix_time = unix_time
        self.user = user
        self.content = content
        self.room = room
        self._config = config
        self.is_pm = room.name == 'pm'

    def from_self(self):
        """Determines if this message was from the bot instance itself."""
        return self.user.name == self._config['bot_username']

    def requests_command(self):
        """Determines if the message sent by the user starts with a command character."""
        return self.content.startswith(self._config['command_char'])

    def __str__(self):
        # |c:|unix_time|user| message => ['c:', 'unix_time', 'user', 'message']
        # or
        # |pm|user| message => ['pm', 'user', 'message']
        prt = 'pm' if self.is_pm else 'c:'
        return '|{prt}|{time}|{user}|{msg}'.format(prt, self.unix_time, self.user.id, self.content)


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
    def __init__(self, res='', reply=False, escape=False, broadcast=False, game=False, pmreply=False):
        self.text = str(res)
        self.samePlace = reply
        self.ignoreEscaping = escape
        self.ignoreBroadcastPermission = broadcast
        self.gameCommand = game
        self.canPmReply = pmreply

    def __eq__(self, other):
        if type(other) == Reply:
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

