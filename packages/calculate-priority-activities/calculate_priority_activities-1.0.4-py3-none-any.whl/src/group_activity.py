# -*- coding: utf-8 -*-
"""Module timeActivity
Object about the management of the data about the project and time
"""
from datetime import date
from datetime import datetime
from .personal_logging import PersonalLogging


class GroupActivity:
    def __init__(self, newReadRows):
        self.readRows = newReadRows

    def __str__(self):
        return "GroupActivity:{0}".format(str( self.readRows ) )
    
    def __repr__(self):
        data = self.readRows
        return "GroupActivity[{0}]\n>[{1}]".format( len (data), data )
    
    def rows(self):
        """
        @return the list of Activities
        """
        return self.readRows
    


