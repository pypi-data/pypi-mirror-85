# -*- coding: utf-8 -*-
"""Module timeActivity
Object about the management of the date
"""

from .personal_logging import PersonalLogging
from .csv_time import CSVTime
from .row_time import RowTime
from datetime import date
from datetime import datetime


class DayActivity:
    """
    Abstract represensation of the data by CSV row of project-date.
    To test, it need a fake rowtime
    """
    def __init__(self, newRowTime):
        self.rowTime = newRowTime
        self.log = PersonalLogging()

    def start1(self):    
        """
        @return the start date as Date
        """ 
        return self.ddmmyyyy(self.rowTime.start)

    def end1(self):
        """
        @return the end date as Date
        """
        return self.ddmmyyyy(self.rowTime.end)

    def action(self):
        """
        @return the name of activity
        """
        return self.rowTime.activity

    def ddmmyyyy(self, dateAsString):
        """
        @return object date
        """
        return datetime.strptime(dateAsString, "%d/%m/%Y").replace(hour=0, minute=0, second=0, microsecond=0 ) #centralize in a class

    def __repr__(self):
        return "DayActivity:{0}-{1}:{2}".format (self.rowTime, self.start1(), self.end1() )
    

