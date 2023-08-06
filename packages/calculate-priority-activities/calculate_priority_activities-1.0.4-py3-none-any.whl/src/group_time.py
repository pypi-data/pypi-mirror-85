# -*- coding: utf-8 -*-
"""Module timeActivity
Object about the management of the date
"""

from .personal_logging import PersonalLogging
from .csv_time import CSVTime
from .row_time import RowTime
from .running import Late
from .running import Running
from .day_activity import DayActivity
from datetime import date
from datetime import datetime
from tests.test_state import State
from tests.test_number_days import NumberDays



class GroupTime:
    """
    list of DayActivity
    """
    def rows(self, reader):
        """
        @return the list of the time datas of the Activities
        """
        result = []
        for row in reader:
            tmp = CSVTime(row)
            day =  DayActivity ( RowTime ( tmp.activity(), tmp.start(), tmp.end() ) ) 
            result.append ( Late ( Running ( State ( NumberDays ( day.action() , day.start1(), day.end1()  ) ) ) ) ) 
        return result

