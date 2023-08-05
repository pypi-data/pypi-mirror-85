from typing import List
from .param import Param
from .const import ParamTypes
from datetime import datetime
from XmlElement import XmlElement

class Job:
    def __init__(self, jobname:str, files:List[str]=[], **params):
        """Create a new Job() object.

        Keyword arguments:
        jobname -- String with the a blue jobname, i. e. 'dms.GetResultList'
        files -- (Optional) List of strings with file paths to add to the job.
        **params -- Add arbitrary job input parameters. Uses Param.infer_type() to guess the blue parameter type.
        """
        self.name = jobname
        self.params:List[Param] = []
        self.files = files
        for name, value in params.items():
            self.append(Param.infer_type(name, value))

    def __repr__(self):
        return self.name

    def append(self, param:Param):
        """Appends a job input parameter.
        Keyword arguments:
        param -- Param object.
        """
        self.params.append(param)

    def append_file(self, filepath:str):
        """Appends a job input file parameter.
        Keyword arguments:
        filepath -- String with file path to append.
        """        
        self.files.append(filepath)
