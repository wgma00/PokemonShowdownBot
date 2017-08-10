from plugins.CommandBase import CommandBase
from plugins.images import OnlineImage
from robot import ReplyObject
from user import User
import requests
import random


class Xkcd(CommandBase):
    def __init__(self):
        super().__init__(aliases=['xkcd'], has_html_box_feature=False)

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
        elif len(args) == 1 and args[0] == 'showimage':
            return self._success(room, user, args)
        elif 1 <= len(args) <= 2 and (not args[0] == 'rand' and not args[0].isdigit()):
            return self._error(room, user, 'incorrect_args')
        else:
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
        return ReplyObject(("Responds with url to xkcd article. if left empty, returns most recent. If 'rand' is passed generates a random article. "
                            "If a 'number' is passed, returns that specified xkcd article. This command also supports showimages."), True)

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
        if reason == 'incorrect_args':
            return ReplyObject('first argument should be a number if you want a specific xkcd article, otherwise rand to chose a random article.', True)

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
        msg = args[0] if args else 'rand'
        show_image = args[-1] == 'showimage' if args else False

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
        elif msg and msg.isdigit() and 1 <= int(msg) <= data['num']:
            r = requests.get('http://xkcd.com/{num}/info.0.json'.format(num=int(msg)))
            data = r.json()
            uploaded_image = data['img']
            uploaded_image_dims = OnlineImage.get_image_info(uploaded_image)
            alt_data = data['alt']

        if User.compareRanks(room.rank, '*') and show_image:
            return ReplyObject(('/addhtmlbox <img src="{url}" height=100% width=100%></img>'
                                '<br><b>{alt}</b></br>').format(alt=alt_data, url=uploaded_image,
                                                                width=uploaded_image_dims[0]), True, True)
        else:
            return ReplyObject(uploaded_image, True)
