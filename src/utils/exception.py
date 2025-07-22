import sys
import logging

def error_message_details(error, error_detail: sys):
    """
    This function returns detailed error message including filename and line number.
    """
    exc_type, exc_value, exc_tb = error_detail.exc_info()

    if exc_tb is not None:
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno
        error_message = f"Error occurred in python script name [{file_name}] line number [{line_number}] error message [{str(error)}]"
    else:
        error_message = f"Error occurred with message: {str(error)}"

    return error_message

class EDAException(Exception):
    """
    This class helps to create a custom exception.
    """
    def __init__(self, error_message, error_detail:sys):
        """
        This method overrides the constructor of the parent Exception class.
        """
        super().__init__(error_message)
        self.error_message = error_message_details(error_message,error_detail=error_detail)

    def __str__(self):
        return self.error_message
    
if __name__ == "__main__":
    try:
        a = 1/0
    except Exception as e:
        logging.info("Divide by zero")
        raise EDAException(e,sys)
    
"""
This is a code that was used to test the custom exception.
""" 