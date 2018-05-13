from enum import Enum


class ErrorCode(Enum):
    INTERNAL_ERROR = (0, "Internal error")
    NO_DOCUMENT_FOUND = (1, "No document found")
    NO_DOCUMENT_INSERTED = (2, "No document inserted")
    INVALID_REST_QUALITY = (3, "Invalid rest quality")
    INVALID_WALK_SPEED = (4, "Invalid walk speed")
    NOT_AN_INTEGER = (5, "Not an integer")
    UNABLE_TO_CONNECT_DB = (6, "Unable to connect to Database")
    NO_CHARACTER_FOUND = (7, "Unable to find the character associated to the player")
    GM_COMMAND_ONLY = (8, "Unable to use the command as you are not the GM")
    NOT_A_POSITIVE_INTEGER = (9, "A positive integer was expected")

    def __init__(self, error_code, error_message):
        self.error_code = error_code
        self.error_message = error_message


class Error:
    """Class defining an error based on :
    - its Error Code
    - its Error Message
    - its Context
    - its TimeStamp """

    def __init__(self, error_code_enum, context, timestamp):
        self.error_type = error_code_enum
        self.error_code = error_code_enum.error_code
        self.error_message = error_code_enum.error_message
        self.context = context
        self.timestamp = timestamp

    def __str__(self):
        return "[Type:"+str(self.error_type) +\
            ", Error Code:'"+str(self.error_code) +\
            "', Error Message:'"+self.error_message +\
            "', Context: '"+self.context +\
            "', Timestamp: "+str(self.timestamp)+"]"
