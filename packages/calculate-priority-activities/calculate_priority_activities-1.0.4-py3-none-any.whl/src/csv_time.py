# -*- coding: utf-8 -*-
"""Module csvtime
Object about the management of the data about the project and time
"""
from datetime import date
from datetime import datetime
from .personal_logging import PersonalLogging

class CSVTime:
    """@overview: this class contains the single row of time file"""
    def __init__(self, newrow):
        self.row = newrow
        
    def activity(self):
        return self.row['activity'].strip() 
   
    def start(self):
        return self.row['start'].strip() 

    def end(self):
        return self.row['end'].strip()
    
    def __repr__(self):
        return "CSVTime[{0}]\n>>>[{1}]\n>>>>>>>>>>[{2}]]".format(self.Activity(), self.start(), self.end())


"""
TestCSVTime: the class under test required an external CSV, than the unit is not isolated, then no unit test
"""
