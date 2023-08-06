# -*- coding: utf-8 -*-
"""Module timeActivity
Object about the management of the date
"""

from .personal_logging import PersonalLogging
from .csv_time import CSVTime
from .row_time import RowTime
from datetime import date
from datetime import datetime
from tests.test_number_days import NumberDays


class TimeActivity:

    def days(self):
        """
        it offer the number of days in a Activity
        """        
        pass

    def action(self):
        pass

class Running(TimeActivity):
    """
    base case
    """
    def __init__(self, newState ):
        self.state = newState
        self.log = PersonalLogging()
        self.log.debug ( "Running", "init", "state:" + str ( self.state ) )

    def days(self):
        return self.state.numberDays.days()
 
    def action(self):
        return self.state.activity()

    def __repr__(self):
        return "Running:[{0}]".format( self.state )
    

class Late(TimeActivity):
    """
    case of past activtiy not yet done
    """
    def __init__(self, newTimeActivity ):
        self.timeActivity = newTimeActivity
        self.log = PersonalLogging()
        self.log.debug ( "Late", "init", "start:" + str ( self.timeActivity ) )

    def days(self):
        return self.timeActivity.days()
 
    def action(self):
        return self.timeActivity.action()
    
    def __repr__(self):
        return "Late:[{0}]".format( self.timeActivity )




