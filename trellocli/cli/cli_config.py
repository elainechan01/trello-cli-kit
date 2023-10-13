# module imports
from trellocli.trelloservice import trellojob
from trellocli.misc.custom_exceptions import *
from trellocli import SUCCESS

# dependencies imports
from typer import Typer
from simple_term_menu import TerminalMenu
from rich import print

from dotenv import find_dotenv, set_key

# misc imports


# singleton instances
app = Typer()

@app.command()
def access() -> None:
    """COMMAND to configure authorization for program to access user's Trello account"""
    try:
        # check authorization
        res_authorize = trellojob.authorize()
        if res_authorize.status_code != SUCCESS:
            print("[bold red]Error![/] Authorization hasn't been granted. Try running `trellocli config access`")
            raise AuthorizationError
    except KeyboardInterrupt:
        print("[yellow]Keyboard Interrupt.[/] Program exited...")
    except AuthorizationError:
        print("Program exited...")

@app.command()
def board() -> None:
    """COMMAND to initialize Trello board"""
    try:
        # check authorization
        res_is_authorized = trellojob.is_authorized()
        if not res_is_authorized:
            print("[bold red]Error![/] Authorization hasn't been granted. Try running `trellocli config access`")
            raise AuthorizationError
        # retrieve all boards
        res_get_all_boards = trellojob.get_all_boards()
        if res_get_all_boards.status_code != SUCCESS:
            print("[bold red]Error![/] A problem occurred when retrieving trello boards")
            raise TrelloReadError
        boards_list = {board.name: board.id for board in res_get_all_boards.res}    # for easy access to board id when given board name
        # display menu to select board
        boards_menu = TerminalMenu(
            boards_list.keys(),
            title="Select board:",
            raise_error_on_interrupt=True
        )
        boards_menu.show()
        selected_board = boards_menu.chosen_menu_entry
        # set board ID as env var
        dotenv_path = find_dotenv()
        set_key(
            dotenv_path=dotenv_path,
            key_to_set="TRELLO_BOARD_ID",
            value_to_set=boards_list[selected_board]
        )
    except KeyboardInterrupt:
        print("[yellow]Keyboard Interrupt.[/] Program exited...")
    except (AuthorizationError, TrelloReadError):
        print("Program exited...")
