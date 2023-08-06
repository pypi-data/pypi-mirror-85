# -*- coding: utf-8 -*-
"""Module importance
Object about the management of the data about the project and importance
"""

class ImportanceActivity:
    
    def __init__(self, new_importance):
        self.importance = new_importance#TODO decorator for default values

    def importance(self):
        """
        @return importance
        """
        return self.importance.importance() 

 
