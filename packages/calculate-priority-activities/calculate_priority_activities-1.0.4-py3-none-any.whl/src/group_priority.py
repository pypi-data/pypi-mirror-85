# -*- coding: utf-8 -*-
"""Module priority
Object about the management of the data about the project and priority
"""

from .running import Running
from .priority import Priority
from .my_csv import CSV
from .personal_logging import PersonalLogging


class GroupPriority:    
    def __init__(self, newListPriority):
        self.listPriority = newListPriority
        self.log = PersonalLogging()

    def __str__(self):
        return "GroupPriority:{0}".format(str( self.listPriority ) )
    
    def __repr__(self):
        return "GroupPriority[{0}]\n>[{1}]".format( len ( self.listPriority ), self.listPriority)

    def sort(self, listImportance):
        """
        sort the list of Priority objects in order ascent of number of days and importance
        """
        return self.union(listImportance)

    def union (self, listImportance):
        """
        join the data of the attribute list and the list of activities with their importance
        """
        result = []
        for i in range ( len ( listImportance )  ) :
            date = self.listPriority.rows()[i]
            importance = listImportance[i]
            self.log.debug ("GroupPriority", "union","date:{0}".format( str ( date ) ) ) 
            if date.action() == importance.activity():
                result.append ( CSV ( Priority (  date  , importance) ) )
            else:
                raise Exception("Different project in row {0}:{1}-{2};".format( str(i) , date.action(), importance.activity() ) )
        return GroupPriority(result)        
    
    def rows(self):
        """
        @return the list of activities with thir dates
        """
        return self.listPriority
