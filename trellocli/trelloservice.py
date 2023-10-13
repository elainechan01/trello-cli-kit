# module imports
from trellocli import TRELLO_AUTHORIZATION_ERROR, TRELLO_READ_ERROR, TRELLO_WRITE_ERROR, SUCCESS
from trellocli.misc.models import *

# dependencies imports
from trello import TrelloClient, create_oauth_token
from dotenv import load_dotenv, find_dotenv, set_key

# misc imports
import os

class TrelloService:
    """Class to implement the business logic needed to interact with Trello"""
    def __init__(self) -> None:
        self.__client = None

    def __load_oauth_token_env_var(self) -> None:
        """Private method to configure user's oauth token as an environment variable"""
        load_dotenv()
        if not os.getenv("TRELLO_OAUTH_TOKEN"):
            res = self.__get_user_oauth_token()
            if res.status_code == SUCCESS:
                dotenv_path = find_dotenv()
                set_key(
                    dotenv_path=dotenv_path,
                    key_to_set="TRELLO_OAUTH_TOKEN",
                    value_to_set=res.token
                )
            else:
                print("User denied access.")

    def __get_user_oauth_token(self) -> GetOAuthTokenResponse:
        """Method to retrieve user's oauth token

        Returns
            GetOAuthTokenResponse: user's oauth token
        """
        try:
            res = create_oauth_token()
            return GetOAuthTokenResponse(
                token=res["oauth_token"],
                token_secret=res["oauth_token_secret"],
                status_code=SUCCESS
            )
        except:
            return GetOAuthTokenResponse(
                token="",
                token_secret="",
                status_code=TRELLO_AUTHORIZATION_ERROR
            )
    
    def authorize(self) -> AuthorizeResponse:
        """Method to authorize program to user's trello account
        
        Returns
            AuthorizeResponse: success / error
        """
        self.__load_oauth_token_env_var()
        load_dotenv()
        if not os.getenv("TRELLO_OAUTH_TOKEN"):
            return AuthorizeResponse(status_code=TRELLO_AUTHORIZATION_ERROR)
        else:
            self.__client = TrelloClient(
                api_key=os.getenv("TRELLO_API_KEY"),
                api_secret=os.getenv("TRELLO_API_SECRET"),
                token=os.getenv("TRELLO_OAUTH_TOKEN")
            )
            return AuthorizeResponse(status_code=SUCCESS)
    
    def is_authorized(self) -> bool:
        """Method to check authorization to user's trello account
        
        Returns
            bool: authorization to user's account
        """
        if not self.__client:
            return False
        else:
            return True

    def get_all_boards(self) -> GetAllBoardsResponse:
        """Method to list all boards from user's account

        Returns
            GetAllBoardsResponse: array of user's trello boards
        """
        try:
            res = self.__client.list_boards()
            return GetAllBoardsResponse(
                res=res,
                status_code=SUCCESS
            )
        except:
            return GetAllBoardsResponse(
                res=[],
                status_code=TRELLO_READ_ERROR
            )

    def get_board(self, board_id: str) -> GetBoardResponse:
        """Method to retrieve board

        Required Args
            board_id (str): board id

        Returns
            GetBoardResponse: trello board
        """
        try:
            res = self.__client.get_board(board_id=board_id)
            return GetBoardResponse(
                res=res,
                status_code=SUCCESS
            )
        except:
            return GetBoardResponse(
                res=None,
                status_code=TRELLO_READ_ERROR
            )

    def get_all_lists(self, board: Board) -> GetAllListsResponse:
        """Method to list all lists (columns) from the trello board

        Required Args
            board (Board): trello board

        Returns
            GetAllListsResponse: array of trello lists
        """
        try:
            res = board.all_lists()
            return GetAllListsResponse(
                res=res,
                status_code=SUCCESS
            )
        except:
            return GetAllListsResponse(
                res=[],
                status_code=TRELLO_READ_ERROR
            )

    def get_all_labels(self, board: Board) -> GetAllLabelsResponse:
        """Method to list all labels from the trello board

        Required Args
            board (Board): trello board

        Returns
            GetAllLabelsResponse: array of trello lists
        """
        try:
            res = board.get_labels()
            return GetAllLabelsResponse(
                res=res,
                status_code=SUCCESS
            )
        except:
            return GetAllLabelsResponse(
                res=None,
                status_code=TRELLO_READ_ERROR
            )

    def get_all_cards(self, trellolist: Trellolist) -> GetAllCardsResponse:
        """Method to list all cards from a trellolist

        Required Args
            trellolist (Trellolist): trellolist

        Returns
            GetAllCardsResponse: array of trello cards
        """
        try:
            res = trellolist.list_cards()
            return GetAllCardsResponse(
                res=res,
                status_code=SUCCESS
            )
        except:
            return GetAllCardsResponse(
                res=None,
                status_code=TRELLO_READ_ERROR
            )

    def add_card(
            self,
            col: Trellolist,
            name: str,
            desc: str = "",
            labels: List[Label] = []
    ) -> AddCardResponse:
        """Method to add a new card to a list (column) on the trello board

        Required Args
            col (Trellolist): trello list
            name (str): card name

        Optional Args
            desc (str): card description
            labels (List[Label]): list of labels to be added to the card

        Returns
            AddCardResponse: newly-added card
        """
        try:
            # create new card
            new_card = col.add_card(name=name)
            # add optional description
            if desc:
                new_card.set_description(description=desc)
            # add optional labels
            if labels:
                for label in labels:
                    new_card.add_label(label=label)
            return AddCardResponse(
                res=new_card,
                status_code=SUCCESS
            )
        except:
            return AddCardResponse(
                res=new_card,
                status_code=TRELLO_WRITE_ERROR
            )



# singleton instance
trellojob = TrelloService()
