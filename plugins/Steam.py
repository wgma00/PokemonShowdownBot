from plugins.CommandBase import CommandBase
from plugins.images import OnlineImage
from robot import ReplyObject
from user import User

import time
import requests
import json


class Steam(CommandBase):
    def __init__(self):
        super().__init__(aliases=['steam'], can_learn=False)
        self.data = {}
        self.key_lookup = {}
        try:
            with open('steam.json') as data_file:
                self.data = json.load(data_file)
        except: 
            r = requests.get('http://api.steampowered.com/ISteamApps/GetAppList/v0002/', params={'format': 'json'})
            self.data = r.json()
            with open('steam.json', 'w') as outfile:
                json.dump(self.data, outfile)
        # intitate reverse keylookup
        for item in self.data['applist']['apps']:
            appid, name = item['appid'], item['name']
            lower_name = name.lower()
            self.key_lookup[str(appid)] = lower_name


    def learn(self, room, user, data):
        pass

    def response(self, room, user, args):
        """ Returns a response to the user.

        Args:
            room: Room, room this command was evoked from.
            user: User, user who evoked this command.
            args: no arguments should be passed except for help
        Returns:
            ReplyObject
        """
        if len(args) == 1 and args[0] == 'help':
            return self._help(room, user, args)
        elif len(args) > 2:
            return self._error(room, user, 'too_many_args')
        elif args[0] in self.key_lookup:
            return self._success(room, user, args)

    def _help(self, room, user, args):
        """ Returns a help response to the user.

        In particular gives more information about this command to the user.

        Args:
            room: Room, room this command was evoked from.
            user: User, user who evoked this command.
            args: list of str, any sequence of parameters which are supplied to this command
        Returns:
            ReplyObject
        """
        return ReplyObject("For now supply the steamid for the game you want more info for i.e. dark souls 3 is 374320", True)

    def _error(self, room, user, reason):
        """ Returns an error response to the user.

        In particular gives a helpful error response to the user. Errors can range
        from internal errors to user input errors.

        Args:
            room: Room, room this command was evoked from.
            user: User, user who evoked this command.
            reason: str, reason for this error.
        Returns:
            ReplyObject
        """
        if reason == 'too_many_args':
            return ReplyObject("This command doesn't take any arguments", True)

    def _success(self, room, user, args):
        """ Returns a success response to the user.

        Successfully returns the expected response from the user based on the args.

        Args:
            room: Room, room this command was evoked from.
            user: User, user who evoked this command.
            args: list of str, any sequence of parameters which are supplied to this command
        Returns:
            ReplyObject
        """
        gameid = args[0]
        show_image = args[-1] == 'showimage' if args else False
        game_url = 'https://store.steampowered.com/app/{}'.format(gameid) 
        steaminfo = {'appids': gameid}
        r = requests.get('http://store.steampowered.com/api/appdetails', params=steaminfo)
        game_data = r.json()[gameid]['data']
        header_image, name, description = game_data['header_image'], game_data['name'], game_data['short_description']
        width, height = OnlineImage.get_image_info(header_image)
        if User.compareRanks(room.rank, '*') and show_image:
            res = ReplyObject(('/addhtmlbox <div id="gameinfo"> <img src="{}" height="{}" width="{}"></img> <p>Name: <a href="{}"> {}</a></p> <p>Description: {} </p> </div>').format(header_image, height, width, game_url, name, description), True, True)
            print(res.text)
            return res
        else:
            return ReplyObject('Name: {} Link: Description: {}'.format(name, game_url, description), True)
    

