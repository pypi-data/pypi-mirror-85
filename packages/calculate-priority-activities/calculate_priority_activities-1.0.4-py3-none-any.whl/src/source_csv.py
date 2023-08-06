# -*- coding: utf-8 -*-
"""Module physical
Object and method about the I/O operations
"""

import csv
import os
from .personal_logging import PersonalLogging
from .complete_path import CompletePath

class SourceCSV:
    def __init__(self, newPath, newFilename, newGroupTime):
        self.filename = newFilename
        self.path = newPath
        self.groupTime = newGroupTime
        self.log = PersonalLogging()

    def file(self):
        """
        read the data from the file
        """
        result = []
        completePath =  CompletePath(self.path, self.filename)
        if completePath.existing() :
            with open(completePath.path(), newline = '') as csvfile:
                result = self.groupTime.rows ( csv.DictReader ( csvfile ) )
        else:
            raise Exception ("The file [{0}] is not present, I stop the elaboration ".format (  completePath.path()    )       )
        self.log.info( "SourceCSV", "file", "Elaborated file: {0}".format(  completePath.path() ) )
        self.log.debug( "SourceCSV", "file", "rows:\n{0}".format (str ( result ) ) ) 
        return result

