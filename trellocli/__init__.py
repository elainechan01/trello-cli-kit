__app_name__ = "trellocli"
__version__ = "0.1.0"

(
	SUCCESS,
    TRELLO_AUTHORIZATION_ERROR,
	TRELLO_WRITE_ERROR,
	TRELLO_READ_ERROR
) = range(4)

ERRORS = {
    TRELLO_AUTHORIZATION_ERROR: "Error authorizing app to access user's trello account",
	TRELLO_WRITE_ERROR: "Error when writing to Trello",
	TRELLO_READ_ERROR: "Error when reading from Trello"
}