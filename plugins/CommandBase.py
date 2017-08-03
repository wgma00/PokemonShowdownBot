import plugins.CommandTriggers as CommandTriggers


class DuplicateTriggerConflict(Exception):
    pass

class CommandBase(object):
    """Wrapper class for all commands written in this Bot.

    Defines main behaviour each command should have and also keeps track of
    duplicate commands.

    Attributes:
        triggers: list of str, keeps track of all the triggers that evoke this command
        has_html_box_feature: Bool, keeps track of this command has an optional behaviour if html boxes are enabled.
    """
    def __init__(self, triggers, has_html_box_feature):
        # check for conflicts and raise exception if found
        for trigger in triggers:
            if CommandTriggers.conflict(trigger):
                raise DuplicateTriggerConflict
            else
                CommandTriggers.add_trigger(trigger)

        self.has_html_box_feature = has_html_box_feature

    def response(self, room, user, *args):
        """ Returns a response to the user.

        Args:
            room: Room, room this command was evoked from.
            user: User, user who evoked this command.
            args: any sequence of parameters which are supplied to this command
        Returns:
            ReplyObject
        """
        pass

    def _help(self, room, user, *kwargs):
        """ Returns a help response to the user.

        In particular gives more information about this command to the user.

        Args:
            room: Room, room this command was evoked from.
            user: User, user who evoked this command.
            args: any sequence of parameters which are supplied to this command
        Returns:
            ReplyObject
        """
        pass

    def _error(self, room, user, *kwargs):
        """ Returns an error response to the user.

        In particular gives a helpful error response to the user. Errors can range
        from internal errors to user input errors.

        Args:
            room: Room, room this command was evoked from.
            user: User, user who evoked this command.
            args: any sequence of parameters which are supplied to this command
        Returns:
            ReplyObject
        """
        pass

    def _success(self, room, user, *kwargs):
        """ Returns a success response to the user.

        Successfully returns the expected response from the user based on the args.

        Args:
            room: Room, room this command was evoked from.
            user: User, user who evoked this command.
            args: any sequence of parameters which are supplied to this command
        Returns:
            ReplyObject
        """
        pass

