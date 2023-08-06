# -*- coding: utf-8 -*-
"""Module test_NumberDays
Object about the testing of the calculation of the number of days
"""
from datetime import date
from datetime import datetime
import pytest
from .numberdays import NumberDays


def testDaysMoreYearsOK ( temporalRange ):
    """
    test NumberDays.days(): number of days
    """
    numberDays = temporalRange.days()
    expected = 3545
    assert expected == numberDays
    
def testRunningOK ( temporalRange ):
    """
    test NumberDays.running(): state of a running activity
    """
    day = datetime.now().replace( hour=0, minute=0, second=0, microsecond=0)  
    runningState = temporalRange.running( day )
    expected = True
    assert True == runningState

def testFutureOK ( ):
    """
    test NumberDays.future(): state of a future activity
    """
    day = datetime.now().replace( hour=0, minute=0, second=0, microsecond=0)  
    start = datetime(2023, 12, 2, 10, 24, 34, 198130)
    due = datetime(2024, 10, 5, 10, 24, 34, 198130)
    futureState = NumberDays( "future-activity", start, due ).future( day )
    expected = True
    assert True == futureState

def testLateOK ( ) :
    """
    test NumberDays.late(): state of a late activity
    """
    day = datetime.now().replace( hour=0, minute=0, second=0, microsecond=0)  
    start = datetime(2020, 1, 2, 10, 24, 34, 198130)
    due = datetime(2020, 10, 5, 10, 24, 34, 198130)
    lateState = NumberDays("late-activity", start, due ).late( day )
    expected = True
    assert True == lateState

@pytest.fixture
def temporalRange () :
    """
    preparation of the test data. In this situation its useless because this funciton is called by one test,
    but it's a reference in the future refactoring
    """
    end = datetime.now().replace(year= 2030, month=7, day=20, hour=0, minute=0, second=0, microsecond=0)  
    start = datetime.now().replace(year= 2010, month=5, day=10, hour=0, minute=0, second=0, microsecond=0)
    return NumberDays ( "activity", start, end )

