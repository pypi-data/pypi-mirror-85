# -*- coding: utf-8 -*-
"""Module physical
Object and method about the I/O operations
"""

import csv
import os
from .personal_logging import PersonalLogging
from .complete_path import CompletePath


class FinalCSV:

    def __init__(self, new_path, new_filename, newGroupPriority):
        self.filename = new_filename
        self.path = new_path
        self.groupPriority = newGroupPriority
        self.log = PersonalLogging()


    def file(self):
        """
        write the final file
        """
        result = []
        completePath =  CompletePath(self.path, self.filename) 
        with open(completePath.path(), 'w', newline='') as csvfile:
            fieldnames = ['Activity', 'Points']
            writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
            writer.writeheader()
            for i in range ( len( self.groupPriority.rows() ) ):
                tmp = self.groupPriority.rows()[i]
                self.log.info ( "FinalCSV", "file","data {0},{1}".format( tmp.activity(),  tmp.points() ) )
                writer.writerow({'Activity': tmp.activity(), 'Points': tmp.points()})
        self.log.info("FinalCSV", "file", "Elaborated file: {0}".format ( completePath.path() ) )
 
