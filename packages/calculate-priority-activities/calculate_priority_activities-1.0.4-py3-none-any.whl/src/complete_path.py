# -*- coding: utf-8 -*-
"""Module physical
Object and method about the I/O operations
"""

import csv
import os


class CompletePath:
    #TODO create decorator cache
    def __init__(self, new_partialPath, new_filename):
        self.filename = new_filename
        self.partialPath = new_partialPath

    def existing(self):
        """
        @return true if the path exists already in the hard disk
        """
        return os.path.exists( self.path () )

    def path(self):
        """
        @return complete path (withfilename) of the file
        """
        return "{0}{1}{2}".format(self.partialPath, os.sep , self.filename)

"""'
class TestCompletePath(unittest.TestCase): dependent on os, then it's not a unit test
"""


