# -*- coding: utf-8 -*-
"""Module importance
Object about the management of the data about the project and importance
"""

from .personal_logging import PersonalLogging

class GroupImportance:
    
    def __init__(self):
        pass

    def rows(self, reader):#TODO maybe reuse another class
        """
        @return the importance data of the Activities
        """
        result = []
        for row in reader:
            result.append ( RowImportance(row) )
        return result


class RowImportance:
    def __init__(self, newrow):
        self.row = newrow
        
    def activity(self):
        return self.row['activity'].strip() 
   
    def importance(self):
        return self.row['importance'].strip() 

    def area(self):
        return self.row['area'].strip()

    def __str__(self):
        return "RowImportance:{0}".format(self.row)
    
    def __repr__(self):
        return "RowImportance[{0}]\n>>>[{1}]\n>>>>>>>>>>[{2}]".format(self.activity(), self.importance(), self.area())


class ImportanceActivity:
    def __init__(self, new_importance):
        self.importance = new_importance#TODO decorator for default values

    def importance(self):
        """
        @return importance
        """
        return self.importance.importance() 

 
