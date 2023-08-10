__app_name__ = "trellocli"
__version__ = "0.0.1"

(
	SUCCESS,
	TRELLO_WRITE_ERROR,
	TRELLO_READ_ERROR
) = range(3)

ERRORS = {
	TRELLO_WRITE_ERROR: "Error when writing to Trello",
	TRELLO_READ_ERROR: "Error when reading from Trello"
}