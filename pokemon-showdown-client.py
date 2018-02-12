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
import websockets
import requests
import json
from details import ps_config as default_config 


class LoginCredentialsException(Exception):
    pass


class Client:
    """Represents a client connection that connects to PokemonShowdown.

    This class handles the major client-side connection to the PokemonShowdown
    server. It also provides an API wrapper for the basic PS commands and 
    protocols PS abides by. 

    You should expect to be somewhat familiar with the PS protocols outlined 
    here: https://github.com/Zarel/Pokemon-Showdown/blob/master/PROTOCOL.md
    if you want to make edits to the following piece of code.

    For the sake of simplicity, we assume that the command char used is ~ in 
    the documentation.

    Attributes:
        ws: websockets connection, asyncio compliant websocket client.
        rooms: map of Room, map containing all of the rooms this bot is in.
        config: dict, contains all relevant config details for the bot.
        session: session, coroutine session required for aiohttp connections.
    """
    def __init__(self, config=None, url=None):
        self.ws = None
        self.rooms = {}
        # attempt connectiong to the main PS server, unless otherwise specified
        self.config = default_config if not config else config 
        self.url = 'ws://sim.psim.us:8000/showdown/websocket' if not url else url
        self.session = aiohttp.ClientSession()

    @asyncio.coroutine
    def start_connection(self):
        """Initiates a connection to the specified showdown server."""
        try:
            self.ws = yield from websockets.connect(self.url)
            while True:
                message = yield from self.ws.recv()
                print(message)
                # Random PS boogeyman 
                if not message.startswith('|'): continue
                # Protocol messages are delimited by |
                content = message.split('|')
                event = content[1]

                if event == 'challstr':
                    challengekeyid, challenge = content[2], content[3]
                    yield from self.login(challengekeyid, challenge)
                elif event == "updateuser":
                    name, result_code = content[2], content[3]
                    yield from self.update_user(name, result_code)

        except KeyboardInterrupt:
            print('program has been terminated by program interrupt')
            yield from self.ws.close()
            self.session.close()
            exit()
        except LoginCredentialsException:
            print('Your login credentials are incorrect.')
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
            LoginCredentialsException
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
            raise LoginCredentialsException

    @asyncio.coroutine
    def update_user(self, name, result_code):
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
        # self.rooms[room] = Room(room, data)


        


client = Client()
asyncio.get_event_loop().run_until_complete(client.start_connection())
