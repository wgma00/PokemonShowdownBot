from plugins.CommandBase import CommandBase
from robot import ReplyObject


class Test(CommandBase):
    def __init__(self):
        super().__init__(triggers=['test'], has_html_box_feature=False)

    def response(self, room, user, args):
        """ Returns a response to the user.

        Args:
            room: Room, room this command was evoked from.
            user: User, user who evoked this command.
            args: no arguments should be passed except for help
        Returns:
            ReplyObject
        """
        print(len(args), args)
        if len(args) == 1 and args[0] == 'help':
            print('help:', self._help(room, user, args).text)
            return self._help(room, user, args)
        elif len(args) != 0:
            return self._error(room, user, ['param'])
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
        return ReplyObject('Responds with word "test"', True)

    def _error(self, room, user, args):
        """ Returns an error response to the user.

        In particular gives a helpful error response to the user. Errors can range
        from internal errors to user input errors.

        Args:
            room: Room, room this command was evoked from.
            user: User, user who evoked this command.
            args: list of str, any sequence of parameters which are supplied to this command
        Returns:
            ReplyObject
        """
        if args[0] == 'param':
            return ReplyObject('This command takes 0 parameters', True)

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
        return ReplyObject('test', True)
