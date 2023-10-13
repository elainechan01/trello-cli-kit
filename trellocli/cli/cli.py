# module imports
from trellocli.trelloservice import trellojob
from trellocli.cli import cli_config, cli_create
from trellocli.misc.custom_exceptions import *
from trellocli import SUCCESS

# dependencies imports
from typer import Typer, Option
from rich import print
from rich.console import Console
from rich.table import Table

from dotenv import load_dotenv

# misc imports
from typing_extensions import Annotated
import os


# singleton instances
app = Typer()
console = Console()

# init command groups
app.add_typer(cli_config.app, name="config", help="COMMAND GROUP to initialize configurations")
app.add_typer(cli_create.app, name="create", help="COMMAND GROUP to create new Trello elements")

@app.command()
def list(
    detailed: Annotated[
        bool,
        Option(help="Enable detailed view")
    ] = None,
    board_name: Annotated[str, Option()] = ""
) -> None:
    """COMMAND to list board details in a simplified (default)/detailed view

    OPTIONS
        detailed (bool): request for detailed view
        board_name (str): board to use
    """
    try:
        # check authorization
        res_is_authorized = trellojob.is_authorized()
        if not res_is_authorized:
            print("[bold red]Error![/] Authorization hasn't been granted. Try running `trellocli config access`")
            raise AuthorizationError
        # if board_name OPTION was given, attempt to retrieve board id using the name
            # else attempt to retrieve board id stored as an env var
        board_id = None
        if not board_name:
            load_dotenv()
            if not os.getenv("TRELLO_BOARD_ID"):
                print("[bold red]Error![/] A trello board hasn't been configured to use. Try running `trellocli config board`")
                raise InvalidUserInputError
            board_id = os.getenv("TRELLO_BOARD_ID")
        else:
            res_get_all_boards = trellojob.get_all_boards()
            if res_get_all_boards.status_code != SUCCESS:
                print("[bold red]Error![/] A problem occurred when retrieving boards from trello")
                raise TrelloReadError
            boards_list = {board.name: board.id for board in res_get_all_boards.res}    # retrieve all board id(s) and find matching board name
            if board_name not in boards_list:
                print("[bold red]Error![/] An invalid trello board name was provided. Try running `trellocli config board`")
                raise InvalidUserInputError
            board_id = boards_list[board_name]
        # configure board to use
        res_get_board = trellojob.get_board(board_id=board_id)
        if res_get_board.status_code != SUCCESS:
            print("[bold red]Error![/] A problem occurred when configuring the trello board to use")
            raise TrelloReadError
        board = res_get_board.res
        # retrieve data (labels, trellolists) from board
        res_get_all_labels = trellojob.get_all_labels(board=board)
        if res_get_all_labels.status_code != SUCCESS:
            print("[bold red]Error![/] A problem occurred when retrieving data from board")
            raise TrelloReadError
        labels_list = res_get_all_labels.res
        res_get_all_lists = trellojob.get_all_lists(board=board)
        if res_get_all_lists.status_code != SUCCESS:
            print("[bold red]Error![/] A problem occurred when retrieving data from board")
            raise TrelloReadError
        trellolists_list = res_get_all_lists.res
        # store data on cards for each trellolist
        trellolists_dict = {trellolist: [] for trellolist in trellolists_list}
        for trellolist in trellolists_list:
            res_get_all_cards = trellojob.get_all_cards(trellolist=trellolist)
            if res_get_all_cards.status_code != SUCCESS:
                print("[bold red]Error![/] A problem occurred when retrieving cards from trellolist")
                raise TrelloReadError
            cards_list = res_get_all_cards.res
            trellolists_dict[trellolist] = cards_list
        # display data (lists count, cards count, labels)
            # if is_detailed OPTION is selected, display data (name, description, labels) for each card in each trellolist
        print()
        table = Table(title="Board: "+board.name, title_justify="left", show_header=False)
        table.add_row("[bold]Lists count[/]", str(len(trellolists_list)))
        table.add_row("[bold]Cards count[/]", str(sum([len(cards_list) for cards_list in trellolists_dict.values()])))
        table.add_row("[bold]Labels[/]", ", ".join([label.name for label in labels_list if label.name]))
        console.print(table)
        if detailed:
            for trellolist, cards_list in trellolists_dict.items():
                table = Table("Name", "Desc", "Labels", title="List: "+trellolist.name, title_justify="left")
                for card in cards_list:
                    table.add_row(card.name, card.description, ", ".join([label.name for label in card.labels if label.name]))
                console.print(table)
        print()
    except (AuthorizationError, InvalidUserInputError, TrelloReadError):
        print("Program exited...")
