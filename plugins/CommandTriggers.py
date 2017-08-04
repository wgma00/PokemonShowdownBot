global_triggers = {}


def conflict(command_triggers):
    """Determines if there are conflicting commands

    Args:
        command_triggers: list of str, triggers for this command
    Returns:
        True if there is a conflict, false otherwise
    """
    for trigger in command_triggers:
        if trigger in global_triggers:
            return True
    return False


def add_trigger(trigger):
    """Add triggers to global triggers"""
    global_triggers[trigger] = True
