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


# The command file for every external command not specifically for running the
# bot. Even more relevant commands like broadcast options are treated as such.
#
# Information passed from the chat-parser:
#   self: The program object itself.
#
#   cmd: Contains what command was used.
#
#   msg: This hold everything else that was passed with the command, such as
#        optional parameters.
#
#   room: What room the command was used in. If the command was sent in a pm,
#         room will contain: 'Pm'. See room.py for more details.
#
#   user: A user object like the one described in the app.py file

import random
import re
import time

import requests

from data.links import Links
from data.links import YoutubeLinks
from data.pokedex import Pokedex
from data.replies import Lines
from data.tiers import formats
from data.tiers import tiers
from data.types import Types
from plugins import PluginCommands
from plugins.images import OnlineImage
from plugins.math import equation
from plugins.math.Latex import Latex
from plugins.math.partyparrot import PartyParrot
from plugins.math.putnam import LatexParsingException
from plugins.math.putnam import Putnam
from robot import ReplyObject
from room import RoomCommands
from user import User

ExternalCommands = RoomCommands.copy()
ExternalCommands.update(PluginCommands)

usageLink = r'http://www.smogon.com/stats/2017-06/'


def URL():
    """URL for the source code"""
    return "https://github.com/wgma00/quadbot/"


def Command(self, cmd, room, msg, user):
    """ Handles commands given by the chat parser.

    Better documentation of the commands can be found in the COMMANDS.md file.

    Args:
        self: PSBot object of the main program.
        cmd: string representing the command the user wants to be done.
        room: Room object that this command was posted in.
        msg: the remaining message after this command.
        user: User object that initiated this command.
    Returns:
        Returns a Reply object a differing reply object depending on the
        nature of the command.
    Raises:
        Exception: There was likely improper input in the .calc command or
                   something I entirely missed lol.
    """
    # This handles the abuse of RTL override

    if cmd == "test":
        return ReplyObject("test", True)

    if cmd == 'send' and user.isOwner():
        self.send(msg)
        return ReplyObject(msg, True, True)

    if cmd in ["source", "git", "credits"]:
        return ReplyObject(("Source code can be found at: {url}").format(url=URL()))

    if cmd == "latex":
        if not Latex.validate_request(msg):
            return ReplyObject("invalid latex expression")
        else:
            uploaded_image_data = Latex.handle_request(msg)
            uploaded_image = uploaded_image_data[0]
            uploaded_image_dims = uploaded_image_data[1]
            if User.compareRanks(room.rank, '*'):
                # don't render to 100% of screen because latex renders badly
                return ReplyObject('/addhtmlbox <img src="{url}" height="{height}" width="{width}"></img>'.format(url=uploaded_image, height=uploaded_image_dims[1], width=uploaded_image_dims[0]),True, True)
            else:
                return ReplyObject(uploaded_image, True)

    if cmd == 'machine':
        return ReplyObject("I am the machine!", True)

    if cmd == "dilbert":
        return ReplyObject(('http://dilbert.com/strip/')+time.strftime("%Y-%m-%d"), True)

    if cmd == "xkcd":
        r = requests.get('http://xkcd.com/info.0.json')
        data = r.json()
        uploaded_image = data['img']
        uploaded_image_dims = OnlineImage.get_image_info(uploaded_image)
        alt_data = data['alt']
        if msg and msg == 'rand':
            msg = random.randint(1, data['num'])
            r = requests.get('http://xkcd.com/{num}/info.0.json'.format(num=int(msg)))
            data = r.json()
            uploaded_image = data['img']
            uploaded_image_dims = OnlineImage.get_image_info(uploaded_image)
            alt_data = data['alt']
        elif msg and msg.isdigit() and int(msg) >= 1 and int(msg) <= data['num']:
            r = requests.get('http://xkcd.com/{num}/info.0.json'.format(num=int(msg)))
            data = r.json()
            uploaded_image = data['img']
            uploaded_image_dims = OnlineImage.get_image_info(uploaded_image)
            alt_data = data['alt']
        elif msg is not '':
            print(msg)
            return ReplyObject('Please select a valid xkcd article from 1 to {num} or use rand to generate a random one'.format(num=data['num']), True)
        
        if User.compareRanks(room.rank, '*'):
            return ReplyObject('/addhtmlbox <img src="{url}" height=100% width=100%></img><br><b>{alt}</b></br>'.format(alt=alt_data, url=uploaded_image, width=uploaded_image_dims[0]),True, True)
        else:
            return ReplyObject(uploaded_image, True)

    if cmd in ['partyparrot', 'pp', 'parrot', 'party']:
        if msg == 'help':
            return ReplyObject('http://cultofthepartyparrot.com/', True)
        else:
            uploaded_image_data = PartyParrot.random_parrot()
            if PartyParrot.get_parrot(msg):
                uploaded_image_data = PartyParrot.get_parrot(msg)
            uploaded_image = uploaded_image_data[0]
            uploaded_image_dims = uploaded_image_data[1]
            if User.compareRanks(room.rank, '*'):
                return ReplyObject('/addhtmlbox <img src="{url}" height="{height}" width={width}></img>'.format(
                                   url=uploaded_image, height=uploaded_image_dims[1], width=uploaded_image_dims[0]),True, True)
            else:
                return ReplyObject(uploaded_image, True)

    if cmd == 'jetfuel':
        return ReplyObject('/me pours jetfuel on SteelEdges', True, True)

    if cmd in ["dingram"]:
        output = ["rocks", "sucks", "chupa", "succhia"]
        return ReplyObject(random.choice(output),True)

    if cmd == "putnam":
        try:
            p = Putnam()
        except LatexParsingException:
            return ReplyObject("I dun goofed", True)
        else:
            return ReplyObject(p.upload_random_problem(), True)

    if cmd == "dune":
        dune = ["A secret report within the Guild.\n",
                ("Four planets have come to our attention … regarding a plot"
                 " which could jeopardize spice production. Planet Arrakis,"
                 " source of the spice.\n"),
                ("Planet Caladan, home of House Atreides. Planet Giedi Prime,"
                 " home of House Harkonnen. Planet Kaitain, home of the "
                 "Emperor of the Known Universe.\n"),
                ("Send a third stage Guild Navigator to Kaitain to demand "
                 "details from the Emperor. The spice must flow…\n"),
                "https://www.youtube.com/watch?v=nJ_ysxBi_O0\n"]
        return ReplyObject(dune[0]+dune[1]+dune[2]+dune[3]+dune[4], True)


    if cmd == "calc":
        if "," in msg:
            msg = msg.split(",")
            return ReplyObject(str(equation.solve(msg[0],msg[1])), True)
        else:
            return ReplyObject(str(equation.solve(msg)), True)

    if cmd == "owner":
        return ReplyObject("Owned by: {owner}".format(owner=self.owner), True)

    if cmd in ["commands", "help"]:
        return ReplyObject(("Read about commands here: {url}wiki/Commands").format(url=URL()), True)

    if cmd == "explain":
        return ReplyObject('Inspired by dubsbot, this bot is twice as good', True)

    if cmd == 'leave':
        msg = self.removeSpaces(msg)
        if not msg: msg = room.title
        if self.leaveRoom(msg):
            return ReplyObject('Leaving room {r} succeeded'.format(r = msg))
        return ReplyObject('Could not leave room: {r}'.format(r = msg))

    if cmd == 'get':
        if user.isOwner():
            res = str(eval(msg))
            return ReplyObject(res if not res is None else '', True)
        return ReplyObject('You do not have permisson to use this '
                           'command. (Only for owner)')
    if cmd == 'forcerestart':
        if user.hasRank('#'):
            # Figure out how to do this
            self.closeConnection()
            return ReplyObject('')
        return ReplyObject('You do not have permisson to use this command.'
                           ' (Only for owner)')
    # Save current self.details to details.yaml (moves rooms to joinRooms)
    # Please note that this command will remove every comment from
    # details.yaml, if those exist.
    if cmd == 'savedetails':
        if user.hasRank('#'):
            self.saveDetails()
            return ReplyObject('Details saved.', True)
        return ReplyObject("You don't have permission to save settings."
                           "(Requires #)")

    if cmd == 'newautojoin':
        if user.hasRank('#'):
            # Join the room before adding it to list of autojoined rooms
            self.joinRoom(msg)
            self.saveDetails(True)
            return ReplyObject("New autojoin ({room}) added.".format(room=msg))
        return ReplyObject("You don't have permission to save settings."
                           " (Requires #)")
    # Permissions
    if cmd == 'broadcast':
        if not room.isPM:
            return ReplyObject(("Rank required to broadcast: {rank}"
                                "").format(rank=room.broadcast_rank), True)
        else:
            return ReplyObject("No broadcast ranks in PMs")

    if cmd == 'setbroadcast':
        msg = self.removeSpaces(msg)
        if msg in User.Groups or msg in ['off', 'no', 'false']:
            if user.hasRank('#'):
                if msg in ['off', 'no', 'false']: msg = ' '
                if room.broadcast_rank == msg:
                    return ReplyObject('Broadcast rank is already {rank}'.format(rank = msg if not msg == ' ' else 'none'), True)
                room.broadcast_rank = msg
                return ReplyObject('Broadcast rank set to {rank}. (This is not saved on reboot)'.format(rank = msg if not msg == ' ' else 'none'), True)
            return ReplyObject('You are not allowed to set broadcast rank. (Requires #)')
        return ReplyObject('{rank} is not a valid rank'.format(rank = msg if not msg == ' ' else 'none'))

    # External commands from plugins (and also room.py)
    try:
        return ExternalCommands[cmd](self, cmd, room, msg, user)
    except KeyError as ke:
        # Do nothing, it's expected some commands doesn't exist
        pass
    except Exception as e:
        # Something else went wrong D:
        return ReplyObject(e)

    # Informational commands
    if cmd in Links:
        msg = msg.lower()
        if msg in Links[cmd]:
            return ReplyObject(Links[cmd][msg], True)
        return ReplyObject(('{tier} is not a supported format for {command}'
                            '').format(tier=msg, command=cmd), True)
    if cmd == 'usage':
        return ReplyObject(usageLink, True, False, False, False, True)
    # Fun stuff
    if cmd == 'pick':
        options = msg.split(',')
        return ReplyObject(options[random.randint(0,(len(options) - 1))], True)
    if cmd == 'ask':
        return ReplyObject(Lines[random.randint(0, len(Lines) - 1)], True)
    if cmd == 'seen':
        return ReplyObject("This is not a command because I value other users privacy.", True)
    if cmd == 'squid':
        return ReplyObject('\u304f\u30b3\u003a\u5f61', True)
    if cmd in YoutubeLinks:
        return ReplyObject(YoutubeLinks[cmd], True)
    if cmd in tiers:
        pick = list(tiers[cmd])[random.randint(0,len(tiers[cmd])-1)]
        pNoForm = re.sub('-(?:Mega(?:-(X|Y))?|Primal)','', pick).lower()
        return ReplyObject(('{poke} was chosen: http://www.smogon.com/dex/xy/'
                            'pokemon/{mon}/').format(poke=pick, mon=pNoForm),
                            True)
    if cmd in [t.replace('poke','team') for t in tiers]:
        team = set()
        hasMega = False
        attempts = 0
        while len(team) < 6 or not acceptableWeakness(team):
            poke = list(tiers[cmd.replace('team','poke')])
            poke = poke[random.randint(0, len(tiers[cmd.replace('team','poke')])-1)]
            # Test if share dex number with anything in the team
            if [p for p in team if Pokedex[poke]['num'] == Pokedex[p]['num']]:
                continue
            if hasMega and '-Mega' in poke:
                continue
            team |= {poke}
            if not acceptableWeakness(team):
                team -= {poke}
            elif '-Mega' in poke:
                hasMega = True
            if len(team) >= 6:
                break
            attempts += 1
            if attempts >= 100:
                # Prevents locking up if a pokemon turns the team to an
                # impossible genration. Since the team is probably bad anyway,
                # just finish it and exit
                while len(team) < 6:
                    teams = list(tiers[cmd.replace('team','poke')])
                    seed = len(tiers[cmd.replace('team','poke')])-1
                    rand_team = [random.randint(0, seed)]
                    team |= {rand_team}
                break
        return ReplyObject(' / '.join(list(team)), True)
    if cmd in formats:
        return ReplyObject(('Format: http://www.smogon.com/dex/xy/formats/'
                            '{tier}/').format(tier = cmd), True)
    # This command is here because it's an awful condition, so try it last :/
    pkmn_name_regex = re.sub('-(?:mega(?:-(x|y))?|primal|xl|l)$','', cmd, flags=re.I) 
    if filter(lambda p: pkmn_name_regex in self.removespaces(p).lower(), [p for p in Pokedex]):
        cmd = re.sub('-(?:mega(?:-(x|y))?|primal)','', cmd)
        # This doesn't break Arceus-Steel like adding |S to the regex would
        # and gourgeist-s /pumpkaboo-s still get found, because it matches the
        # entry for gougeist/pumpkaboo-super
        substitutes = {'gourgeist-s':'gourgeist-small',
                       'gourgeist-l':'gourgeist-large',
                       'gourgeist-xl':'gourgeist-super',
                       'pumpkaboo-s':'pumpkaboo-small',
                       'pumpkaboo-l':'pumpkaboo-large',
                       'pumpkaboo-xl':'pumpkaboo-super',
                       'giratina-o':'giratina-origin',
                       'mr.mime':'mr_mime',
                       'mimejr.':'mime_jr'
        }
        # Just in case do a double check before progressing...
        if cmd.lower() not in (self.removeSpaces(p).lower() for p in Pokedex):
            return ReplyObject('{cmd} is not a valid command'.format(cmd = cmd), True)
        if cmd in substitutes:
            cmd = substitutes[cmd]
        if msg not in ('rb', 'gs', 'rs', 'dp', 'bw', 'xy', 'sm'):
            msg = 'sm'
        if self.canHtml(room):
            return ReplyObject('/addhtmlbox <a href="http://www.smogon.com/dex/{gen}/pokemon/{mon}/">{capital} analysis</a>'.format(gen = msg, mon = cmd, capital = cmd.title()), True, True)
        return ReplyObject('Analysis: http://www.smogon.com/dex/{gen}/pokemon/{mon}/'.format(gen = msg, mon = cmd), reply = True, pmreply = True)

    return ReplyObject('{command} is not a valid command.'.format(command=cmd))

def acceptableWeakness(team):
    """ Determines a threshold for a teams weakness to all possible types

    Args:
        team: list of string.
    Returns:
        Returns true if the team is below the threshold, false otherwise.
    Raises:
        None.
    """
    if not team:
        return False
    comp = {t: {"weak": 0, "res": 0} for t in Types}
    for poke in team:
        types = Pokedex[poke]["types"]
        if len(types) > 1:
            for matchup in Types:
                eff = Types[types[0]][matchup]*Types[types[1]][matchup]
                if eff > 1:
                    comp[matchup]["weak"] += 1
                elif eff < 1:
                    comp[matchup]["res"] += 1
        else:
            for matchup in Types:
                if Types[types[0]][matchup] > 1:
                    comp[matchup]["weak"] += 1
                elif Types[types[0]][matchup] < 1:
                    comp[matchup]["res"] += 1
    for t in comp:
        if comp[t]["weak"] >= 3:
            return False
        if comp[t]["weak"] >= 2 and comp[t]["res"] <= 1:
            return False
    return True
