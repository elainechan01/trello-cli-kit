# trello-cli-kit

# Overview
CLI program to modify your Trello boards from your computer's command line

# Getting Started
1. Install the package: `pip install trello-cli-kit`
2. Install dependencies: `pip install -r requirements.txt`
3. Retrieve your `Trello API Key` and `Trello API Secret` (How to get API key and secret from Trello: [Guide](https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction/)) and store them as environment variables as such:
    ```
    # .env

    TRELLO_API_KEY=<your_api_key>
    TRELLO_API_SECRET=<your_api_secret>
    ```

# Usage
1. General usage
`trellocli GROUP | COMMAND`
2. Initializing configurations
`trellocli config COMMAND`
3. Display data from trello board
`trellocli list [--is-detailed][--board-name=<BOARD_NAME>]`
4. Add a new card to a trello board
`trellocli create card [--board-name=<BOARD_NAME>]`

# References
1. [How to Create a Python CLI Program for Trello Board Management (Part 1)](https://hackernoon.com/how-to-create-a-python-cli-program-for-trello-board-management-part-1)
