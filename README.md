# Overview
Trello board management program via the command line

# Getting Started
1. Install the package: `pip install trello-cli-kit`
2. Retrieve your `Trello API Key` and `Trello API Secret` (How to get API key and secret from Trello: [Guide](https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction/)) and store them as environment variables as such:
    ```
    # .env

    TRELLO_API_KEY=<your_api_key>
    TRELLO_API_SECRET=<your_api_secret>
    ```

# Usage

## General Usage
```
trellocli GROUP | COMMAND

FLAGS
    --help: display help text for command
```

## Commands
### config
```
trellocli config

COMMANDS
    access: authorize program to trello account
    board: configure board to use
```

### list
```
trellocli list

FLAGS
    --is-detailed: display in detailed view

OPTIONS
    --board-name: provide name of trello board to execute on (required if board not previously set)
```

### create
```
trellocli create

COMMANDS
    card: create a trello card

OPTIONS
    --board-name: provide name of trello board to execute on (required if board not previously set)
```

## Use Cases
1. Configure a trello board to execute on
`trellocli config board`
2. Add a new trello card
`trellocli create card`
![Sample output trellocli create card](misc/images/create_card.png)
3. Display trello board data in a detailed view
`trellocli list --is-detailed`
![Sample output trellocli list --is-detailed](misc/images/list_detailed.png)

# References
1. [PyPI Release](https://pypi.org/project/trello-cli-kit/)
2. [How to Create a Python CLI Program for Trello Board Management (Part 1)](https://hackernoon.com/how-to-create-a-python-cli-program-for-trello-board-management-part-1)
