# -*- coding: utf-8 -*-
"""Module physical
Object and method about the I/O operations
"""

import csv
import os
 
class Safe:
    def __init__(self, newFinalCSV):
        self.finalCSV = newFinalCSV

    def file(self):
        """
        if the file already exists, it block the execution and saves original file
        """
        completePath =  CompletePath(self.path, self.filename) 
        if completePath.existing():
            raise Exception ("The file [{0}] exists already, I stop the elaboration and I don't write".format ( completePath.path() ) )
        else:
            self.finalCSV.file()
