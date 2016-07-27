# The MIT License (MIT)
#
# Copyright (c) 2015 QuiteQuiet
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

from random import randint
from random import sample
import re
import os
import math

from data.tiers import tiers
from data.tiers import formats
from data.links import Links
from data.links import YoutubeLinks
from data.pokedex import Pokedex
from data.types import Types
from data.replies import Lines
from plugins.math import equation
from user import User
from room import RoomCommands
from plugins import PluginCommands
from plugins import IgnoreEscaping
from plugins import GameCommands
from plugins import IgnoreBroadcastPermission
from plugins.math.latex import latex
from plugins.math.clever import Clever

ExternalCommands = RoomCommands.copy()
ExternalCommands.update(PluginCommands)

usageLink = r'http://www.smogon.com/stats/2016-04/'
CanPmReplyCommands = ["usage", "help"]
IgnoreBroadcastPermission.append("tour")


def URL():
    """URL for the source code"""
    return "https://github.com/wgma00/PokemonShowdownBot/"


def Command(self, cmd, room, msg, user, room_name=None, markov_db=None):
    """ Handles commands given by the chat parser.
    
    Better documentation of the commands can be found in the COMMANDS.md file.

    Args:
        self: PSBot object of the main program.
        cmd: string represnting the command the user wants to be done.
        room: Room object that this command was posted in.
        msg: the remaning message after this command.
        user: User object that initiated this command.
        room_name: Name of the room that this command was initiated in.
        markov_db: Connection to the Markov database for recording messages
                   to improve grammar of sentences formed.
    Returns:
        Returns a pair indicating first,  the result of the command(output)
        and the second a Boolean representing one of the following: 
       
        True: Allows that the command in question can, if gotten from a room,
              be returned to the same room rather than a PM.
        False: This will ALWAYS return the reply as a PM, no matter where it 
               came from.
        example:

         ("Credits can be found: {url}".format(url = URL()), True)
         ("Source code can be found at: {url}".format(url = URL()), False)

    Raises:
        Exception: there was likely improper input in the .calc command
    """
    if cmd in ["source", "git"]:
        return "Source code can be found at: {url}".format(url=URL()), False

    if cmd == "credits":
        return "Credits can be found: {url}".format(url=URL()), True

    if cmd == "latex":
        ltx = latex()
        print("test")
        if not ltx.validateRequest(msg):
            return "invalid latex expression", False
        else:
            url_upload = ltx.handleRequest(msg)
            return url_upload, True

    if cmd == "test":
        return "test", True

    if cmd == "dune": 
        dune = ["A secret report within the Guild.","Four planets have come to our attention … regarding a plot which could jeopardize spice production. Planet Arrakis, source of the spice.","Planet Caladan, home of House Atreides. Planet Giedi Prime, home of House Harkonnen. Planet Kaitain, home of the Emperor of the Known Universe.","Send a third stage Guild Navigator to Kaitain to demand details from the Emperor. The spice must flow…","https://www.youtube.com/watch?v=E_fzSc_i0Tc"]
        return dune[int(msg)], True

    if cmd == "clever":
        return self.clever_bot.reply(), True

    if cmd == "reset":
        self.clever_bot = Clever()
        return "reset", True

    if cmd == "m":
        if (markov_db is not None and room_name is not None and
                room_name in markov_db):
            return markov_db[room_name].generateText(), True
        else:
            return "sorry, there is no data for this room.", False

    if cmd == "calc":
        try:
            return str(equation.solve(msg)), True
        except Exception:
            return "Arithmetic error or unrecognized symbols", False

    if cmd == "owner":
        return "Owned by: {owner}".format(owner=self.owner), True

    if cmd in ["commands", "help"]:
        return ("Read about commands here: {url}blob/master/"
                "COMMANDS.md").format(url=URL()), True

    if cmd == "explain":
        return "Inspired by dubsbot, this bot is twice as good", True

    if cmd == "leave":
        msg = self.removeSpaces(msg)
        if not msg:
            msg = room.title

        if (user.isOwner() or user.hasRank("#")) and self.leaveRoom(msg):
            return "Leaving room {r} succeeded".format(r=msg), False
        elif not (user.isOwner() or user.hasRank("#")):
            return "You do not have adaquate permissions", False

        return "Could not leave room: {r}".format(r=msg), False

    if cmd == "get":
        if user.isOwner():
            return str(eval(msg)), True
        return ("You do not have permisson to use this command."
                " (Only for owner)"), False

    # Save current self.details to details.yaml (moves rooms to joinRooms)
    # Please note that this command will remove every comment from
    # details.yaml, if those exist.
    if cmd == "savedetails":
        if user.hasRank("#"):
            self.saveDetails()
            return "Details saved.", True
        return ("You don't have permission to save settings."
                " (Requires #)"), False


    if cmd == "broadcast":
        if room.title != "pm":
            return ("Rank required to broadcast: {rank}"
                    "").format(rank=room.broadcast_rank), True
        else:
            return "No broadcast ranks in Pms", False

    if cmd == "setbroadcast":
        if room.title != "pm":
            msg = self.removeSpaces(msg)
            if msg in User.Groups or msg in ["off", "no", "false"]:
                if user.hasRank("#"):
                    if msg in ["off", "no", "false"]:
                        msg = " "
                    room.broadcast_rank = msg
                    return ("Local broadcast rank set to {rank}. (This is not"
                            " saved on reboot)").format(rank=msg), True
                return ("You are not allowed to set broadcast rank."
                        " (Requires #)"), False
            return "{rank} is not a valid rank".format(rank=msg), False
        else:
            return "No broadcast ranks in Pms", False


    # External commands from plugins (and also room.py)
    if cmd in ExternalCommands.keys():
        return ExternalCommands[cmd](self, cmd, room, msg, user)

    # Informational commands
    if cmd in Links:
        msg = msg.lower()
        if msg in Links[cmd]:
            return Links[cmd][msg], True
        return ("{tier} is not a supported format for {command}"
                "").format(tier=msg, command=cmd), True

    if cmd == "usage":
        return usageLink, True

    # Fun stuff
    if cmd == "pick":
        options = msg.split(",")
        return options[randint(0, (len(options)-1))], True

    if cmd == "ask":
        return Lines[randint(0, len(Lines)-1)], True

    if cmd == "squid":
        return "\u304f\u30b3\u003a\u5f61", True

    if cmd in YoutubeLinks:
        return YoutubeLinks[cmd], True

    if cmd in tiers:
        pick = list(tiers[cmd])[randint(0, len(tiers[cmd])-1)]
        pNoForm = re.sub("-(?:Mega(?:-(X|Y))?|Primal)", "", pick).lower()
        return ("{poke} was chosen: http://www.smogon.com/dex/xy/pokemon/"
                "{mon}/").format(poke=pick, mon=pNoForm), True

    if cmd in [t.replace("poke", "team") for t in tiers]:
        team = set()
        hasMega = False
        attempts = 0
        while len(team) < 6 or not acceptableWeakness(team):
            tier_list = tiers[cmd.replace("team", "poke")]
            poke = list(tier_list)[randint(0, len(tier_list)-1)]
            # Test if share dex number with anything in the team
            if [p for p in team if Pokedex[poke]["dex"] == Pokedex[p]["dex"]]:
                continue
            if hasMega:
                continue
            team |= {poke}
            if not acceptableWeakness(team):
                team -= {poke}
            elif "-Mega" in poke:
                hasMega = True
            if len(team) >= 6:
                break
            attempts += 1
            if attempts >= 100:
                # Prevents locking up if a pokemon turns the team to an
                # impossible generation. Since the team is probably bad anyway,
                # just finish it and exit
                while len(team) < 6:
                    tier_list = tiers[cmd.replace("team", "poke")]
                    team |= {list(tier_list)[randint(0, len(tier_list)-1)]}
                break
        return " / ".join(list(team)), True

    if cmd in formats:
        return ("Format: http://www.smogon.com/dex/xy/formats/{tier}/"
                "").format(tier=cmd), True

    # This command is here because it's an awful condition, so try it last :/
    rgx = "-(?:mega(?:-(x|y))?|primal|xl|l)"
    if [p for p in Pokedex if re.sub(rgx, "", cmd, flags=re.I)
            in p.replace(" ", "").lower()]:
        cmd = re.sub("-(?:mega(?:-(x|y))?|primal)", "", cmd)
        # This doesn't break Arceus-Steel like adding |S to the regex would
        # and gourgeist-s /pumpkaboo-s still get found, because it matches the
        # entry for gougeist/pumpkaboo-super
        substitutes = {"gourgeist-s": "gourgeist-small",
                       "gourgeist-l": "gourgeist-large",
                       "gourgeist-xl": "gourgeist-super",
                       "pumpkaboo-s": "pumpkaboo-small",
                       "pumpkaboo-l": "pumpkaboo-large",
                       "pumpkaboo-xl": "pumpkaboo-super",
                       "giratina-o": "giratina-origin",
                       "mr.mime": "mr_mime",
                       "mimejr.": "mime_jr"}
        if cmd.lower() not in (self.removeSpaces(p).lower() for p in Pokedex):
            return "{cmd} is not a valid command".format(cmd=cmd), True

        if cmd in substitutes:
            cmd = substitutes[cmd]

        return ("Analysis: http://www.smogon.com/dex/xy/pokemon/{mon}/"
                "").format(mon=cmd), True

    return "{command} is not a valid command.".format(command=cmd), False


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
