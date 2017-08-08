from robot import ReplyObject
from user import User
from room import RoomCommands


def Command(self, cmd, room, msg, user):
    """ Handles commands given by the chat parser.

    Better documentation of the commands can be found in the COMMANDS.md file.

    Args:
        self: PSBot object of the main program.
        cmd: string representing the command the user wants to be done.
        room: Room object that this command was posted in.
        msg: the remaining message after this command.
        user: User object that initiated this command.
    Returns:
        Returns a Reply object a differing reply object depending on the
        nature of the command.
    Raises:
        Exception: There was likely improper input in the .calc command or
                   something I entirely missed lol.
    """
    if cmd == 'secret' and user.isOwner():
        return ReplyObject('This is a secret command!', True)

    return None
