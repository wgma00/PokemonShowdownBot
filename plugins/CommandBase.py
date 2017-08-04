import plugins.CommandAliases as CommandAliases


class DuplicateAliasConflict(Exception):
    pass


class UnreachableCommand(Exception):
    pass


class CommandBase(object):
    """Wrapper class for all commands written in this Bot.

    Defines main behaviour each command should have and also keeps track of
    duplicate commands.

    Attributes:
        aliases: list of str, keeps track of all the aliases that evoke this command
        has_html_box_feature: Bool, keeps track of this command has an optional behaviour if html boxes are enabled.
    """
    def __init__(self, aliases, has_html_box_feature):
        if not aliases:
            raise UnreachableCommand
        # check for conflicts and raise exception if found
        for alias in aliases:
            if CommandAliases.conflict(alias):
                raise DuplicateAliasConflict
            else:
                CommandAliases.add_alias(alias)
        self.aliases = aliases
        self.has_html_box_feature = has_html_box_feature

    def response(self, room, user, args):
        """ Returns a response to the user.

        Args:
            room: Room, room this command was evoked from.
            user: User, user who evoked this command.
            args: list of str, any sequence of parameters which are supplied to this command
        Returns:
            ReplyObject
        """
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

