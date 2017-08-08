from plugins.CommandBase import CommandBase
from robot import ReplyObject


class Broadcast(CommandBase):
    def __init__(self):
        super().__init__(aliases=['broadcast'], has_html_box_feature=False)

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
        elif len(args) >= 2:
            return self._error(room, user, 'too_many_args')
        elif len(args) == 1 and args[0] not in ['off', '+', '%', '@', '*', '#']:
            return self._error(room, user, 'invalid_arg')
        elif len(args) == 1 and room.isPM:
            return self._error(room, user, 'pms')
        elif len(args) == 1 and not user.hasRank('#'):
            return self._error(room, user, 'insufficient_rank')
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
        return ReplyObject(("If no arguments are passed, display current broadcast rank."
                            " Otherwise you can provide one of the following arguments: "
                            "off, +, %, @, *, #. This doesn't work in Pms."), True)

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
            return ReplyObject("This command only takes 1 argument", True)
        elif reason == 'invalid_arg':
            return ReplyObject("You have provided an invalid argument", True)
        elif reason == 'pms':
            return ReplyObject("There are no broadcast ranks in PMs", True)
        elif reason == 'insufficient_rank':
            return ReplyObject("This command is reserved for Room Owners(#)", True)

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
        if len(args) == 0:
            return ReplyObject('Rank required to broadcast: {rank}'.format(rank=room.broadcast_rank))
        else:
            broadcast_rank = ' ' if args[0] == 'off' else args[0]
            room.broadcast_rank = broadcast_rank
            return ReplyObject('Broadcast rank set to {rank}. (This is not saved on reboot)'.format(rank=broadcast_rank if not broadcast_rank == ' ' else 'none'), True)
