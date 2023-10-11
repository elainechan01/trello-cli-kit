# module imports

# dependencies imports
from trello import Board, List as Trellolist, Label, Card

# misc imports
from typing import NamedTuple, List


class GetOAuthTokenResponse(NamedTuple):
    """Model to store response when retrieving user oauth tokens

    Attributes
        token (str): user oauth token
        token_secret (str): user oauth token secret
        status_code (int): success / error
    """
    token: str
    token_secret: str
    status_code: int

class AuthorizeResponse(NamedTuple):
    """Model to store response on whether the user has provided authorization for the program

    Attributes
        status_code (int): success / error
    """
    status_code: int

class GetAllBoardsResponse(NamedTuple):
    """Model to store response when retrieving all boards

    Attributes
        res (List[Board]): array of boards
        status_code (int): success / error
    """
    res: List[Board]
    status_code: int

class GetBoardResponse(NamedTuple):
    """Model to store response when retrieving board

    Attributes
        res (Board): board
        status_code (int): success / error
    """
    res: Board
    status_code: int

class GetAllListsResponse(NamedTuple):
    """Model to store response when retrieving all trello lists

    Attributes
        res (List[Trellolist]): array of trello lists
        status_code (int): success / error
    """
    res: List[Trellolist]
    status_code: int

class GetAllLabelsResponse(NamedTuple):
    """Model to store response when retrieving all labels

    Attributes
        res (List[Label]): array of labels
        status_code (int): success / error
    """
    res: List[Label]
    status_code: int

class GetAllCardsResponse(NamedTuple):
    """Model to store response when retrieving all cards

    Attributes
        res (Card): array of cards
        status_code (int): success / error
    """
    res: List[Card]
    status_code: int

class AddCardResponse(NamedTuple):
    """Model to store response when adding a new card

    Attributes
        res (Card): card
        status_code (int): success / error
    """
    res: Card
    status_code: int
