import asyncio
from plugins.CommandBase import CommandBase
from showdown import ReplyObject


class Credits(CommandBase):
    """
    Usage: .credits
        - Returns a url to this page.
        [test](google.ca)
    """
    def __init__(self):
        super().__init__(aliases=['credits', 'git', 'source'], can_learn=False)

    def learn(self, room, user, data):
        pass

    @asyncio.coroutine 
    def response(self, room, user, args):
        """ Returns a response to the user.

        Args:
            room: Room, room this command was evoked from.
            user: User, user who evoked this command.
            args: no arguments should be passed except for help
        Returns:
            ReplyObject
        """
        yield from asyncio.sleep(0)
        if len(args) == 1 and args[0] == 'help':
            return self._help(room, user, args)
        elif len(args) >= 1:
            return self._error(room, user, 'too_many_params')
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
        return ReplyObject("Responds with url to this bot's source code", True)

    def _error(self, room, user, reason):
        """ Returns an error response to the user.

        In particular gives a helpful error response to the user. Errors can range
        from internal errors to user input errors.

        Args:
            room: Room, room this command was evoked from.
            user: User, user who evoked this command.
            reason: str,  reason for this error.
        Returns:
            ReplyObject
        """
        if reason == 'too_many_params':
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
        return ReplyObject('Source code can be found at: {url}'.format(url='https://github.com/wgma00/quadbot/'))
