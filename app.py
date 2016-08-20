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




# Extended notes:
# user:
#     user objects are objects containing some information about the user who
#     said anything. This information consists of user.id, user.rank, and
#     user.name. user.id is a format-removed id of the speaker with only a-z
#     lowercase and 0-9 present.
#
#     user.rank contain the auth level of the user, as a single character
#     string of either ' ', +, %, @, &, #, or ~. To compare groups against each
#     other self.Groups have the information required when used like:
#     User.Groups[user.rank] for a numeric value.
#
#     Lastly, user.name is the unaltered name as seen in the chatrooms, and
#     can be used for things like replying, but shouldn't be used for
#     comparisions.

import json
import time
from commands import CanPmReplyCommands
from commands import Command
from commands import GameCommands
from commands import IgnoreBroadcastPermission
from commands import IgnoreEscaping
from robot import PokemonShowdownBot
from robot import Room
from robot import User
from plugins.battling.battleHandler import supportedFormats
from plugins import moderation
from plugins.messages import MessageDatabase
from plugins.workshop import Workshop


class PSBot(PokemonShowdownBot):
    """This is the master class of the Pokemon Showdown Bot project.

    This is the entry point for the Pokemon Showdown Bot, and contain most of
    the permission checks for chat returns.

    It's derived from the base class PokemonShowdownBot, and as such hide a lot
    of it's core functions by simply calling functions from the base class.
    For any function called here not defined in this file, look in robot.py.

    Changes to this file should be made with caution, as much of the extended
    functions depend on this being structured in a specific way.

    Attributes:
        do: Command object which handles '.command' actions from the user
        usernotes: MessageDatabase object which handles all PMs sent from users
    """
    def __init__(self):
        """Initializes the PSBot class

        Setups up the commands, usernotes, and opens the websocket to the
        pokemonshowdown server
        """
        self.do = Command
        self.usernotes = MessageDatabase()
        PokemonShowdownBot.__init__(self,
                                    ("ws://sim.smogon.com:8000/showdown/"
                                     "websocket"),
                                    self.splitMessage)

    def splitMessage(self, ws, message):
        """ Splits the string received and delegates tasks to modules

        This method is the modified splitMessage that is passed to the open
        websocket. This method splits the string given by the websocket and
        delegates the tasks to the corresponding modules.

        Args:
            ws: websocket that is using this method.
            message: string given by websocket.
        Returns:
            None.
        Raises:
            None.
        """
        if not message:
            return
        if "\n" not in message:
            self.parseMessage(message, "")

        room = ""
        msg = message.split("\n")
        # this is the name of the room of the room we're currently in
        # i.e. ">joim"
        if msg[0].startswith(">"):
            room = msg[0][1:]
        msg.pop(0)

        if room.startswith("battle-"):
            if room not in self.rooms:
                # Battle rooms don't need the same interface as chatrooms
                self.rooms[room] = True
            if "deinit" in msg[0]:
                self.rooms.pop(room)
            # Go to battle handler instead of regular rooms
            # (I don't allow commands in battle rooms anyway)
            for m in msg:
                self.bh.parse(room, m)
            return
        # here we handle things like commands or saving user data
        for m in msg:
            self.parseMessage(m, room)

    def handleJoin(self, room, message):
        """Handles new users entering a room

        Args:
            room: Room object that we are inspecting
            message: string produced by each user on joining
        Returns:
            None.
        Raises:
            None.
        """
        if self.userIsSelf(message[1:]):
            room.rank = message[0]
            room.doneLoading()
        userid = self.toId(message)
        user = User(userid, message[0], self.isOwner(userid))
        # block banned users from this room
        if moderation.shouldBan(self, user, room):
            self.takeAction(room.title, user, "roomban", ("You are blacklisted"
                            " from this room, so please don't come here."))
            return
        room.addUser(user)
        # If the user have a message waiting, tell them that in a pm
        if self.usernotes.shouldNotifyMessage(user.id):
            self.sendPm(user.id, self.usernotes.pendingMessages(user.id))

    def parseMessage(self, msg, roomName):
        """Parses the message given by a user and delegates the tasks further

        This is the meat and bones of the program. This handles all user
        related queries such as commands. It also logs information so that the
        markov chain model can learn from the users.

        Args:
            room: Room object that we are inspecting.
            message: string produced by each user on joining.
                example: "|c:|1467521329| wgma|we need more cowbell".
        Returns:
            None.
        Raises:
            None.
        """
        if not msg.startswith("|"):
            return
        message = msg.split("|")
        room = self.getRoom(roomName)

        # Logging in
        if message[1] == "challstr":
            print("{name}: Attempting to login...".format(name=self.name))
            self.login(message[3], message[2])

        elif message[1] == "updateuser":
            self.updateUser(message[2], message[3])

        # Challenges
        elif "updatechallenges" in message[1]:
            challs = json.loads(message[2])
            if challs["challengesFrom"]:
                opp = list(challs["challengesFrom"].keys())[0]
                if challs["challengesFrom"][opp] in supportedFormats:
                    self.send("|/accept {name}".format(name=opp))
                else:
                    self.sendPm(opp, ("Sorry, I only accept challenges in "
                                      "Challenge Cup 1v1, Random Battles "
                                      "or Battle Factory :("))

        elif "updatesearch" in message[1]:
            # This gets sent before `updatechallenges` does when recieving a
            # battle, but it's not useful for anything, so just return straight
            # away
            return

        # This is a safeguard for l and n in case that a moderation action
        # happen
        elif("unlink" == message[1] or "uhtml" in message[1]or
             "html" == message[1]):
            return

        # As long as the room have a roomintro (which even groupchats do now)
        # Roomintros are also the last thing that is sent when joining a room
        # so when this show up, assume the room is loaded
        elif "raw" == message[1]:
            if message[2].startswith(('<div class="infobox infobox-roomintro">'
                                      '<div class="infobox-limited">')):
                room.doneLoading()

        # Joined new room
        elif "users" in message[1]:
            for user in message[2].split(",")[1:]:
                room.addUser(User(user[1:], user[0], self.isOwner(user[1:])))
            # If PS doesn't tell us we joined, this still give us our room rank
            room.rank = message[2][message[2].index(self.name) - 1]

        elif "j" in message[1].lower():
            self.handleJoin(room, message[2])

        elif "l" == message[1].lower() or "leave" == message[1].lower():
            if self.userIsSelf(message[2][1:]):
                # This is just a failsafe in case the bot is forcibly removed
                # from a room. Any other memory release required is handeled by
                # the room destruction
                if roomName in self.rooms:
                    self.rooms.pop(roomName)
                return
            userid = self.toId(message[2])
            room.removeUser(userid)
        elif "n" in message[1].lower() and len(message[1]) < 3:
            # Keep track of your own rank
            # When demoting / promoting a user the server sends a |N| message
            # to update the userlist
            if self.userIsSelf(message[2][1:]):
                room.rank = message[2][0]
            oldName = self.toId(message[3])
            room.renamedUser(oldName, User(message[2][1:], message[2][0]))

        # Chat messages
        elif "c" in message[1].lower():

            if room.loading:
                return
            user = room.getUser(self.toId(message[3]))
            if not user:
                return
            if self.userIsSelf(user.id):
                return

            # perform moderation on user content
            if room.moderate and self.canPunish(room):
                anything = moderation.shouldAct(message[4], user, room,
                                                message[2])
                if anything:
                    action, reason = moderation.getAction(self, room, user,
                                                          anything, message[2])
                    self.takeAction(room.title, user, action, reason)

            #update clever bot with last message
            if not message[4].startswith(self.commandchar):
                self.clever_bot.update(message[4].lower())

            # handle commands defined in our commands class
            if(message[4].startswith(self.commandchar) and message[4][1:] and
               message[4][1].isalpha()):
                command = self.extractCommand(message[4])
                self.log("Command", message[4], user.id)

                response, samePlace = "", True
                if not room.allowGames and command in GameCommands:
                    response = "This room does not support chatgames."
                else:
                    parsed_msg = message[4][len(command)+1:].lstrip()
                    if command != "m":
                        response, samePlace = self.do(self, command, room,
                                                      parsed_msg, user)
                    else:
                        response, samePlace = self.do(self, command, room,
                                                      parsed_msg, user,
                                                      roomName,
                                                      self.rooms_markov)
                # administer commands from commands
                if response == "NoAnswer":
                    return

                if self.details['debug'] or room.title != "joim" or user.isOwner():
                    if(self.evalRoomPermission(user, room) or
                       command in IgnoreBroadcastPermission):
                        if command not in IgnoreEscaping:
                            response = self.escapeText(response)

                            self.reply(room.title, user, response, samePlace)

                    elif not self.evalRoomPermission(user, room):
                        self.sendPm(user.id, ("Only {rank} users and up may use"
                                              " commands in this room."
                                              "").format(rank=room.broadcast_rank))

                    elif command in CanPmReplyCommands:
                        self.sendPm(user.id, self.escapeText(response))
                    else:
                        self.sendPm(user.id, "Please pm the commands for"
                                "a response.")

            if type(room.game) == Workshop:
                room.game.logSession(room.title, user.rank+user.name,
                                     message[4])

        elif "pm" in message[1].lower():
            user = User(message[2][1:], message[2][0],
                        self.isOwner(self.toId(message[2])))
            if self.userIsSelf(user.id):
                return

            if message[4].startswith("/invite"):
                if not message[4][8:] == "lobby":
                    if user.hasRank("+"):
                        self.joinRoom(message[4][8:])
                        self.log("Invite", message[4], user.id)
                    else:
                        self.sendPm(user.id, ("Only global voices (+) and up "
                                              "can add me to rooms, sorry :("))

            if(message[4].startswith(self.commandchar) and message[4][1:] and
               message[4][1].isalpha()):
                command = self.extractCommand(message[4])
                self.log("Command", message[4], user.id)
                # +1 to account for command character i.e. '.'
                params = (message[4][len(command)+1:]).lstrip()
                response = ""
                if command in GameCommands:
                    if params.startswith("score"):
                        response, where = self.do(self, command, Room("pm"),
                                                  params, user)
                    else:
                        response = "Don't try to play games in pm please"
                if not response:
                    response, where = self.do(self, command, Room("pm"),
                                              params, user)

                self.sendPm(user.id, response)

        # Tournaments
        elif "tournament" == message[1]:
            if room.loading:
                return
            if "create" in message[2]:
                if not room.tour:
                    room.createTour(self.ws, message[3])
                # Tour was created, join it if in supported formats
                if not self.details["joinTours"]:
                    return
                if room.tour and room.tour.format in supportedFormats:
                    room.tour.joinTour()
            elif "end" == message[2]:
                if not room.tour:
                    return
                winner, tier = room.tour.getWinner(message[3])
                if self.name in winner:
                    self.say(room.title,
                             "I won the {form} tournament!".format(form=tier))
                else:
                    self.say(room.title,
                             ("Congratulations to {name} for winning :)"
                              "").format(name=", ".join(winner)))
                room.endTour()
            elif "forceend" in message[2]:
                room.endTour()
            else:
                if room.tour:
                    room.tour.onUpdate(message[2:])


if __name__ == "__main__":
    psb = PSBot()
    restartCount = 0
    try:
        while restartCount < 100:
            # This function has a loop that runs as long as the websocket
            # is connected
            psb.ws.run_forever()
            # If we get here, the socket is closed and disconnected
            # so we have to reconnect and restart (after waiting a bit 
            # of course say half a minute)
            time.sleep(30)
            print("30 seconds since last disconnect. Retrying connection...")
            psb.openWebsocket()
            psb.addBattleHandler()
            restartCount += 1
            print("Restart Count:", restartCount)
    except KeyboardInterrupt:
        print("bot closed by KeyboardInterrupt")
        exit()
    except SystemExit:
        print("bot closed by SystemExit")
        exit()
