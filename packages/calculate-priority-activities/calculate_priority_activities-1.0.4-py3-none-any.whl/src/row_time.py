# -*- coding: utf-8 -*-
"""Module timeActivity
Object about the management of the data about the project and time
"""
from datetime import date
from datetime import datetime
from .personal_logging import PersonalLogging


class RowTime:
    """@overview: this class contains the single row of time file"""
    def __init__(self, newActivity, newStart, newEnd):
        self.activity = newActivity
        self.start = newStart
        self.end = newEnd
        self.log = PersonalLogging()
        self.log.debug ("Rowtime","init","start:{0}".format ( str ( self.start)  ) ) 
        self.log.debug ("Rowtime","init","end:{0}".format ( str ( self.end)  ) ) 
    
    def __repr__(self):
        return "RowTime:{0}[{1}-{2}]".format(self.activity, self.start, self.end)

