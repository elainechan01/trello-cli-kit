# module imports
from trellocli.trelloservice import trellojob
from trellocli.misc.custom_exceptions import *
from trellocli import SUCCESS

# dependencies imports
from typer import Typer, Option
from simple_term_menu import TerminalMenu
from rich import print
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm

from dotenv import load_dotenv

# misc imports
from typing_extensions import Annotated
import os


# singleton instances
app = Typer()
console = Console()

@app.command()
def card(
    board_name: Annotated[str, Option()] = ""
) -> None:
    """COMMAND to add a new trello card

    OPTIONS
        board_name (str): board to use
    """
    try:
        # check authorization
        res_authorize = trellojob.authorize()
        if res_authorize.status_code != SUCCESS:
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
            print("[bold red]Error![/] A problem occurred when retrieving the labels from the trello board")
            raise TrelloReadError
        labels_list = res_get_all_labels.res
        labels_dict = {label.name: label for label in labels_list if label.name}
        res_get_all_lists = trellojob.get_all_lists(board=board)
        if res_get_all_lists.status_code != SUCCESS:
            print("[bold red]Error![/] A problem occurred when retrieving the lists from the trello board")
            raise TrelloReadError
        trellolists_list = res_get_all_lists.res
        trellolists_dict = {trellolist.name: trellolist for trellolist in trellolists_list}     # for easy access to trellolist when given name of trellolist
        # request for user input (trellolist, card name, description, labels to include) interactively to configure new card to be added
        trellolist_menu = TerminalMenu(
            trellolists_dict.keys(),
            title="Select list:",
            raise_error_on_interrupt=True
        )                                                                               # Prompt: trellolist
        trellolist_menu.show()
        print(trellolist_menu.chosen_menu_entry)
        selected_trellolist = trellolists_dict[trellolist_menu.chosen_menu_entry]
        selected_name = Prompt.ask("Card name")                                       # Prompt: card name
        selected_desc = Prompt.ask("Description (Optional)", default=None)            # Prompt (Optional) description
        labels_menu = TerminalMenu(
            labels_dict.keys(),
            title="Select labels (Optional):",
            multi_select=True,
            multi_select_empty_ok=True,
            multi_select_select_on_accept=False,
            show_multi_select_hint=True,
            raise_error_on_interrupt=True
        )                                                                               # Prompt (Optional): labels
        labels_menu.show()
        selected_labels = [labels_dict[label] for label in list(labels_menu.chosen_menu_entries)] if labels_menu.chosen_menu_entries else None
        # display user selection and request confirmation
        print()
        confirmation_table = Table(title="Card to be Added", show_header=False)
        confirmation_table.add_row("List", selected_trellolist.name)
        confirmation_table.add_row("Name", selected_name)
        confirmation_table.add_row("Description", selected_desc)
        confirmation_table.add_row("Labels", ", ".join([label.name for label in selected_labels]) if selected_labels else None)
        console.print(confirmation_table)
        confirm = Confirm.ask("Confirm")
        # if confirm, attempt to add card to trello
            # else, exit
        if confirm:
            with console.status("Adding card...", spinner="aesthetic"):
                res_add_card = trellojob.add_card(
                    col=selected_trellolist,
                    name=selected_name,
                    desc=selected_desc,
                    labels=selected_labels
                )
                if res_add_card.status_code != SUCCESS:
                    print("[bold red]Error![/] A problem occurred when adding a new card to trello")
                    raise TrelloWriteError
            print(":party_popper: Card successfully added")
        else:
            print("Process cancelled...")
    except KeyboardInterrupt:
        print("[yellow]Keyboard Interrupt.[/] Program exited...")
    except (AuthorizationError, InvalidUserInputError, TrelloReadError, TrelloWriteError):
        print("Program exited...")
