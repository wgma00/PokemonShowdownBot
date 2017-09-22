from plugins.CommandBase import CommandBase
from robot import ReplyObject


class Send(CommandBase):
    def __init__(self):
        super().__init__(aliases=['send'], can_learn=False)

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
        elif not user.isOwner():
            return self._error(room, user, 'not_owner')
        else:
            new_args = [''.join(args)]  # in this case merge anything that may have been split by commas.
            return self._success(room, user, new_args)

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
        return ReplyObject('Responds with arguments passed to this command, reserved for bot owner', True)

    def _error(self, room, user, reason):
        """ Returns an error response to the user.

        In particular gives a helpful error response to the user. Errors can range
        from internal errors to user input errors.

        Args:
            room: Room, room this command was evoked from.
            user: User, user who evoked this command.
            reason: str, reason for this error
        Returns:
            ReplyObject
        """
        if reason == 'not_owner':
            return ReplyObject("This command is reserved for this bot's owner", True)

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
        return ReplyObject(args[0], True, True)
