# module imports
from trellocli import __app_name__
from trellocli.cli import cli
from trellocli.trelloservice import TrelloService

# dependencies imports
from typer import Typer

# misc imports


def main():
	cli.app(prog_name=__app_name__)

if __name__ == "__main__":
	main()