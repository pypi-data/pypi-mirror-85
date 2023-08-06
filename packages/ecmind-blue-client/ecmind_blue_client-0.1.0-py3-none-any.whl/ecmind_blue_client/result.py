from .result_file import ResultFile
from typing import List

class Result:
    def __init__(self, values:dict, files:List[ResultFile], return_code:int, error_message:str):
        """Create a new Result() object.

        Keyword arguments:
        values -- Dictionary of output parameters.
        files -- List of ResultFile() output file parameters.
        return_code -- Integer representation of the job result.
        error_message -- String containing error responses from the server on None if return_code is 0.
        """
        self.values = values
        self.files = files
        self.return_code = return_code
        self.error_message = error_message