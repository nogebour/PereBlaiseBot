from .Error import Error, ErrorCode
import datetime


class ErrorManager:
    error_log = []

    def add_error(self, error_type=ErrorCode.INTERNAL_ERROR, context="N/A", timestamp=datetime.datetime.now()):
        ErrorManager.error_log.append(Error(error_type, context, timestamp))
        print("New Error added ! "+str(ErrorManager.error_log[-1]))
        print("Number of errors present :"+str(len(ErrorManager.error_log)))

    def clear_error(self):
        ErrorManager.error_log = []