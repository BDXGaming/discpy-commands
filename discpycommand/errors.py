class CommandNotFound(Exception):
    """
    Called when a command is not found with the given name
    """
    def __init__(self):
        pass
    def __str__(self):
        return "No command found with the given name!"