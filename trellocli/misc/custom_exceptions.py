class TrelloReadError(BaseException):
    """unable to read from Trello"""
    pass

class TrelloWriteError(BaseException):
    """unable to write to Trello"""
    pass

class InvalidUserInputError(BaseException):
    """user input not recognized"""
    pass

class AuthorizationError(BaseException):
    """program isn't authorized to access user's Trello"""
    pass