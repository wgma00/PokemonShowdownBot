# The MIT License (MIT)
#
# Copyright (c) 2016 QuiteQuiet
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


# Each PS room joined creates an object here.
# Objects control settings on a room-per-room basis, meaning every room can
# be treated differently.


from plugins.tournaments import Tournament


class Room:
    """ Contains all important information of a pokemon showdown room. 
    
    Attributes:
        users: map, 
        loading:
        title:
        rank:
        moderate:
        allowGames:
        tour:
        game:
        tourwhiteList:
    """
    def __init__(self, room, data=None):
        """ 
        """
        '''(Room, str, str or {}) -> None
           Initliazes room object
        '''
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
        self.game = None
        self.tourwhitelist = data['tourwhitelist']

    def doneLoading(self):
        '''(Room) -> None'''
        self.loading = False

    def addUser(self, user):
        '''(Room, User) -> None'''
        if user.id not in self.users:
            self.users[user.id] = user

    def removeUser(self, userid):
        '''(Room, str) -> None'''
        if userid in self.users:
            return self.users.pop(userid)

    def renamedUser(self, old, new):
        '''(Room, User, User) -> None'''
        self.removeUser(old)
        self.addUser(new)

    def getUser(self, name):
        '''(Room, str) -> None or User)'''
        if name in self.users:
            return self.users[name]
        else:
            return False

    def isWhitelisted(self, user):
        '''(Room, Usr) -> Bool'''
        return user.hasRank('@') or user.id in self.tourwhitelist

    def addToWhitelist(self, user):
        '''(Room, User) -> Bool'''
        if user in self.tourwhitelist:
            return False
        self.tourwhitelist.append(user)
        return True

    def delFromWhitelist(self, target):
        '''(Room, User) -> Bool'''
        if target not in self.tourwhitelist:
            return False
        self.tourwhitelist.remove(target)
        return True

    def createTour(self, ws, form):
        '''(Room, websocket, ?) -> None'''
        self.tour = Tournament(ws, self.title, form)

    def endTour(self):
        '''(Room) -> None'''
        self.tour = None


# Commands
def allowgames(bot, cmd, room, msg, user):
    '''(PSBot, str, Room, str, User) -> (str, Bool)'''
    if not user.hasRank('#'):
        return 'You do not have permission to change this. (Requires #)', False
    msg = bot.removeSpaces(msg)
    things = msg.split(',')
    if not len(things) == 2:
        return """Too few/many parameters. Command is ~allowgames [room],
               True/False""", False

    if things[0] not in bot.rooms:
        return 'Cannot allow chatgames without being in the room', True

    if things[1] in ['true', 'yes', 'y', 'True']:
        if bot.getRoom(things[0]).allowGames:
            return """Chatgames are already allowed
                      in {room}""".format(room=things[0]), True
        bot.getRoom(things[0]).allowGames = True
        return """Chatgames are now allowed
                  in {room}""".format(room=things[0]), True

    elif things[1] in ['false', 'no', 'n', ' False']:
        bot.getRoom(things[0]).allowGames = False
        return """Chatgames are no longer allowed
                  in {room}""".format(room=things[0]), True
    return """{param} is not a supported
              parameter""".format(param=things[1]), True


def tour(bot, cmd, room, msg, user):
    '''(PSBot, str, Room, str, User) -> (str, Bool)'''
    if room.title == 'pm':
        return "You can't use this command in a pm.", False
    if not room.isWhitelisted(user):
        return """You are not allowed to use this command.
                  (Requires whitelisting by a Room Owner)""", True
    if not bot.canStartTour(room):
        return "I don't have the rank required to start a tour :(", True
    return '/tour {rest}'.format(rest=msg), True


def tourwl(bot, cmd, room, msg, user):
    '''(PSBot, str, Room, str, User) -> (str, Bool)'''
    if not user.hasRank('#'):
        return 'You do not have permission to change this. (Requires #)', False
    target = bot.toId(msg)
    if not room.addToWhitelist(target):
        return 'This user is already whitelisted in that room.', False
    bot.saveDetails()
    return """{name} added to the whitelist in this
              room.""".format(name=msg), True


def untourwl(bot, cmd, room, msg, user):
    '''(PSBot, str, Room, str, User) -> (str, Bool)'''
    if not user.hasRank('#'):
        return 'You do not have permission to change this. (Requires #)', False
    target = bot.toId(msg)
    if not room.delFromWhitelist(target):
        return 'This user is not whitelisted in that room.', False
    bot.saveDetails()
    return """{name} removed from the whitelist
              in this room.""".format(name=msg), True


RoomCommands = {
    'allowgames': allowgames,
    'tour': tour,
    'tourwl': tourwl,
    'untourwl': untourwl
}
